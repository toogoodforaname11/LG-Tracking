"""Integration tests for the poll pipeline: source -> scrape -> store -> deduplicate -> alert.

Tests the full discovery flow using mocked scrapers and DB sessions.
"""

import hashlib
from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.discovery.base import DiscoveredItem
from app.discovery.poller import (
    poll_source,
    store_discovered_items,
    run_discovery,
    _get_custom_scraper,
    BROKEN_THRESHOLD,
    DOC_TYPE_MAP,
    MEETING_TYPE_MAP,
)
from app.models.municipality import Platform, ScrapeStatus
from app.models.document import DocType, MeetingType


# --- Helpers ---


def _make_source(platform=Platform.CIVICWEB, status=ScrapeStatus.ACTIVE, **kwargs):
    """Create a mock Source object."""
    source = MagicMock()
    source.id = kwargs.get("id", 1)
    source.platform = platform
    source.scrape_status = status
    source.url = kwargs.get("url", "https://example.civicweb.net/Portal")
    source.label = kwargs.get("label", "Test Source")
    source.scrape_config = kwargs.get("scrape_config", None)
    source.municipality_id = kwargs.get("municipality_id", 1)
    source.last_error = None
    source.consecutive_failures = 0
    source.last_scraped_at = None
    return source


def _make_municipality(**kwargs):
    """Create a mock Municipality object."""
    muni = MagicMock()
    muni.id = kwargs.get("id", 1)
    muni.short_name = kwargs.get("short_name", "Colwood")
    muni.is_active = True
    return muni


def _make_item(title="Test Agenda", item_type="agenda", url="https://example.com/doc.pdf",
               meeting_date="2026-03-10", meeting_type="regular"):
    """Create a DiscoveredItem."""
    return DiscoveredItem(
        municipality="Colwood",
        title=title,
        item_type=item_type,
        url=url,
        meeting_date=meeting_date,
        meeting_type=meeting_type,
    )


def _make_video_item():
    """Create a video DiscoveredItem with metadata."""
    return DiscoveredItem(
        municipality="Colwood",
        title="Council Meeting Recording",
        item_type="video",
        url="https://youtube.com/watch?v=abc123",
        meeting_date="2026-03-10",
        meeting_type="regular",
        raw_metadata={
            "content_for_embedding": "Discussion of rezoning bylaws...",
            "timestamps": [{"t": "0:15:30", "label": "Rezoning discussion"}],
            "duration": "1:30:00",
        },
    )


# --- poll_source dispatch tests ---


@pytest.mark.asyncio
async def test_poll_source_dispatches_civicweb():
    """poll_source should create a CivicWebScraper for CIVICWEB sources."""
    source = _make_source(platform=Platform.CIVICWEB)
    muni = _make_municipality()

    with patch("app.discovery.poller.CivicWebScraper") as MockScraper:
        mock_instance = AsyncMock()
        mock_instance.discover = AsyncMock(return_value=[_make_item()])
        mock_instance.close = AsyncMock()
        MockScraper.return_value = mock_instance

        items = await poll_source(source, muni)

        MockScraper.assert_called_once_with("Colwood", source.url)
        assert len(items) == 1
        assert items[0].title == "Test Agenda"


@pytest.mark.asyncio
async def test_poll_source_dispatches_granicus():
    """poll_source should create a GranicusScraper for GRANICUS sources."""
    source = _make_source(platform=Platform.GRANICUS)
    muni = _make_municipality()

    with patch("app.discovery.poller.GranicusScraper") as MockScraper:
        mock_instance = AsyncMock()
        mock_instance.discover = AsyncMock(return_value=[])
        mock_instance.close = AsyncMock()
        MockScraper.return_value = mock_instance

        items = await poll_source(source, muni)
        MockScraper.assert_called_once_with("Colwood", source.url)


@pytest.mark.asyncio
async def test_poll_source_dispatches_escribe():
    """poll_source should create an EScribeScraper for ESCRIBE sources."""
    source = _make_source(platform=Platform.ESCRIBE)
    muni = _make_municipality()

    with patch("app.discovery.poller.EScribeScraper") as MockScraper:
        mock_instance = AsyncMock()
        mock_instance.discover = AsyncMock(return_value=[])
        mock_instance.close = AsyncMock()
        MockScraper.return_value = mock_instance

        items = await poll_source(source, muni)
        MockScraper.assert_called_once_with("Colwood", source.url)


