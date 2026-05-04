"""Invariant test: every Alberta muni in the seed appears in the tracker.

If a future change adds an AB municipality to the seed without adding it to
``docs/alberta-rollout-tracker.md`` we want CI to fail loudly. The tracker
is the source of truth for rollout status, and silent gaps would bypass the
"do not miss any municipality" guarantee.

Tracker rows look like::

    | <short_name> | <n> | <plat> | VALIDATED | <items> | <notes> |

for phases 2..N (the runner output) and like::

    | 1 | Calgary | 1 | 2 | eSCRIBE + YouTube | VALIDATED | 2026-05-04 | ... |

for the Phase 1 hand-written sub-table. Both are matched via tolerant
regexes here so the test isn't tied to one specific layout.
"""

import re
from pathlib import Path

from app.services.seed_registry import (
    ALBERTA_MUNICIPALITIES_PHASE_1,
    ALBERTA_MUNICIPALITIES_REMAINDER,
)


REPO_ROOT = Path(__file__).resolve().parents[2]
TRACKER_PATH = REPO_ROOT / "docs" / "alberta-rollout-tracker.md"


def _tracker_short_names() -> set[str]:
    """Pull every short_name that appears in any tracker validation table."""
    if not TRACKER_PATH.exists():
        return set()
    text = TRACKER_PATH.read_text(encoding="utf-8")

    found: set[str] = set()
    # Phase 1 row format (variable spacing):
    # | 1 | Calgary | 1 | 2 | eSCRIBE + YouTube | VALIDATED | 2026-05-04 | notes |
    # Match rows where the first cell is a small integer (phase index 1..30).
    for m in re.finditer(
        r"^\|\s+\d+\s+\|\s+([^|]+?)\s+\|\s+\d+\s+\|\s+\d+\s+\|", text, re.M
    ):
        found.add(m.group(1).strip())
    # Phase 2+ row format (phase_runner.py output):
    # | <short_name> | <n_sources> | <platform> | <STATUS> | <items> | <notes> |
    for m in re.finditer(
        r"^\|\s+([A-Z][^|]+?)\s+\|\s+\d+\s+\|[^|]+\|\s+(?:VALIDATED|READY|PLACEHOLDER|BROKEN|UNREACHED|DEMOTED)\s+\|",
        text,
        re.M,
    ):
        found.add(m.group(1).strip())
    return found


# Map of seed short_names to friendlier labels used in the hand-curated
# Phase 1 sub-table. Keep this small and obvious so reviewers can spot
# typos vs. legitimate aliases.
TRACKER_ALIASES = {
    "Fort McMurray": {"Fort McMurray", "Fort McMurray (RMWB)"},
}


def _tracker_known_for(short_name: str, found: set[str]) -> bool:
    if short_name in found:
        return True
    for alias in TRACKER_ALIASES.get(short_name, set()):
        if alias in found:
            return True
    return False


def test_tracker_covers_every_alberta_municipality():
    expected = {
        m["short_name"]
        for m in ALBERTA_MUNICIPALITIES_PHASE_1 + ALBERTA_MUNICIPALITIES_REMAINDER
    }
    found = _tracker_short_names()
    missing = sorted(n for n in expected if not _tracker_known_for(n, found))
    assert not missing, (
        f"{len(missing)} Alberta municipalities are in the seed but not the tracker: "
        f"{missing[:20]}"
    )


def test_tracker_has_no_unknown_short_names():
    """Reverse direction: every name in the tracker must come from the seed.

    Catches typos like 'Caglary' that would otherwise slip past review.
    """
    expected = {
        m["short_name"]
        for m in ALBERTA_MUNICIPALITIES_PHASE_1 + ALBERTA_MUNICIPALITIES_REMAINDER
    }
    # The tracker also references some non-muni labels like 'Phase 1' in
    # narrative tables; restrict the diff to the validation rows we care
    # about. Allowlist names that show up in the tracker as illustrative
    # but aren't seeded — none today, but reserve the slot.
    allow: set[str] = set()
    # Friendly labels used in the Phase 1 sub-table that map to seed names
    # via TRACKER_ALIASES — admit them so the test isn't tautologically failed
    # by its own alias map.
    for aliases in TRACKER_ALIASES.values():
        allow.update(aliases)
    found = _tracker_short_names()
    extra = found - expected - allow
    assert not extra, (
        f"Tracker references {len(extra)} short_names not present in the seed: "
        f"{sorted(extra)[:20]}"
    )
