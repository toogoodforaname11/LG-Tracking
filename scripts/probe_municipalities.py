#!/usr/bin/env python3
"""Discover the official website + meeting platform for Alberta municipalities.

This is a one-shot ops script used during the Alberta rollout. For every
short_name we don't yet have a website for, it:

1. Tries a list of candidate hostnames derived from the name
   (e.g. ``townof<slug>.ca``, ``<slug>.ca``, ``<slug>ab.ca``, ...).
2. Picks the first one that returns 200 OK on HTTPS.
3. Fetches the homepage and grep for known meeting-platform patterns
   (CivicWeb, eSCRIBE, Granicus, Legistar, custom YouTube/handle).
4. Writes a JSON report to the path given via ``--out`` (default
   ``/tmp/alberta-probe.json``).

The script is **read-only** with respect to the database — it never seeds
or modifies anything. Operators consume the JSON report manually (or with
a follow-up patch script) to update ``seed_registry.py``.

Usage:
    scripts/probe_municipalities.py                            # probe all AB munis without a website
    scripts/probe_municipalities.py --start 0 --count 10       # probe 10 munis starting at index 0
    scripts/probe_municipalities.py --short-name "Banff"       # probe one
"""

import argparse
import asyncio
import json
import os
import re
import sys
from typing import Iterable

# Ensure the backend package is importable.
backend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "backend")
sys.path.insert(0, backend_dir)
os.chdir(backend_dir)

import httpx  # noqa: E402

from app.services.seed_registry import (  # noqa: E402
    ALBERTA_MUNICIPALITIES_PHASE_1,
    ALBERTA_MUNICIPALITIES_REMAINDER,
)


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/125.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}


def _slug(name: str) -> str:
    """Lowercase + alphanumeric-only slug for hostname candidates."""
    return re.sub(r"[^a-z0-9]", "", name.lower())


def _slug_dashed(name: str) -> str:
    """Lowercase + replace runs of non-alpha with dashes."""
    s = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return s


def _candidate_hosts(short_name: str) -> list[str]:
    """Generate candidate hostnames for a given short_name.

    Order matters: most-specific patterns first so the first 200 wins.
    """
    slug = _slug(short_name)
    dashed = _slug_dashed(short_name)
    name_lc = short_name.lower()

    # Detect entity prefixes ("County of Foo", "SV Foo", etc.) so we can
    # build patterns like ``foocounty.ca`` rather than ``countyoffoo.ca``.
    prefix = ""
    bare = slug
    bare_dashed = dashed
    if name_lc.startswith("county of "):
        prefix = "countyof"
        tail = name_lc[len("county of "):]
        bare = _slug(tail)
        bare_dashed = _slug_dashed(tail)
    elif name_lc.startswith("sv "):
        prefix = "summervillage"
        tail = name_lc[len("sv "):]
        bare = _slug(tail)
        bare_dashed = _slug_dashed(tail)
    elif name_lc.endswith(" county"):
        prefix = "county"
        tail = name_lc[: -len(" county")]
        bare = _slug(tail)
        bare_dashed = _slug_dashed(tail)

    candidates = [
        f"www.{slug}.ca",
        f"{slug}.ca",
        f"www.townof{bare}.ca",
        f"townof{bare}.ca",
        f"www.cityof{bare}.ca",
        f"cityof{bare}.ca",
        f"www.villageof{bare}.ca",
        f"villageof{bare}.ca",
        f"www.{bare}county.ca",
        f"{bare}county.ca",
        f"www.{bare_dashed}.ca",
        f"{bare_dashed}.ca",
        f"www.{slug}.com",
        f"{slug}.com",
        f"www.{bare}-ab.ca",
        f"{bare}-ab.ca",
    ]
    if prefix == "summervillage":
        candidates.insert(0, f"www.summervillageof{bare}.ca")
        candidates.insert(0, f"summervillageof{bare}.ca")
    if prefix == "county":
        candidates.insert(0, f"www.{bare}county.ca")
    if prefix == "countyof":
        candidates.insert(0, f"www.countyof{bare}.ca")
        candidates.insert(0, f"countyof{bare}.ca")

    # Dedupe while preserving order.
    seen: set[str] = set()
    deduped: list[str] = []
    for c in candidates:
        if c not in seen:
            seen.add(c)
            deduped.append(c)
    return deduped


