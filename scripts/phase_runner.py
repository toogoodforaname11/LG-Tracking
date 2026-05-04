#!/usr/bin/env python3
"""Run one rollout phase: pick the next 10 AB munis, re-seed, poll, summarize.

Usage:
    SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt scripts/phase_runner.py 2

Picks munis ``(phase-2)*10 .. (phase-2)*10+9`` from the *alphabetical* AB
remainder roster (Phase 1 — the 10 large cities — is skipped). Re-seeds the
DB, polls each muni via ``run_discovery(municipality_filter=...)``, prints a
markdown table snippet that can be appended to
``docs/alberta-rollout-tracker.md``.

This script is **idempotent** — running phase N twice yields the same DB
state and the same markdown output (modulo timestamps).
"""

import argparse
import asyncio
import json
import os
import sys
from datetime import datetime, timezone

backend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "backend")
sys.path.insert(0, backend_dir)
os.chdir(backend_dir)

from sqlalchemy import select  # noqa: E402

from app.db.database import async_session  # noqa: E402
from app.discovery.poller import run_discovery  # noqa: E402
from app.models.municipality import (  # noqa: E402
    Municipality,
    Platform,
    ScrapeStatus,
)
from app.services.seed_registry import (  # noqa: E402
    ALBERTA_MUNICIPALITIES_REMAINDER,
    ONTARIO_MUNICIPALITIES_REMAINDER,
    seed_registry,
)


PHASE_SIZE = 10


def _remainder_for(province: str) -> list[dict]:
    if province == "Alberta":
        return list(ALBERTA_MUNICIPALITIES_REMAINDER)
    if province == "Ontario":
        return list(ONTARIO_MUNICIPALITIES_REMAINDER)
    raise SystemExit(f"Unknown province {province!r} for phase_runner")


def _select_phase_munis(phase: int, province: str) -> list[dict]:
    """Slice the alphabetical remainder roster for the given phase number.

    Phase 2 covers indexes 0..9, phase 3 covers 10..19, etc.
    """
    if phase < 2:
        raise SystemExit(
            f"Phase {phase} doesn't exist — Phase 1 was the 10 large cities, "
            "subsequent phases iterate the remainder roster starting at phase 2."
        )
    sorted_remainder = sorted(_remainder_for(province), key=lambda m: m["short_name"])
    start = (phase - 2) * PHASE_SIZE
    if start >= len(sorted_remainder):
        return []
    return sorted_remainder[start : start + PHASE_SIZE]


async def _ensure_seeded(session) -> None:
    """Re-run the registry seeder (idempotent) so any new patches land."""
    await seed_registry(session)


def _summarize(
    short_name: str, results: dict, *, is_patched: bool,
) -> tuple[str, int, int]:
    """Return (status_label, total_items, active_sources_run) for one muni.

    Status labels:
        VALIDATED  — at least one source returned items today
        READY      — patched muni; sources reachable but zero items today
        PLACEHOLDER— still using the AB directory placeholder URL
        BROKEN     — at least one source returned an exception
        UNREACHED  — poller didn't touch any of this muni's sources
    """
    keys = [k for k in results if k.startswith(f"{short_name}/")]
    if not keys:
        return "UNREACHED", 0, 0
    total = sum(
        v.get("total", 0)
        for k, v in results.items()
        if k.startswith(f"{short_name}/") and isinstance(v, dict) and "error" not in v
    )
    error_count = sum(
        1
        for k, v in results.items()
        if k.startswith(f"{short_name}/") and isinstance(v, dict) and "error" in v
    )
    if error_count:
        return "BROKEN", total, len(keys)
    if total > 0:
        return "VALIDATED", total, len(keys)
    if not is_patched:
        return "PLACEHOLDER", 0, len(keys)
    return "READY", 0, len(keys)


