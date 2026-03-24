"""Test model imports and enum consistency."""

from app.models.municipality import Municipality, Source, ScrapeRun, GovType, Platform, SourceType, ScrapeStatus
from app.models.document import Document, Meeting, DocType, MeetingType
from app.models.track import Track, TrackMatch, AVAILABLE_TOPICS
from app.models.audit import AuditLog


def test_all_models_importable():
    """All SQLAlchemy models should import without error."""
    assert Municipality.__tablename__ == "municipalities"
    assert Source.__tablename__ == "sources"
    assert ScrapeRun.__tablename__ == "scrape_runs"
    assert Meeting.__tablename__ == "meetings"
    assert Document.__tablename__ == "documents"
    assert Track.__tablename__ == "tracks"
    assert TrackMatch.__tablename__ == "track_matches"
    assert AuditLog.__tablename__ == "audit_log"


def test_enums():
    assert GovType.CITY.value == "city"
    assert Platform.CIVICWEB.value == "civicweb"
    assert SourceType.AGENDA.value == "agenda"
    assert ScrapeStatus.ACTIVE.value == "active"
    assert DocType.VIDEO.value == "video"
    assert MeetingType.PUBLIC_HEARING.value == "public_hearing"


def test_available_topics():
    assert len(AVAILABLE_TOPICS) == 12
    assert "ocp_updates" in AVAILABLE_TOPICS
    assert "rezoning" in AVAILABLE_TOPICS
    assert "public_hearings" in AVAILABLE_TOPICS