# Regex to extract platform-specific portal URLs from a homepage.
PLATFORM_PATTERNS: list[tuple[str, re.Pattern]] = [
    ("escribe",  re.compile(r"https?://[a-zA-Z0-9.-]*\.escribemeetings\.com/?[^\"' >]*", re.I)),
    ("civicweb", re.compile(r"https?://[a-zA-Z0-9.-]*\.civicweb\.net/?[^\"' >]*", re.I)),
    ("granicus", re.compile(r"https?://[a-zA-Z0-9.-]*\.granicus\.com/?[^\"' >]*", re.I)),
    ("legistar", re.compile(r"https?://[a-zA-Z0-9.-]+\.legistar\.com/?[^\"' >]*", re.I)),
    ("primegov", re.compile(r"https?://[a-zA-Z0-9.-]*\.primegov\.com/?[^\"' >]*", re.I)),
    ("youtube",  re.compile(r"https?://(?:www\.)?youtube\.com/(?:@[A-Za-z0-9._-]+|c/[A-Za-z0-9._-]+|user/[A-Za-z0-9._-]+|channel/UC[A-Za-z0-9_-]{22})", re.I)),
]


# Subpaths likely to contain links to the meeting platform / YouTube channel.
# After the homepage, we crawl these in order and merge their HTML text into
# one blob before grepping. Capped to avoid hammering tiny municipal sites.
_COUNCIL_SUBPATHS = [
    "/council",
    "/council-meetings",
    "/council/meetings",
    "/government",
    "/your-government",
    "/town-hall",
    "/agendas-and-minutes",
    "/agendas-minutes",
    "/agendas",
    "/meetings",
]


async def _try_host(client: httpx.AsyncClient, host: str) -> tuple[int, str | None]:
    """Issue a single HTTPS GET. Return (status, html-or-None).

    A connect error or non-200 returns (-1, None) so the caller can move
    on to the next candidate. We don't bother with HTTP/HTTP fallback —
    Alberta munis universally redirect to HTTPS.
    """
    url = f"https://{host}/"
    try:
        resp = await client.get(url, follow_redirects=True, timeout=12.0)
    except (httpx.HTTPError, OSError):
        return -1, None
    if resp.status_code != 200:
        return resp.status_code, None
    return 200, resp.text


async def _gather_council_html(
    client: httpx.AsyncClient, base_url: str, *, homepage_html: str,
) -> str:
    """Concatenate the homepage HTML with up to N council-related subpages.

    Returns one big string suitable for regex-grepping platform URLs.
    """
    blobs = [homepage_html]
    base = base_url.rstrip("/")
    # Scan the homepage for any council-related hrefs first; use them as
    # high-priority candidates before falling back to the static path list.
    href_candidates: list[str] = []
    for m in re.finditer(r'href="([^"]+)"', homepage_html):
        href = m.group(1)
        lower = href.lower()
        if any(k in lower for k in ("council", "agenda", "meeting", "government")):
            if href.startswith("/"):
                href_candidates.append(base + href)
            elif href.startswith("http"):
                # Only follow same-host links.
                if base in href:
                    href_candidates.append(href)
    seen: set[str] = set()
    targets = [
        u
        for u in (href_candidates + [base + p for p in _COUNCIL_SUBPATHS])
        if not (u in seen or seen.add(u))
    ][:6]

    for url in targets:
        try:
            r = await client.get(url, follow_redirects=True, timeout=10.0)
            if r.status_code == 200 and r.text:
                blobs.append(r.text)
        except (httpx.HTTPError, OSError):
            continue
    return "\n".join(blobs)