def _is_patched(muni: dict) -> bool:
    """A muni is 'patched' when the seed_registry has at least one ACTIVE
    source pointing at a real portal URL (i.e. not the AB-directory
    placeholder).
    """
    placeholder_substr = "alberta.ca/find-a-municipal-official"
    for s in muni["sources"]:
        if placeholder_substr in s["url"]:
            continue
        if isinstance(s["scrape_status"], ScrapeStatus):
            if s["scrape_status"] == ScrapeStatus.ACTIVE:
                return True
        elif s["scrape_status"] == "active":
            return True
    return False


def _platform_label(muni: dict) -> str:
    """Human-readable platform label for the tracker row."""
    plats = []
    for s in muni["sources"]:
        p = s["platform"]
        st = s["scrape_status"]
        if isinstance(p, Platform):
            p = p.value
        if isinstance(st, ScrapeStatus):
            st = st.value
        if st == "pending":
            plats.append(f"{p}*")
        else:
            plats.append(p)
    seen = []
    for p in plats:
        if p not in seen:
            seen.append(p)
    return " + ".join(seen) or "placeholder"


async def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("phase", type=int)
    parser.add_argument(
        "--province",
        choices=("Alberta", "Ontario"),
        default="Alberta",
        help="Which province's remainder roster to slice (default: Alberta).",
    )
    parser.add_argument(
        "--out",
        default=None,
        help="Append the markdown summary to this file. Stdout if omitted.",
    )
    args = parser.parse_args()

    munis = _select_phase_munis(args.phase, args.province)
    if not munis:
        print(f"[{args.province}] Phase {args.phase}: no more municipalities to roll out.")
        return 0

    short_names = [m["short_name"] for m in munis]
    print(
        f"[{args.province}] Phase {args.phase}: {len(munis)} munis -> "
        f"{', '.join(short_names)}",
        flush=True,
    )

    async with async_session() as session:
        # 1. Make sure these munis exist in the DB (re-seed picks up any
        #    newly-patched probe URLs).
        await _ensure_seeded(session)

        # 2. Poll each one and aggregate the results.
        per_muni_results: dict[str, dict] = {}
        for short in short_names:
            print(f"  -> polling {short}", flush=True)
            try:
                results = await run_discovery(session, municipality_filter=short)
            except Exception as e:  # noqa: BLE001
                print(f"     !! {short} raised: {e}")
                results = {f"{short}/__exception__": {"error": str(e)}}
            per_muni_results[short] = results

    # 3. Render markdown table.
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    lines = [
        f"### Phase {args.phase} ({len(munis)} munis — {today})",
        "",
        "| Municipality | Sources | Platform | Status | Items | Notes |",
        "|---|---:|---|---|---:|---|",
    ]
    for muni in munis:
        short = muni["short_name"]
        status, total, src_count = _summarize(
            short, per_muni_results[short], is_patched=_is_patched(muni)
        )
        platform_label = _platform_label(muni)
        notes = ""
        if status == "READY":
            notes = "URLs resolve, no items today"
        elif status == "PLACEHOLDER":
            notes = "no portal discovered yet"
        elif status == "VALIDATED":
            notes = f"{total} items"
        elif status == "BROKEN":
            errors = [
                v.get("error")
                for k, v in per_muni_results[short].items()
                if isinstance(v, dict) and "error" in v
            ]
            notes = "; ".join(filter(None, errors))[:80]
        lines.append(
            f"| {short} | {len(muni['sources'])} | {platform_label} | "
            f"{status} | {total} | {notes} |"
        )
    lines.append("")

    output = "\n".join(lines)

    if args.out:
        with open(args.out, "a", encoding="utf-8") as f:
            f.write("\n" + output)
        print(f"Appended phase {args.phase} table to {args.out}")
    else:
        print()
        print(output)

    # Also dump raw poll output for debugging.
    debug_path = f"/tmp/ab-phase-{args.phase}.json"
    with open(debug_path, "w", encoding="utf-8") as f:
        json.dump(per_muni_results, f, indent=2, default=str)
    print(f"Per-source poll results -> {debug_path}")

    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