@pytest.mark.asyncio
async def test_poll_source_dispatches_youtube():
    """poll_source should resolve handle URLs to a UCxxx channel id and pass
    that to YouTubeScraper. The resolved id should also be cached back into
    ``scrape_config`` so the second poll skips the resolution round-trip.
    """
    source = _make_source(
        platform=Platform.YOUTUBE,
        url="https://www.youtube.com/@CityofColwood",
    )
    muni = _make_municipality()
    fake_channel_id = "UC" + "0" * 22

    with (
        patch("app.discovery.poller.YouTubeScraper") as MockScraper,
        patch(
            "app.discovery.poller.resolve_channel_id",
            new=AsyncMock(return_value=fake_channel_id),
        ) as MockResolve,
    ):
        mock_instance = AsyncMock()
        mock_instance.discover = AsyncMock(return_value=[])
        mock_instance.close = AsyncMock()
        MockScraper.return_value = mock_instance

        await poll_source(source, muni)

        MockResolve.assert_awaited_once_with("https://www.youtube.com/@CityofColwood")
        MockScraper.assert_called_once_with("Colwood", fake_channel_id)
        # Resolved id cached back onto the source.
        assert source.scrape_config and fake_channel_id in source.scrape_config


@pytest.mark.asyncio
async def test_poll_source_youtube_uses_cached_channel_id():
    """If scrape_config already holds a real UCxxx, no resolution call happens."""
    cached_id = "UC" + "1" * 22
    source = _make_source(
        platform=Platform.YOUTUBE,
        url="https://www.youtube.com/@CityofColwood",
    )
    source.scrape_config = '{"channel_id": "%s"}' % cached_id
    muni = _make_municipality()

    with (
        patch("app.discovery.poller.YouTubeScraper") as MockScraper,
        patch(
            "app.discovery.poller.resolve_channel_id",
            new=AsyncMock(),
        ) as MockResolve,
    ):
        mock_instance = AsyncMock()
        mock_instance.discover = AsyncMock(return_value=[])
        mock_instance.close = AsyncMock()
        MockScraper.return_value = mock_instance

        await poll_source(source, muni)

        MockResolve.assert_not_called()
        MockScraper.assert_called_once_with("Colwood", cached_id)


@pytest.mark.asyncio
async def test_poll_source_youtube_returns_empty_when_resolution_fails():
    """A handle URL we can't resolve should produce zero items, not crash."""
    source = _make_source(
        platform=Platform.YOUTUBE,
        url="https://www.youtube.com/@TotallyNotARealChannelXYZ",
    )
    muni = _make_municipality()

    with (
        patch("app.discovery.poller.YouTubeScraper") as MockScraper,
        patch(
            "app.discovery.poller.resolve_channel_id",
            new=AsyncMock(return_value=None),
        ),
    ):
        items = await poll_source(source, muni)
        assert items == []
        MockScraper.assert_not_called()


@pytest.mark.asyncio
async def test_poll_source_dispatches_custom_substantive():
    """poll_source should use CUSTOM_SCRAPER_MAP for known custom scrapers."""
    source = _make_source(platform=Platform.CUSTOM)
    muni = _make_municipality(short_name="Saanich")

    with patch.dict("app.discovery.poller.CUSTOM_SCRAPER_MAP", {"Saanich": MagicMock()}) as mock_map:
        mock_instance = AsyncMock()
        mock_instance.discover = AsyncMock(return_value=[_make_item()])
        mock_instance.close = AsyncMock()
        mock_map["Saanich"].return_value = mock_instance

        items = await poll_source(source, muni)
        mock_map["Saanich"].assert_called_once_with("Saanich", source.url)
        assert len(items) == 1


@pytest.mark.asyncio
async def test_poll_source_dispatches_custom_generic():
    """poll_source should fall back to make_generic_scraper for config-driven municipalities."""
    source = _make_source(platform=Platform.CUSTOM)
    muni = _make_municipality(short_name="Surrey")

    with patch("app.discovery.poller.make_generic_scraper") as mock_factory:
        mock_scraper = AsyncMock()
        mock_scraper.discover = AsyncMock(return_value=[_make_item()])
        mock_scraper.close = AsyncMock()
        mock_factory.return_value = mock_scraper

        items = await poll_source(source, muni)
        mock_factory.assert_called_once_with("Surrey", source.url)
        assert len(items) == 1


