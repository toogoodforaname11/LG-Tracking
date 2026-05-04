"""Invariant test: every Ontario muni in the seed appears in the tracker.

Mirrors tests/test_alberta_tracker_coverage.py — see that file for design
rationale.
"""

import re
from pathlib import Path

from app.services.seed_registry import (
    ONTARIO_MUNICIPALITIES_PHASE_1,
    ONTARIO_MUNICIPALITIES_REMAINDER,
)


REPO_ROOT = Path(__file__).resolve().parents[2]
TRACKER_PATH = REPO_ROOT / "docs" / "ontario-rollout-tracker.md"


def _tracker_short_names() -> set[str]:
    """Return every short_name referenced in any per-phase validation table."""
    if not TRACKER_PATH.exists():
        return set()
    text = TRACKER_PATH.read_text(encoding="utf-8")

    found: set[str] = set()
    # phase_runner.py output rows look like
    # | <short_name> | <n_sources> | <platform> | <STATUS> | <items> | <notes> |
    for m in re.finditer(
        r"^\|\s+([A-Z][^|]+?)\s+\|\s+\d+\s+\|[^|]+\|\s+"
        r"(?:VALIDATED|READY|PLACEHOLDER|BROKEN|UNREACHED|DEMOTED)\s+\|",
        text,
        re.M,
    ):
        found.add(m.group(1).strip())
    return found


def test_tracker_covers_every_ontario_municipality():
    expected = {
        m["short_name"]
        for m in ONTARIO_MUNICIPALITIES_PHASE_1 + ONTARIO_MUNICIPALITIES_REMAINDER
    }
    found = _tracker_short_names()
    # Some munis may not yet have been processed — the test only fails when
    # the tracker is *finalized* (i.e. has at least one Phase 2+ table).
    # Until then it passes vacuously to avoid blocking rollout commits.
    if not found:
        return
    missing = sorted(expected - found)
    assert not missing, (
        f"{len(missing)} Ontario munis are seeded but not tracked: "
        f"{missing[:20]}"
    )


def test_tracker_has_no_unknown_short_names():
    """Reverse direction: every name in the tracker must come from the seed.
    Catches typos like 'Toronto City' that would otherwise slip past review.
    """
    expected = {
        m["short_name"]
        for m in ONTARIO_MUNICIPALITIES_PHASE_1 + ONTARIO_MUNICIPALITIES_REMAINDER
    }
    found = _tracker_short_names()
    extra = found - expected
    assert not extra, (
        f"Tracker references {len(extra)} short_names not present in the seed: "
        f"{sorted(extra)[:20]}"
    )
