"""Test seed registry data integrity — all municipalities, not just CRD."""

from app.models.municipality import Platform
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
)
from app.discovery.poller import CUSTOM_SCRAPER_MAP


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


def test_custom_scraper_map_covers_all_custom_sources():
    """Every municipality with a CUSTOM platform source must have a CUSTOM_SCRAPER_MAP entry."""
    missing = []
    seen = set()
    for muni in ALL_MUNICIPALITIES:
        short = muni["short_name"]
        if short in seen:
            continue
        seen.add(short)
        has_custom = any(s["platform"] == Platform.CUSTOM for s in muni["sources"])
        if has_custom and short not in CUSTOM_SCRAPER_MAP:
            missing.append(short)

    assert not missing, (
        f"Municipalities with CUSTOM sources but no CUSTOM_SCRAPER_MAP entry: {missing}"
    )


def test_total_municipality_count():
    """Sanity check: registry should have at least 160 unique municipalities."""
    unique_names = {m["short_name"] for m in ALL_MUNICIPALITIES}
    assert len(unique_names) >= 160, (
        f"Expected at least 160 unique municipalities, got {len(unique_names)}"
    )


def test_all_source_urls_are_nonempty():
    """No source should have an empty or whitespace-only URL."""
    for muni in ALL_MUNICIPALITIES:
        for source in muni["sources"]:
            assert source["url"].strip(), (
                f"{muni['short_name']} has empty URL in source: {source['label']}"
            )