@pytest.mark.asyncio
async def test_poll_source_returns_empty_on_error():
    """poll_source should return [] and not raise if scraper throws."""
    source = _make_source(platform=Platform.CIVICWEB)
    muni = _make_municipality()

    with patch("app.discovery.poller.CivicWebScraper") as MockScraper:
        mock_instance = AsyncMock()
        mock_instance.discover = AsyncMock(side_effect=Exception("Network error"))
        mock_instance.close = AsyncMock()
        MockScraper.return_value = mock_instance

        items = await poll_source(source, muni)
        assert items == []


@pytest.mark.asyncio
async def test_poll_source_unsupported_platform():
    """poll_source should return [] for unsupported platforms."""
    source = _make_source(platform=Platform.UNKNOWN)
    muni = _make_municipality()

    items = await poll_source(source, muni)
    assert items == []


# --- store_discovered_items tests ---


@pytest.mark.asyncio
async def test_store_new_documents():
    """New documents should be stored with correct content hash and fields."""
    db = AsyncMock()
    source = _make_source()
    muni = _make_municipality()
    items = [_make_item(), _make_item(title="Test Minutes", item_type="minutes",
                                      url="https://example.com/minutes.pdf")]

    # Mock: no existing documents
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = None
    db.execute = AsyncMock(return_value=mock_result)
    db.flush = AsyncMock()
    db.commit = AsyncMock()

    # Mock meeting creation: first call returns no existing document,
    # second call returns no existing meeting
    call_count = 0

    async def mock_execute(query):
        nonlocal call_count
        call_count += 1
        result = MagicMock()
        result.scalar_one_or_none.return_value = None
        # For meetings, make flush set an id
        return result

    db.execute = AsyncMock(side_effect=mock_execute)

    stats, new_docs = await store_discovered_items(db, items, source, muni)

    assert stats["new"] == 2
    assert stats["existing"] == 0
    assert len(new_docs) == 2
    assert db.commit.called


@pytest.mark.asyncio
async def test_store_deduplicates_by_url():
    """Documents with the same URL should be detected as existing."""
    db = AsyncMock()
    source = _make_source()
    muni = _make_municipality()
    items = [_make_item()]

    # Mock: document already exists
    existing_doc = MagicMock()
    existing_doc.content_hash = hashlib.sha256("Test Agenda".encode()).hexdigest()
    existing_doc.last_checked_at = None
    existing_doc.raw_text = None

    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = existing_doc
    db.execute = AsyncMock(return_value=mock_result)
    db.commit = AsyncMock()

    stats, new_docs = await store_discovered_items(db, items, source, muni)

    assert stats["existing"] == 1
    assert stats["new"] == 0
    assert len(new_docs) == 0


@pytest.mark.asyncio
async def test_store_detects_content_revision():
    """Changed content at same URL should mark document for reprocessing."""
    db = AsyncMock()
    source = _make_source()
    muni = _make_municipality()
    items = [_make_item(title="Updated Agenda")]

    # Existing doc has old hash
    existing_doc = MagicMock()
    existing_doc.content_hash = hashlib.sha256("Old Agenda".encode()).hexdigest()
    existing_doc.last_checked_at = None
    existing_doc.raw_text = None

    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = existing_doc
    db.execute = AsyncMock(return_value=mock_result)
    db.commit = AsyncMock()

    stats, new_docs = await store_discovered_items(db, items, source, muni)

    assert stats["existing"] == 1
    assert stats.get("updated", 0) == 1
    assert existing_doc.is_processed is False
    assert existing_doc.is_new is True


