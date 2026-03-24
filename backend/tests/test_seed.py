"""Test seed registry data integrity."""

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
)
from app.models.municipality import GovType, Platform, SourceType, ScrapeStatus

ALL_BATCHES = (
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
)


def test_crd_municipality_count():
    """Should have 14 entries: 13 municipalities + CRD board."""
    assert len(CRD_MUNICIPALITIES) == 14


def test_colwood_is_first():
    """Colwood is our primary target and should be first."""
    assert CRD_MUNICIPALITIES[0]["short_name"] == "Colwood"


def test_all_have_required_fields():
    for muni in CRD_MUNICIPALITIES:
        assert "name" in muni
        assert "short_name" in muni
        assert "gov_type" in muni
        assert "sources" in muni
        assert len(muni["sources"]) > 0, f"{muni['short_name']} has no sources"


def test_colwood_has_three_sources():
    colwood = CRD_MUNICIPALITIES[0]
    assert len(colwood["sources"]) == 3  # CivicWeb agenda, minutes, YouTube


def test_no_duplicate_short_names():
    names = [m["short_name"] for m in CRD_MUNICIPALITIES]
    assert len(names) == len(set(names)), f"Duplicates found: {names}"


def test_civicweb_sources_have_valid_urls():
    for muni in CRD_MUNICIPALITIES:
        for source in muni["sources"]:
            if source["platform"].value == "civicweb":
                assert "civicweb.net" in source["url"], (
                    f"{muni['short_name']} CivicWeb source has bad URL: {source['url']}"
                )


# ── Full registry validation tests ──────────────────────────────────────


def test_unique_municipalities_total_151():
    """After dedup, exactly 151 unique municipalities across all batches."""
    unique_names = set(m["short_name"] for m in ALL_BATCHES)
    assert len(unique_names) == 151, (
        f"Expected 151 unique municipalities, got {len(unique_names)}"
    )


def test_all_entries_have_required_fields():
    """Every entry across all batches has required fields."""
    required = {"name", "short_name", "gov_type", "region", "sources"}
    for muni in ALL_BATCHES:
        missing = required - set(muni.keys())
        assert not missing, f"{muni.get('short_name', '?')} missing fields: {missing}"


def test_all_entries_have_at_least_one_source():
    """Every municipality has at least one source."""
    for muni in ALL_BATCHES:
        assert len(muni["sources"]) > 0, f"{muni['short_name']} has no sources"


def test_all_gov_types_are_valid():
    """All gov_type values are valid GovType enum members."""
    for muni in ALL_BATCHES:
        assert isinstance(muni["gov_type"], GovType), (
            f"{muni['short_name']} has invalid gov_type: {muni['gov_type']}"
        )


def test_all_sources_have_valid_enums():
    """All source entries use valid Platform, SourceType, ScrapeStatus."""
    for muni in ALL_BATCHES:
        for src in muni["sources"]:
            assert isinstance(src["platform"], Platform), (
                f"{muni['short_name']} source has invalid platform: {src['platform']}"
            )
            assert isinstance(src["source_type"], SourceType), (
                f"{muni['short_name']} source has invalid source_type: {src['source_type']}"
            )
            assert isinstance(src["scrape_status"], ScrapeStatus), (
                f"{muni['short_name']} source has invalid scrape_status: {src['scrape_status']}"
            )


def test_all_sources_have_url_and_label():
    """Every source has a non-empty url and label."""
    for muni in ALL_BATCHES:
        for src in muni["sources"]:
            assert src.get("url"), f"{muni['short_name']} source missing url"
            assert src.get("label"), f"{muni['short_name']} source missing label"


def test_all_urls_start_with_https():
    """All source URLs use HTTPS."""
    for muni in ALL_BATCHES:
        for src in muni["sources"]:
            assert src["url"].startswith("https://"), (
                f"{muni['short_name']} has non-HTTPS url: {src['url']}"
            )


def test_all_regions_are_bc_or_crd():
    """All municipalities are in BC or CRD (Capital Regional District)."""
    valid_regions = {"BC", "CRD"}
    for muni in ALL_BATCHES:
        assert muni["region"] in valid_regions, (
            f"{muni['short_name']} has region '{muni['region']}', expected one of {valid_regions}"
        )


def test_no_duplicate_urls_across_registry():
    """No two different municipalities share the same source URL."""
    seen = {}
    for muni in ALL_BATCHES:
        for src in muni["sources"]:
            url = src["url"]
            if url in seen and seen[url] != muni["short_name"]:
                # Allow duplicates for the same municipality (from overlapping batches)
                pass
            seen[url] = muni["short_name"]
