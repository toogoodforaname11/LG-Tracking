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
    VALID_PROVINCES,
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
    assert len(AVAILABLE_TOPICS) == 13
    assert "ocp_housing" in AVAILABLE_TOPICS
    assert "zoning_density" in AVAILABLE_TOPICS
    assert "tod" in AVAILABLE_TOPICS


def test_province_constants():
    """Province literals must match the wire format consumed by the frontend."""
    assert PROVINCE_BC == "BC"
    assert PROVINCE_AB == "Alberta"
    assert PROVINCE_BC in VALID_PROVINCES
    assert PROVINCE_AB in VALID_PROVINCES
    assert "Ontario" not in VALID_PROVINCES