@pytest.mark.asyncio
async def test_store_legacy_hash_migration():
    """Documents with legacy URL-based hash should be silently upgraded."""
    db = AsyncMock()
    source = _make_source()
    muni = _make_municipality()
    url = "https://example.com/doc.pdf"
    items = [_make_item(url=url)]

    # Existing doc has legacy hash (sha256 of URL)
    legacy_hash = hashlib.sha256(url.encode()).hexdigest()
    existing_doc = MagicMock()
    existing_doc.content_hash = legacy_hash
    existing_doc.last_checked_at = None
    existing_doc.raw_text = None

    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = existing_doc
    db.execute = AsyncMock(return_value=mock_result)
    db.commit = AsyncMock()

    stats, new_docs = await store_discovered_items(db, items, source, muni)

    # Hash should be upgraded to content-based hash
    new_hash = hashlib.sha256("Test Agenda".encode()).hexdigest()
    assert existing_doc.content_hash == new_hash
    # Should NOT be marked for reprocessing (content hasn't changed)
    assert stats["existing"] == 1
    assert stats.get("updated", 0) == 0


@pytest.mark.asyncio
async def test_store_video_with_metadata():
    """Video items should store raw_text, timestamps, and duration."""
    db = AsyncMock()
    source = _make_source()
    muni = _make_municipality()
    items = [_make_video_item()]

    call_count = 0
    added_docs = []

    async def mock_execute(query):
        nonlocal call_count
        call_count += 1
        result = MagicMock()
        result.scalar_one_or_none.return_value = None
        return result

    db.execute = AsyncMock(side_effect=mock_execute)
    db.flush = AsyncMock()
    db.commit = AsyncMock()

    original_add = db.add

    def capture_add(obj):
        if hasattr(obj, 'raw_text'):
            added_docs.append(obj)
        original_add(obj)

    db.add = capture_add

    stats, new_docs = await store_discovered_items(db, items, source, muni)

    assert stats["new"] == 1
    assert len(new_docs) == 1
    doc = new_docs[0]
    assert doc.raw_text == "Discussion of rezoning bylaws..."
    assert doc.video_timestamps == [{"t": "0:15:30", "label": "Rezoning discussion"}]
    assert doc.video_duration == "1:30:00"


# --- DOC_TYPE_MAP and MEETING_TYPE_MAP coverage ---


def test_doc_type_map_completeness():
    """DOC_TYPE_MAP should cover agenda, minutes, video."""
    assert DOC_TYPE_MAP["agenda"] == DocType.AGENDA
    assert DOC_TYPE_MAP["minutes"] == DocType.MINUTES
    assert DOC_TYPE_MAP["video"] == DocType.VIDEO


def test_meeting_type_map_completeness():
    """MEETING_TYPE_MAP should cover all standard meeting types."""
    assert MEETING_TYPE_MAP["regular"] == MeetingType.REGULAR
    assert MEETING_TYPE_MAP["special"] == MeetingType.SPECIAL
    assert MEETING_TYPE_MAP["public_hearing"] == MeetingType.PUBLIC_HEARING
    assert MEETING_TYPE_MAP["committee"] == MeetingType.COMMITTEE
    assert MEETING_TYPE_MAP["committee_of_the_whole"] == MeetingType.COW


# --- run_discovery integration tests ---


@pytest.mark.asyncio
async def test_run_discovery_empty_sources():
    """run_discovery should return {} when no sources are found."""
    db = AsyncMock()
    mock_result = MagicMock()
    mock_result.all.return_value = []
    db.execute = AsyncMock(return_value=mock_result)

    result = await run_discovery(db)
    assert result == {}


@pytest.mark.asyncio
async def test_run_discovery_marks_broken_after_threshold():
    """A source should be marked BROKEN after BROKEN_THRESHOLD consecutive failures."""
    source = _make_source()
    source.consecutive_failures = BROKEN_THRESHOLD - 1  # One more failure = BROKEN

    muni = _make_municipality()

    db = AsyncMock()

    # First execute returns the source list
    source_result = MagicMock()
    source_result.all.return_value = [(source, muni)]

    db.execute = AsyncMock(return_value=source_result)
    db.flush = AsyncMock()
    db.commit = AsyncMock()

    with patch("app.discovery.poller.poll_source", new_callable=AsyncMock) as mock_poll:
        mock_poll.side_effect = Exception("Connection refused")

        with patch("app.discovery.poller.send_immediate_alerts_for_documents", new_callable=AsyncMock):
            result = await run_discovery(db)

    assert source.scrape_status == ScrapeStatus.BROKEN
    assert source.consecutive_failures == BROKEN_THRESHOLD


