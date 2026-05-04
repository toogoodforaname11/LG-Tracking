"""Test seed registry data integrity — all BC + Alberta municipalities."""

from app.models.municipality import Platform, PROVINCE_BC, PROVINCE_AB
from app.services.seed_registry import (
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
    ALBERTA_MUNICIPALITIES_PHASE_1,
    ALBERTA_MUNICIPALITIES_REMAINDER,
    BC_BATCHES,
    AB_BATCHES,
)
from app.discovery.poller import CUSTOM_SCRAPER_MAP
from app.discovery.custom_bc_municipal import GENERIC_SCRAPER_KEYWORDS


BC_ONLY_MUNICIPALITIES = [m for batch in BC_BATCHES for m in batch]
AB_ONLY_MUNICIPALITIES = [m for batch in AB_BATCHES for m in batch]
ALL_MUNICIPALITIES = BC_ONLY_MUNICIPALITIES + AB_ONLY_MUNICIPALITIES


# --- CRD-specific tests (preserved from original) ---


def test_crd_municipality_count():
    """Should have 14 entries: 13 municipalities + CRD board."""
    assert len(CRD_MUNICIPALITIES) == 14


def test_colwood_is_first():
    """Colwood is our primary target and should be first."""
    assert CRD_MUNICIPALITIES[0]["short_name"] == "Colwood"


def test_colwood_has_three_sources():
    colwood = CRD_MUNICIPALITIES[0]
    assert len(colwood["sources"]) == 3  # CivicWeb agenda, minutes, YouTube


# --- Full registry tests ---


def test_all_municipalities_have_required_fields():
    """Every municipality must have name, short_name, gov_type, and at least one source."""
    for muni in ALL_MUNICIPALITIES:
        assert "name" in muni, f"Missing 'name' in: {muni}"
        assert "short_name" in muni, f"Missing 'short_name' in: {muni}"
        assert "gov_type" in muni, f"Missing 'gov_type' in: {muni}"
        assert "sources" in muni, f"Missing 'sources' in: {muni.get('short_name', '?')}"
        assert len(muni["sources"]) > 0, f"{muni['short_name']} has no sources"


def test_all_sources_have_required_fields():
    """Every source must have platform, source_type, url, label, and scrape_status."""
    for muni in ALL_MUNICIPALITIES:
        for source in muni["sources"]:
            for field in ("platform", "source_type", "url", "label", "scrape_status"):
                assert field in source, (
                    f"{muni['short_name']} source missing '{field}': {source}"
                )


def test_no_duplicate_short_names_within_crd():
    """CRD list must not contain duplicates."""
    names = [m["short_name"] for m in CRD_MUNICIPALITIES]
    assert len(names) == len(set(names)), f"CRD duplicates: {names}"


def test_civicweb_sources_have_valid_urls():
    """All CivicWeb sources must point to a civicweb.net domain."""
    for muni in ALL_MUNICIPALITIES:
        for source in muni["sources"]:
            if source["platform"] == Platform.CIVICWEB:
                assert "civicweb.net" in source["url"], (
                    f"{muni['short_name']} CivicWeb source has bad URL: {source['url']}"
                )


def test_youtube_sources_have_valid_urls():
    """YouTube sources must point to youtube.com."""
    for muni in ALL_MUNICIPALITIES:
        for source in muni["sources"]:
            if source["platform"] == Platform.YOUTUBE:
                assert "youtube.com" in source["url"], (
                    f"{muni['short_name']} YouTube source has bad URL: {source['url']}"
                )


def test_custom_scraper_map_covers_all_bc_custom_sources():
    """Every BC municipality with a CUSTOM platform source must have either a
    CUSTOM_SCRAPER_MAP entry (substantive) or a GENERIC_SCRAPER_KEYWORDS entry.

    Alberta munis are excluded because their PENDING placeholder sources are
    intentionally not yet wired to scrapers — that's the next phase of work.
    """
    missing = []
    seen = set()
    for muni in BC_ONLY_MUNICIPALITIES:
        short = muni["short_name"]
        if short in seen:
            continue
        seen.add(short)
        has_custom = any(s["platform"] == Platform.CUSTOM for s in muni["sources"])
        if has_custom and short not in CUSTOM_SCRAPER_MAP and short not in GENERIC_SCRAPER_KEYWORDS:
            missing.append(short)

    assert not missing, (
        f"BC municipalities with CUSTOM sources but no scraper config: {missing}"
    )


