#!/usr/bin/env python3
"""Translate the AB probe report into a Python patches file.

Reads ``docs/alberta-probe-report.json`` (or whatever path is given via
``--in``) and writes ``backend/app/services/_ab_remainder_patches.py``
containing a ``REMAINDER_PATCHES`` dict::

    {
        "Banff": {
            "website_url": "https://www.banff.ca/",
            "sources": [...],
        },
        ...
    }

``seed_registry`` imports the dict and merges it onto the
``ALBERTA_MUNICIPALITIES_REMAINDER`` placeholder entries before seeding.

Reasoning per platform:
- **CivicWeb / eSCRIBE / Granicus / Legistar**: the probe gives us the real
  portal URL; emit a single ACTIVE source per portal so the existing
  scrapers pick it up.
- **YouTube** (handle/channel link found on the muni site): emit an ACTIVE
  YouTube source with the discovered URL — the resolver lazily converts
  it to a UCxxx and caches the result in scrape_config.
- **No platform link, no website**: keep the placeholder PENDING source.
- **Website found but no platform link**: bump the placeholder URL to the
  real website (so the muni's website_url is correct) but leave the
  scraper-config PENDING.

This script is idempotent — running it twice produces byte-identical
output (the dict is sorted by short_name).
"""

import argparse
import json
import os
import re
import sys
import textwrap
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parent
DEFAULT_IN_BY_PROVINCE = {
    "Alberta": REPO_ROOT / "docs" / "alberta-probe-report.json",
    "Ontario": REPO_ROOT / "docs" / "ontario-probe-report.json",
}
DEFAULT_OUT_BY_PROVINCE = {
    "Alberta": REPO_ROOT / "backend" / "app" / "services" / "_ab_remainder_patches.py",
    "Ontario": REPO_ROOT / "backend" / "app" / "services" / "_on_remainder_patches.py",
}


# Map probe-platform-key -> seed enum value (Platform.X) we'll emit as a
# string-form reference. The seed module re-imports and resolves these.
PLATFORM_TO_ENUM = {
    "civicweb": "Platform.CIVICWEB",
    "escribe": "Platform.ESCRIBE",
    "granicus": "Platform.GRANICUS",
    "legistar": "Platform.CUSTOM",   # no Platform.LEGISTAR yet (issue AB-008)
    "primegov": "Platform.CUSTOM",
    "youtube": "Platform.YOUTUBE",
}


def _normalize_url(url: str) -> str:
    """Trim trailing junk eSCRIBE / CivicWeb URLs sometimes carry."""
    # Strip query-string fluff and trailing punctuation injected by surrounding HTML.
    url = url.split("\\")[0]
    url = url.rstrip("\"'.,;:>) ")
    return url


def _pick_best(urls: list[str], platform: str) -> str | None:
    """Pick the canonical URL for a platform from the probe result list."""
    if not urls:
        return None
    cleaned = [_normalize_url(u) for u in urls]
    if platform in {"civicweb", "escribe"}:
        # Prefer ``https://<host>/`` — the scraper appends paths itself.
        roots = [u for u in cleaned if "/Portal/" in u or u.count("/") <= 3]
        if roots:
            # Strip path so we use the root host. The scraper hits Portal subpaths.
            m = re.match(r"(https?://[^/]+)", roots[0])
            if m:
                return m.group(1)
        return _normalize_url(cleaned[0])
    if platform == "youtube":
        # Prefer @handle URLs — they survive renames better than channel/UC ids,
        # but the resolver handles both.
        handle = [u for u in cleaned if "/@" in u]
        if handle:
            return handle[0]
        chan = [u for u in cleaned if "/channel/UC" in u]
        if chan:
            return chan[0]
        return cleaned[0]
    return cleaned[0]


def build_patches(probe: list[dict]) -> dict:
    """Produce ``{short_name: patch_dict}`` from the probe results."""
    patches: dict[str, dict] = {}

    for entry in probe:
        name = entry["short_name"]
        website = entry.get("website_url")
        platform_links = entry.get("platform_links") or {}

        if not website and not platform_links:
            # Nothing useful — leave the placeholder alone.
            continue

        sources: list[dict] = []
        # Order matters in the seed (first ACTIVE wins for "primary platform"
        # in the tracker). Emit doc platforms first, YouTube last.
        for plat in ("civicweb", "escribe", "granicus", "legistar", "primegov"):
            urls = platform_links.get(plat) or []
            best = _pick_best(urls, plat)
            if not best:
                continue
            sources.append({
                "platform": PLATFORM_TO_ENUM[plat],
                "source_type": "SourceType.AGENDA",
                "url": best,
                "label": f"{name} {plat.capitalize()} Portal",
                "scrape_status": "ScrapeStatus.ACTIVE" if plat != "legistar" else "ScrapeStatus.PENDING",
            })
        yt = _pick_best(platform_links.get("youtube") or [], "youtube")
        if yt:
            sources.append({
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": yt,
                "label": f"{name} YouTube",
                "scrape_status": "ScrapeStatus.ACTIVE",
            })

        patches[name] = {
            "website_url": website,
            "sources": sources,
        }

    return patches


def render_python(patches: dict) -> str:
    """Render the patches dict as a Python module string."""
    lines: list[str] = [
        '"""Auto-generated from docs/alberta-probe-report.json by',
        '``scripts/apply_alberta_probe.py``. Do not edit by hand —',
        're-run the script if the probe report changes."""',
        "",
        "# Strings reference Platform / SourceType / ScrapeStatus enum values",
        "# defined in app.models.municipality. seed_registry resolves them at",
        "# import time so this module stays free of model-side dependencies.",
        "",
        "REMAINDER_PATCHES: dict = {",
    ]
    for name in sorted(patches.keys()):
        patch = patches[name]
        lines.append(f"    {name!r}: {{")
        lines.append(f"        \"website_url\": {patch['website_url']!r},")
        lines.append(f"        \"sources\": [")
        for s in patch["sources"]:
            lines.append("            {")
            lines.append(f"                \"platform\": \"{s['platform']}\",")
            lines.append(f"                \"source_type\": \"{s['source_type']}\",")
            lines.append(f"                \"url\": {s['url']!r},")
            lines.append(f"                \"label\": {s['label']!r},")
            lines.append(f"                \"scrape_status\": \"{s['scrape_status']}\",")
            lines.append("            },")
        lines.append("        ],")
        lines.append("    },")
    lines.append("}")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--province", choices=("Alberta", "Ontario"), default="Alberta",
        help="Which province's probe report to process (default: Alberta).",
    )
    parser.add_argument("--in", dest="in_path", default=None)
    parser.add_argument("--out", dest="out_path", default=None)
    args = parser.parse_args()

    in_path = Path(args.in_path) if args.in_path else DEFAULT_IN_BY_PROVINCE[args.province]
    out_path = Path(args.out_path) if args.out_path else DEFAULT_OUT_BY_PROVINCE[args.province]

    probe = json.loads(in_path.read_text(encoding="utf-8"))
    patches = build_patches(probe)
    text = render_python(patches)
    out_path.write_text(text, encoding="utf-8")
    print(f"[{args.province}] Wrote {len(patches)} patches to {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