def _extract_links(html: str) -> dict[str, list[str]]:
    """For each known platform pattern, pull the unique URLs found."""
    out: dict[str, list[str]] = {}
    for name, pattern in PLATFORM_PATTERNS:
        hits = sorted(set(pattern.findall(html)))
        if hits:
            out[name] = hits[:5]  # cap noise
    return out


async def probe_one(
    client: httpx.AsyncClient, short_name: str, *, hint_url: str | None = None,
) -> dict:
    """Resolve a short_name to (website, platform_links).

    If ``hint_url`` is provided (already-known website from the seed), it is
    tried first. Otherwise candidate hosts are generated from the name and
    tried in order.
    """
    candidates: list[str] = []
    if hint_url:
        # Strip scheme/path to get the bare host so we run the same code path.
        m = re.match(r"https?://([^/]+)/?", hint_url)
        if m:
            candidates.append(m.group(1))
    candidates.extend(_candidate_hosts(short_name))

    found_url: str | None = None
    found_html: str | None = None
    for host in candidates:
        status, html = await _try_host(client, host)
        if status == 200 and html:
            found_url = f"https://{host}/"
            found_html = html
            break

    result: dict = {
        "short_name": short_name,
        "website_url": found_url,
        "candidates_tried": candidates,
        "platform_links": {},
    }
    if found_url and found_html:
        merged = await _gather_council_html(client, found_url, homepage_html=found_html)
        result["platform_links"] = _extract_links(merged)
    return result


async def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", default="/tmp/alberta-probe.json")
    parser.add_argument(
        "--start",
        type=int,
        default=None,
        help="Start index into the (sorted) AB roster.",
    )
    parser.add_argument(
        "--count",
        type=int,
        default=None,
        help="Number of munis to probe.",
    )
    parser.add_argument(
        "--short-name",
        default=None,
        help="Probe a single muni by short_name.",
    )
    parser.add_argument(
        "--include-phase-1",
        action="store_true",
        help="Also probe the 10 Phase 1 munis (skipped by default).",
    )
    parser.add_argument(
        "--concurrency",
        type=int,
        default=6,
        help="Parallel HTTP requests (default: 6 — be polite).",
    )
    args = parser.parse_args()

    phase_1 = list(ALBERTA_MUNICIPALITIES_PHASE_1)
    remainder = sorted(
        ALBERTA_MUNICIPALITIES_REMAINDER, key=lambda m: m["short_name"]
    )

    munis: list[dict]
    if args.short_name:
        candidate_pool: Iterable[dict] = phase_1 + remainder
        munis = [m for m in candidate_pool if m["short_name"] == args.short_name]
        if not munis:
            print(f"No AB municipality matches short_name {args.short_name!r}", file=sys.stderr)
            return 1
    else:
        munis = phase_1 + remainder if args.include_phase_1 else remainder
        if args.start is not None:
            munis = munis[args.start :]
        if args.count is not None:
            munis = munis[: args.count]

    sem = asyncio.Semaphore(args.concurrency)
    results: list[dict] = []

    async with httpx.AsyncClient(headers=HEADERS) as client:
        async def _go(m: dict) -> None:
            async with sem:
                hint = m.get("website_url")
                res = await probe_one(client, m["short_name"], hint_url=hint)
                results.append(res)
                # One-line progress so long runs stay observable.
                links = res["platform_links"]
                summary = ", ".join(f"{k}:{len(v)}" for k, v in links.items()) or "no platform links"
                print(
                    f"  {m['short_name']:35s} -> "
                    f"{res['website_url'] or '(no website)':50s} "
                    f"[{summary}]",
                    flush=True,
                )

        await asyncio.gather(*(_go(m) for m in munis))

    # Sort by short_name for stable diffs in the output JSON.
    results.sort(key=lambda r: r["short_name"])

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    found_website = sum(1 for r in results if r["website_url"])
    found_platform = sum(1 for r in results if r["platform_links"])
    print(
        f"\nProbed {len(results)} munis: "
        f"{found_website} websites resolved, "
        f"{found_platform} have platform links. "
        f"Report -> {args.out}",
    )
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
