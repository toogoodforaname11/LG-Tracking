"""Invariants for the Ontario seed roster.

Mirrors the Alberta seed invariants in tests/test_seed.py — see that file
for the rationale (per-province uniqueness, tier sanity, Phase-1 has full
ACTIVE configs, etc.).
"""

from collections import Counter

from app.models.municipality import (
    PROVINCE_ON,
    ScrapeStatus,
    TIER_LOWER,
    TIER_SINGLE,
    TIER_UPPER,
    VALID_TIERS,
)
from app.services.seed_registry import (
    ONTARIO_MUNICIPALITIES_PHASE_1,
    ONTARIO_MUNICIPALITIES_REMAINDER,
)


ALL_ON = ONTARIO_MUNICIPALITIES_PHASE_1 + ONTARIO_MUNICIPALITIES_REMAINDER


def test_phase_1_has_ten_entries():
    assert len(ONTARIO_MUNICIPALITIES_PHASE_1) == 10


def test_phase_1_includes_required_cities():
    """Toronto, Ottawa and Hamilton must always be in Phase 1 — anything
    less and the rollout doc is lying about scope."""
    short_names = {m["short_name"] for m in ONTARIO_MUNICIPALITIES_PHASE_1}
    for required in ("Toronto", "Ottawa", "Mississauga", "Hamilton", "London"):
        assert required in short_names, (
            f"Phase 1 must include {required!r}, got {sorted(short_names)}"
        )


def test_every_on_entry_tagged_province_ontario():
    for muni in ALL_ON:
        assert muni["province"] == PROVINCE_ON, (
            f"ON entry {muni['short_name']!r} has wrong province {muni['province']!r}"
        )


def test_every_on_entry_has_valid_tier():
    for muni in ALL_ON:
        tier = muni.get("tier")
        assert tier in VALID_TIERS, (
            f"ON entry {muni['short_name']!r} has invalid tier {tier!r}"
        )


def test_no_short_name_collisions_within_ontario():
    names = [m["short_name"] for m in ALL_ON]
    dupes = {n: c for n, c in Counter(names).items() if c > 1}
    assert not dupes, f"Duplicate ON short_names: {dupes}"


def test_phase_1_munis_have_at_least_one_active_source():
    """Toronto's portal source ships PENDING (ON-001), but every Phase 1
    muni still has YouTube as ACTIVE so we get *some* coverage on day 1.
    """
    for muni in ONTARIO_MUNICIPALITIES_PHASE_1:
        active_sources = [
            s for s in muni["sources"] if s["scrape_status"] == ScrapeStatus.ACTIVE
        ]
        assert active_sources, (
            f"Phase 1 muni {muni['short_name']!r} has no ACTIVE sources"
        )


def test_upper_tier_munis_present():
    """The 8 regional municipalities must all show up as upper-tier."""
    upper = {
        m["short_name"]
        for m in ALL_ON
        if m["tier"] == TIER_UPPER
    }
    for region in (
        "Durham Region",
        "Halton Region",
        "Niagara Region",
        "Peel Region",
        "Waterloo Region",
        "York Region",
    ):
        assert region in upper, f"Missing upper-tier {region!r} (got {sorted(upper)})"


def test_total_on_count_above_330():
    """Sanity floor — we seed at least 330 ON munis."""
    unique = {m["short_name"] for m in ALL_ON}
    assert len(unique) >= 330, f"Expected ≥330 ON munis, got {len(unique)}"
