"""Test seed registry data integrity."""

from app.services.seed_registry import CRD_MUNICIPALITIES


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
