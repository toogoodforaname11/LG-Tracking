#!/usr/bin/env python3
"""Validate all source URLs in the seed registry.

Fetches each URL, records HTTP status, checks for expected content patterns,
and outputs a CSV report.  Designed to be run manually before launch to
identify which scrapers actually reach live content.

Usage:
    cd backend
    python -m scripts.validate_sources [--timeout 15] [--concurrency 20] [--out report.csv]
"""

import argparse
import asyncio
import csv
import sys
import time
from dataclasses import dataclass, field

import httpx

# ---------------------------------------------------------------------------
# Import seed data
# ---------------------------------------------------------------------------

sys.path.insert(0, ".")

from app.services.seed_registry import (  # noqa: E402
    CRD_MUNICIPALITIES,
    BC_MUNICIPALITIES_BATCH_1,
    BC_MUNICIPALITIES_BATCH_2,
    BC_MUNICIPALITIES_BATCH_3,
    BC_MUNICIPALITIES_BATCH_4,
    BC_MUNICIPALITIES_BATCH_5,
    BC_MUNICIPALITIES_BATCH_6,
    BC_MUNICIPALITIES_BATCH_7,
    BC_MUNICIPALITIES_BATCH_8,
    BC_MUNICIPALITIES_BATCH_9,
    BC_MUNICIPALITIES_BATCH_10,
    BC_MUNICIPALITIES_BATCH_11,
    BC_MUNICIPALITIES_BATCH_12,
    BC_MUNICIPALITIES_BATCH_13,
    BC_MUNICIPALITIES_BATCH_14,
    BC_MUNICIPALITIES_BATCH_15,
    BC_MUNICIPALITIES_BATCH_16,
    BC_MUNICIPALITIES_BATCH_17,
)

ALL_MUNICIPALITIES = (
    CRD_MUNICIPALITIES
    + BC_MUNICIPALITIES_BATCH_1
    + BC_MUNICIPALITIES_BATCH_2
    + BC_MUNICIPALITIES_BATCH_3
    + BC_MUNICIPALITIES_BATCH_4
    + BC_MUNICIPALITIES_BATCH_5
    + BC_MUNICIPALITIES_BATCH_6
    + BC_MUNICIPALITIES_BATCH_7
    + BC_MUNICIPALITIES_BATCH_8
    + BC_MUNICIPALITIES_BATCH_9
    + BC_MUNICIPALITIES_BATCH_10
    + BC_MUNICIPALITIES_BATCH_11
    + BC_MUNICIPALITIES_BATCH_12
    + BC_MUNICIPALITIES_BATCH_13
    + BC_MUNICIPALITIES_BATCH_14
    + BC_MUNICIPALITIES_BATCH_15
    + BC_MUNICIPALITIES_BATCH_16
    + BC_MUNICIPALITIES_BATCH_17
)

# ---------------------------------------------------------------------------
# Content-pattern checks per platform
# ---------------------------------------------------------------------------

# If the response body contains any of these strings we consider the page
# "has expected content" for that platform.  Case-insensitive matching.
PLATFORM_CONTENT_MARKERS: dict[str, list[str]] = {
    "civicweb": ["civicweb", "meeting", "agenda", "minutes", "portal"],
    "granicus": ["granicus", "meeting", "agenda", "clip_id", "metaviewer"],
    "escribe": ["escribe", "meeting", "agenda", "minutes"],
    "youtube": ["youtube", "channel", "subscribe", "video"],
    "custom": ["agenda", "minutes", "council", "meeting", "bylaw"],
}


@dataclass
class ValidationResult:
    municipality: str
    platform: str
    source_type: str
    label: str
    url: str
    status_code: int = 0
    response_time_ms: int = 0
    has_expected_content: bool = False
    content_markers_found: list[str] = field(default_factory=list)
    error: str = ""
    verdict: str = ""  # OK, WARN, FAIL, ERROR


async def validate_one(
    muni_name: str,
    source: dict,
    client: httpx.AsyncClient,
    semaphore: asyncio.Semaphore,
) -> ValidationResult:
    """Fetch a single source URL and evaluate the response."""
    result = ValidationResult(
        municipality=muni_name,
        platform=source["platform"].value,
        source_type=source["source_type"].value,
        label=source["label"],
        url=source["url"],
    )

    async with semaphore:
        start = time.monotonic()
        try:
            resp = await client.get(source["url"], follow_redirects=True)
            result.status_code = resp.status_code
            result.response_time_ms = int((time.monotonic() - start) * 1000)

            if resp.status_code >= 400:
                result.verdict = "FAIL"
                result.error = f"HTTP {resp.status_code}"
                return result

            # Check for expected content
            body_lower = resp.text.lower()
            markers = PLATFORM_CONTENT_MARKERS.get(result.platform, [])
            result.content_markers_found = [m for m in markers if m in body_lower]
            result.has_expected_content = len(result.content_markers_found) > 0

            if result.has_expected_content:
                result.verdict = "OK"
            else:
                result.verdict = "WARN"
                result.error = "No expected content markers found"

        except httpx.TimeoutException:
            result.response_time_ms = int((time.monotonic() - start) * 1000)
            result.verdict = "ERROR"
            result.error = "Timeout"
        except httpx.ConnectError as exc:
            result.response_time_ms = int((time.monotonic() - start) * 1000)
            result.verdict = "ERROR"
            result.error = f"Connection error: {exc}"
        except Exception as exc:
            result.response_time_ms = int((time.monotonic() - start) * 1000)
            result.verdict = "ERROR"
            result.error = str(exc)[:200]

    return result