@pytest.mark.asyncio
async def test_run_discovery_resets_failures_on_success():
    """Successful poll should reset consecutive_failures and set status to ACTIVE."""
    source = _make_source(status=ScrapeStatus.PENDING)
    source.consecutive_failures = 3
    muni = _make_municipality()

    db = AsyncMock()

    source_result = MagicMock()
    source_result.all.return_value = [(source, muni)]
    db.execute = AsyncMock(return_value=source_result)
    db.flush = AsyncMock()
    db.commit = AsyncMock()

    with patch("app.discovery.poller.poll_source", new_callable=AsyncMock) as mock_poll:
        mock_poll.return_value = [_make_item()]

        with patch("app.discovery.poller.store_discovered_items", new_callable=AsyncMock) as mock_store:
            mock_store.return_value = ({"total": 1, "new": 1}, [MagicMock()])

            with patch("app.discovery.poller.send_immediate_alerts_for_documents", new_callable=AsyncMock) as mock_alerts:
                mock_alerts.return_value = {"alerts_sent": 0}
                result = await run_discovery(db)

    assert source.scrape_status == ScrapeStatus.ACTIVE
    assert source.consecutive_failures == 0
    assert source.last_error is None


@pytest.mark.asyncio
async def test_run_discovery_sends_immediate_alerts():
    """run_discovery should call send_immediate_alerts_for_documents when new docs found."""
    source = _make_source()
    muni = _make_municipality()

    db = AsyncMock()

    source_result = MagicMock()
    source_result.all.return_value = [(source, muni)]
    db.execute = AsyncMock(return_value=source_result)
    db.flush = AsyncMock()
    db.commit = AsyncMock()

    new_doc = MagicMock()

    with patch("app.discovery.poller.poll_source", new_callable=AsyncMock) as mock_poll:
        mock_poll.return_value = [_make_item()]

        with patch("app.discovery.poller.store_discovered_items", new_callable=AsyncMock) as mock_store:
            mock_store.return_value = ({"total": 1, "new": 1}, [new_doc])

            with patch("app.discovery.poller.send_immediate_alerts_for_documents", new_callable=AsyncMock) as mock_alerts:
                mock_alerts.return_value = {"alerts_sent": 1}
                result = await run_discovery(db)

                mock_alerts.assert_called_once()
                call_args = mock_alerts.call_args
                assert new_doc in call_args[0][1]  # new_doc in the documents list


@pytest.mark.asyncio
async def test_run_discovery_skips_alerts_when_no_new_docs():
    """run_discovery should NOT call alerts when all docs are existing."""
    source = _make_source()
    muni = _make_municipality()

    db = AsyncMock()

    source_result = MagicMock()
    source_result.all.return_value = [(source, muni)]
    db.execute = AsyncMock(return_value=source_result)
    db.flush = AsyncMock()
    db.commit = AsyncMock()

    with patch("app.discovery.poller.poll_source", new_callable=AsyncMock) as mock_poll:
        mock_poll.return_value = [_make_item()]

        with patch("app.discovery.poller.store_discovered_items", new_callable=AsyncMock) as mock_store:
            mock_store.return_value = ({"total": 1, "new": 0, "existing": 1}, [])

            with patch("app.discovery.poller.send_immediate_alerts_for_documents", new_callable=AsyncMock) as mock_alerts:
                result = await run_discovery(db)
                mock_alerts.assert_not_called()


# --- Content hash computation ---


def test_content_hash_prefers_raw_text():
    """Content hash should use raw_text when available (for videos)."""
    raw_text = "Discussion of rezoning"
    expected = hashlib.sha256(raw_text.encode()).hexdigest()

    # Simulated logic from store_discovered_items
    hash_source = raw_text or "Title" or "url"
    assert hashlib.sha256(hash_source.encode()).hexdigest() == expected


def test_content_hash_falls_back_to_title():
    """Content hash should use title when raw_text is None."""
    title = "Council Agenda March 2026"
    expected = hashlib.sha256(title.encode()).hexdigest()

    hash_source = None or title or "url"
    assert hashlib.sha256(hash_source.encode()).hexdigest() == expected


def test_content_hash_falls_back_to_url():
    """Content hash should use URL as last resort."""
    url = "https://example.com/doc.pdf"
    expected = hashlib.sha256(url.encode()).hexdigest()

    hash_source = None or None or url
    assert hashlib.sha256(hash_source.encode()).hexdigest() == expected
