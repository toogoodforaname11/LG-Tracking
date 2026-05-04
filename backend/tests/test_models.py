"""Test model imports and enum consistency."""

from app.models.municipality import (
    Municipality,
    Source,
    ScrapeRun,
    GovType,
    Platform,
    SourceType,
    ScrapeStatus,
    PROVINCE_BC,
    PROVINCE_AB,
    PROVINCE_ON,
    VALID_PROVINCES,
    TIER_UPPER,
    TIER_LOWER,
    TIER_SINGLE,
    VALID_TIERS,
)
from app.models.document import Document, Meeting, DocType, MeetingType
from app.models.track import Track, TrackMatch, AVAILABLE_TOPICS


def test_all_models_importable():
    """All SQLAlchemy models should import without error."""
    assert Municipality.__tablename__ == "municipalities"
    assert Source.__tablename__ == "sources"
    assert ScrapeRun.__tablename__ == "scrape_runs"
    assert Meeting.__tablename__ == "meetings"
    assert Document.__tablename__ == "documents"
    assert Track.__tablename__ == "tracks"
    assert TrackMatch.__tablename__ == "track_matches"


def test_enums():
    assert GovType.CITY.value == "city"
    assert Platform.CIVICWEB.value == "civicweb"
    assert SourceType.AGENDA.value == "agenda"
    assert ScrapeStatus.ACTIVE.value == "active"
    assert DocType.VIDEO.value == "video"
    assert MeetingType.PUBLIC_HEARING.value == "public_hearing"


def test_available_topics():
    # 13 BC topics (incl. other_housing_transit) + 3 ON topics = 16
    assert len(AVAILABLE_TOPICS) == 16
    assert "ocp_housing" in AVAILABLE_TOPICS
    assert "zoning_density" in AVAILABLE_TOPICS
    assert "tod" in AVAILABLE_TOPICS
    # Ontario topics
    assert "official_plans" in AVAILABLE_TOPICS
    assert "secondary_plan_op_amendment" in AVAILABLE_TOPICS
    assert "bill23_more_homes" in AVAILABLE_TOPICS


def test_province_constants():
    """Province literals must match the wire format consumed by the frontend."""
    assert PROVINCE_BC == "BC"
    assert PROVINCE_AB == "Alberta"
    assert PROVINCE_ON == "Ontario"
    assert PROVINCE_BC in VALID_PROVINCES
    assert PROVINCE_AB in VALID_PROVINCES
    assert PROVINCE_ON in VALID_PROVINCES
    # Saskatchewan / Quebec aren't supported yet; guard against silent
    # additions to VALID_PROVINCES sneaking through review.
    assert "Saskatchewan" not in VALID_PROVINCES
    assert "Quebec" not in VALID_PROVINCES


def test_tier_constants():
    """Tier literals match the wire format used by the registry endpoint."""
    assert TIER_UPPER == "upper"
    assert TIER_LOWER == "lower"
    assert TIER_SINGLE == "single"
    assert VALID_TIERS == frozenset({"upper", "lower", "single"})
