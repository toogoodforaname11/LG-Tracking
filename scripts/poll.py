#!/usr/bin/env python3
"""Run the discovery poller for one municipality (or all of them) from the CLI.

Usage:
    python3 scripts/poll.py                       # poll every active source
    python3 scripts/poll.py "Calgary"             # poll just Calgary
    python3 scripts/poll.py --province Alberta    # poll every Alberta muni

Useful for ops during phased Alberta rollout — verifying scrapers work
against real portals without relying on the cron HTTP endpoint (which is
locked behind ``CRON_SECRET``). Output is one line per source so the result
is easy to grep.

Requires ``DATABASE_URL`` in ``backend/.env`` (or the environment), same
as ``scripts/seed.py``.
"""

import argparse
import asyncio
import json
import os
import sys

# Ensure the backend package is importable.
backend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "backend")
sys.path.insert(0, backend_dir)

# Change to backend dir so pydantic-settings finds .env.
os.chdir(backend_dir)

from sqlalchemy import select  # noqa: E402

from app.db.database import async_session  # noqa: E402
from app.discovery.poller import run_discovery  # noqa: E402
from app.models.municipality import Municipality, PROVINCE_BC, VALID_PROVINCES  # noqa: E402


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run discovery for one or more municipalities.")
    parser.add_argument(
        "municipality",
        nargs="?",
        default=None,
        help="short_name to poll (e.g. 'Calgary'). Omit to poll all matching munis.",
    )
    parser.add_argument(
        "--province",
        choices=sorted(VALID_PROVINCES),
        default=None,
        help="Restrict polling to one province. Defaults to no province filter.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit the per-source results as a single JSON document.",
    )
    return parser.parse_args()


async def _poll_each(province: str | None, municipality: str | None) -> dict:
    """Run discovery for every muni matching ``province``/``municipality``.

    Calling ``run_discovery`` once with a single ``municipality_filter`` is
    sufficient for the single-muni case. For the bulk-by-province case we
    iterate over the matched ``short_name`` list so per-muni progress is
    visible in the output.
    """
    aggregated: dict = {}

    async with async_session() as session:
        if municipality is not None:
            print(f"Polling {municipality}...", flush=True)
            results = await run_discovery(session, municipality_filter=municipality)
            aggregated.update(results)
            return aggregated

        # No specific muni — pick all that match the province filter.
        query = select(Municipality.short_name).where(Municipality.is_active.is_(True))
        if province is not None:
            query = query.where(Municipality.province == province)
        query = query.order_by(Municipality.short_name)

        result = await session.execute(query)
        names = list(result.scalars().all())
        if not names:
            print("No municipalities matched the filter; nothing to poll.")
            return aggregated

        print(f"Polling {len(names)} municipalities...", flush=True)
        for name in names:
            print(f"  -> {name}", flush=True)
            sub_results = await run_discovery(session, municipality_filter=name)
            aggregated.update(sub_results)

    return aggregated


def _format_human(results: dict) -> str:
    """Format ``run_discovery`` output as human-readable lines."""
    if not results:
        return "(no sources polled)"

    lines: list[str] = []
    for key, value in sorted(results.items()):
        if key.startswith("_"):
            # Synthetic keys like "_immediate_alerts" — print verbatim.
            lines.append(f"{key}: {value}")
            continue
        if isinstance(value, dict) and "error" in value:
            lines.append(f"  ✗ {key}: error: {value['error']}")
        elif isinstance(value, dict):
            total = value.get("total", 0)
            new = value.get("new", 0)
            updated = value.get("updated", 0)
            lines.append(
                f"  ✓ {key}: total={total} new={new} updated={updated}"
            )
        else:
            lines.append(f"  ? {key}: {value}")
    return "\n".join(lines)


async def main() -> int:
    args = _parse_args()
    results = await _poll_each(args.province, args.municipality)

    if args.json:
        print(json.dumps(results, default=str, indent=2))
    else:
        print(_format_human(results))

    # Exit non-zero if any source errored — useful for CI / ops scripting.
    error_count = sum(
        1
        for k, v in results.items()
        if not k.startswith("_") and isinstance(v, dict) and "error" in v
    )
    return 1 if error_count else 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