async def run_validation(
    timeout: int = 15,
    concurrency: int = 20,
) -> list[ValidationResult]:
    """Validate all source URLs concurrently."""
    semaphore = asyncio.Semaphore(concurrency)
    headers = {
        "User-Agent": "LGTracker/0.1 (source-validation script)",
    }

    async with httpx.AsyncClient(
        timeout=httpx.Timeout(timeout),
        headers=headers,
    ) as client:
        tasks = []
        for muni in ALL_MUNICIPALITIES:
            for source in muni["sources"]:
                tasks.append(
                    validate_one(muni["short_name"], source, client, semaphore)
                )

        results = await asyncio.gather(*tasks)

    return list(results)


def print_summary(results: list[ValidationResult]) -> None:
    """Print a human-readable summary to stderr."""
    from collections import Counter

    verdicts = Counter(r.verdict for r in results)
    print(f"\n{'='*60}", file=sys.stderr)
    print(f"Source URL Validation Report", file=sys.stderr)
    print(f"{'='*60}", file=sys.stderr)
    print(f"Total sources checked: {len(results)}", file=sys.stderr)
    for v in ["OK", "WARN", "FAIL", "ERROR"]:
        count = verdicts.get(v, 0)
        print(f"  {v:6s}: {count}", file=sys.stderr)

    # Platform breakdown
    print(f"\nBy platform:", file=sys.stderr)
    platforms = sorted({r.platform for r in results})
    for plat in platforms:
        plat_results = [r for r in results if r.platform == plat]
        plat_verdicts = Counter(r.verdict for r in plat_results)
        parts = ", ".join(f"{v}={plat_verdicts.get(v, 0)}" for v in ["OK", "WARN", "FAIL", "ERROR"])
        print(f"  {plat:10s} ({len(plat_results):3d}): {parts}", file=sys.stderr)

    # List failures and errors
    problems = [r for r in results if r.verdict in ("FAIL", "ERROR")]
    if problems:
        print(f"\nProblems ({len(problems)}):", file=sys.stderr)
        for r in sorted(problems, key=lambda x: x.municipality):
            print(
                f"  [{r.verdict}] {r.municipality} ({r.platform}/{r.source_type}): "
                f"{r.error} — {r.url}",
                file=sys.stderr,
            )

    # List warnings
    warnings = [r for r in results if r.verdict == "WARN"]
    if warnings:
        print(f"\nWarnings ({len(warnings)}):", file=sys.stderr)
        for r in sorted(warnings, key=lambda x: x.municipality):
            print(
                f"  [WARN] {r.municipality} ({r.platform}/{r.source_type}): "
                f"{r.error} — {r.url}",
                file=sys.stderr,
            )


def write_csv(results: list[ValidationResult], path: str) -> None:
    """Write results to CSV file."""
    fieldnames = [
        "municipality", "platform", "source_type", "label", "url",
        "status_code", "response_time_ms", "has_expected_content",
        "content_markers_found", "verdict", "error",
    ]
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in sorted(results, key=lambda x: (x.verdict != "OK", x.municipality)):
            writer.writerow({
                "municipality": r.municipality,
                "platform": r.platform,
                "source_type": r.source_type,
                "label": r.label,
                "url": r.url,
                "status_code": r.status_code,
                "response_time_ms": r.response_time_ms,
                "has_expected_content": r.has_expected_content,
                "content_markers_found": "|".join(r.content_markers_found),
                "verdict": r.verdict,
                "error": r.error,
            })
    print(f"\nCSV report written to: {path}", file=sys.stderr)


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate all seed registry source URLs")
    parser.add_argument("--timeout", type=int, default=15, help="Request timeout in seconds (default: 15)")
    parser.add_argument("--concurrency", type=int, default=20, help="Max concurrent requests (default: 20)")
    parser.add_argument("--out", type=str, default="source_validation_report.csv", help="Output CSV path")
    args = parser.parse_args()

    print(f"Validating {sum(len(m['sources']) for m in ALL_MUNICIPALITIES)} sources "
          f"across {len(ALL_MUNICIPALITIES)} municipalities...", file=sys.stderr)
    print(f"Timeout: {args.timeout}s, Concurrency: {args.concurrency}", file=sys.stderr)

    results = asyncio.run(run_validation(timeout=args.timeout, concurrency=args.concurrency))
    print_summary(results)
    write_csv(results, args.out)


if __name__ == "__main__":
    main()