def test_total_municipality_count():
    """Sanity check: registry should have at least 160 BC + 280 AB entries."""
    bc_names = {m["short_name"] for m in BC_ONLY_MUNICIPALITIES}
    ab_names = {m["short_name"] for m in AB_ONLY_MUNICIPALITIES}
    assert len(bc_names) >= 160, (
        f"Expected at least 160 unique BC municipalities, got {len(bc_names)}"
    )
    assert len(ab_names) >= 280, (
        f"Expected at least 280 unique Alberta municipalities, got {len(ab_names)}"
    )


def test_no_duplicate_short_names_within_each_province():
    """short_name must be unique within a province (matches the DB UNIQUE).

    Cross-province duplicates ARE allowed (e.g. Lacombe exists in both BC and
    AB lists per the product spec) since the DB unique constraint is on
    ``(short_name, province)``.
    """
    from collections import Counter

    bc_names = [m["short_name"] for m in BC_ONLY_MUNICIPALITIES]
    bc_dupes = {n: c for n, c in Counter(bc_names).items() if c > 1}
    assert not bc_dupes, f"Duplicate BC short_names: {bc_dupes}"

    ab_names = [m["short_name"] for m in AB_ONLY_MUNICIPALITIES]
    ab_dupes = {n: c for n, c in Counter(ab_names).items() if c > 1}
    assert not ab_dupes, f"Duplicate AB short_names: {ab_dupes}"


def test_all_source_urls_are_nonempty():
    """No source should have an empty or whitespace-only URL."""
    for muni in ALL_MUNICIPALITIES:
        for source in muni["sources"]:
            assert source["url"].strip(), (
                f"{muni['short_name']} has empty URL in source: {source['label']}"
            )


# --- Alberta-specific tests ---


def test_alberta_phase_1_has_ten_entries():
    """Phase 1 ships exactly 10 fully-configured Alberta municipalities."""
    assert len(ALBERTA_MUNICIPALITIES_PHASE_1) == 10


def test_alberta_phase_1_includes_calgary_and_edmonton():
    """Calgary and Edmonton must be in Phase 1 (highest population)."""
    short_names = {m["short_name"] for m in ALBERTA_MUNICIPALITIES_PHASE_1}
    assert "Calgary" in short_names
    assert "Edmonton" in short_names


def test_all_alberta_munis_tagged_with_province_alberta():
    """Every entry in either AB batch must declare province=Alberta."""
    for muni in AB_ONLY_MUNICIPALITIES:
        assert muni.get("province") == PROVINCE_AB, (
            f"AB entry {muni['short_name']!r} missing province=Alberta"
        )


def test_no_bc_munis_tagged_with_province_alberta():
    """BC entries must not leak the AB province tag.

    BC entries may either omit ``province`` (legacy default behavior) or
    explicitly set ``PROVINCE_BC`` — both are accepted by ``seed_registry``.
    """
    for muni in BC_ONLY_MUNICIPALITIES:
        province = muni.get("province", PROVINCE_BC)
        assert province == PROVINCE_BC, (
            f"BC entry {muni['short_name']!r} declared province={province!r}"
        )


def test_alberta_phase_1_has_active_sources():
    """Phase 1 munis must have at least one ACTIVE source so the poller picks
    them up immediately on deploy."""
    from app.models.municipality import ScrapeStatus

    for muni in ALBERTA_MUNICIPALITIES_PHASE_1:
        active_sources = [
            s for s in muni["sources"] if s["scrape_status"] == ScrapeStatus.ACTIVE
        ]
        assert active_sources, (
            f"Phase 1 muni {muni['short_name']!r} has no ACTIVE sources"
        )


def test_alberta_remainder_uses_pending_status():
    """Remainder munis must be PENDING — they're placeholders, not live."""
    from app.models.municipality import ScrapeStatus

    for muni in ALBERTA_MUNICIPALITIES_REMAINDER:
        for source in muni["sources"]:
            assert source["scrape_status"] == ScrapeStatus.PENDING, (
                f"AB remainder {muni['short_name']!r} should be PENDING, "
                f"got {source['scrape_status']}"
            )
