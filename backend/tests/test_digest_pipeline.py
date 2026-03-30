"""Integration tests for the weekly digest pipeline:
gather recent docs -> match subscriber preferences -> render email -> send.

Also tests the instant alert rendering and delivery flow.
"""

from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.services.digest import (
    build_digest_items,
    render_digest_email,
    run_weekly_digest,
    get_recent_documents,
)
from app.services.instant_alerts import (
    render_alert_email,
    send_alert_via_smtp,
    send_immediate_alerts_for_documents,
)
from app.services.email import render_timestamp_links_html, render_timestamp_links_text
from app.models.document import DocType


# --- Helpers ---


def _make_document(**kwargs):
    doc = MagicMock()
    doc.id = kwargs.get("id", 1)
    doc.municipality_id = kwargs.get("municipality_id", 1)
    doc.title = kwargs.get("title", "Council Agenda - Rezoning")
    doc.raw_text = kwargs.get("raw_text", "Discussion of rezoning bylaw amendment")
    doc.doc_type = kwargs.get("doc_type", DocType.AGENDA)
    doc.url = kwargs.get("url", "https://example.com/agenda.pdf")
    doc.video_timestamps = kwargs.get("video_timestamps", None)
    doc.first_seen_at = kwargs.get(
        "first_seen_at",
        datetime.now(timezone.utc) - timedelta(days=1),
    )
    return doc


def _make_municipality(**kwargs):
    muni = MagicMock()
    muni.id = kwargs.get("id", 1)
    muni.short_name = kwargs.get("short_name", "Colwood")
    return muni


def _make_subscriber(**kwargs):
    sub = MagicMock()
    sub.email = kwargs.get("email", "user@example.com")
    sub.municipalities = kwargs.get("municipalities", ["Colwood"])
    sub.topics = kwargs.get("topics", ["zoning_density"])
    sub.keywords = kwargs.get("keywords", "rezoning")
    sub.immediate_alerts = kwargs.get("immediate_alerts", False)
    sub.active = kwargs.get("active", True)
    sub.unsubscribe_token = kwargs.get("unsubscribe_token", "test-token-uuid")
    return sub


# --- build_digest_items ---


def test_build_digest_items_matches_topic():
    """Documents matching subscriber topics should appear in digest."""
    doc = _make_document(raw_text="Rezoning application for density increase")
    muni = _make_municipality()

    items = build_digest_items([(doc, muni)], ["zoning_density"], "")

    assert len(items) == 1
    assert items[0]["municipality"] == "Colwood"
    assert "zoning_density" in items[0]["matched_topics"]


def test_build_digest_items_matches_keyword():
    """Documents matching subscriber keywords should appear in digest."""
    doc = _make_document(raw_text="Discussion of affordable housing policy")
    muni = _make_municipality()

    items = build_digest_items([(doc, muni)], [], "affordable housing")

    assert len(items) == 1
    assert "affordable housing" in items[0]["matched_keywords"]


def test_build_digest_items_no_match():
    """Documents not matching any topic or keyword should be excluded."""
    doc = _make_document(raw_text="Parks and recreation budget discussion")
    muni = _make_municipality()

    items = build_digest_items([(doc, muni)], ["tod"], "skytrain")

    assert len(items) == 0


def test_build_digest_items_multiple_topics():
    """Documents matching multiple topics should list all matched topics."""
    doc = _make_document(
        raw_text="Rezoning and OCP amendment for increased density"
    )
    muni = _make_municipality()

    items = build_digest_items(
        [(doc, muni)],
        ["zoning_density", "ocp_housing"],
        "",
    )

    assert len(items) == 1
    assert "zoning_density" in items[0]["matched_topics"]
    assert "ocp_housing" in items[0]["matched_topics"]


def test_build_digest_items_uses_title_fallback():
    """When raw_text is None, should match against title."""
    doc = _make_document(raw_text=None, title="Rezoning Application 123")
    muni = _make_municipality()

    items = build_digest_items([(doc, muni)], ["zoning_density"], "")

    assert len(items) == 1


def test_build_digest_items_case_insensitive():
    """Matching should be case-insensitive."""
    doc = _make_document(raw_text="REZONING APPLICATION FOR DENSITY")
    muni = _make_municipality()

    items = build_digest_items([(doc, muni)], ["zoning_density"], "")

    assert len(items) == 1


# --- render_digest_email ---


def test_render_digest_email_with_items():
    """Digest email should contain municipality and doc info."""
    items = [{
        "municipality": "Colwood",
        "doc_type": "agenda",
        "title": "Council Rezoning",
        "url": "https://example.com/doc.pdf",
        "summary": None,
        "key_points": None,
        "matched_topics": ["zoning_density"],
        "matched_keywords": [],
        "verification_status": "unverified",
    }]

    html = render_digest_email("user@example.com", items, "March 30, 2026", "https://example.com/unsub")

    assert "Colwood" in html
    assert "Council Rezoning" in html
    assert "AGENDA" in html
    assert "Unsubscribe" in html


def test_render_digest_email_empty_items():
    """Empty digest should show 'no updates' message."""
    html = render_digest_email("user@example.com", [], "March 30, 2026", "https://example.com/unsub")

    assert "No new updates" in html


def test_render_digest_email_verified_badge():
    """Verified items should show verification badge."""
    items = [{
        "municipality": "Colwood",
        "doc_type": "agenda",
        "title": "Verified Item",
        "url": "#",
        "summary": "Summary text",
        "key_points": ["Point 1", "Point 2"],
        "matched_topics": [],
        "matched_keywords": [],
        "verification_status": "verified",
    }]

    html = render_digest_email("user@example.com", items, "March 30, 2026", "#")

    assert "Verified" in html
    assert "Summary text" in html
    assert "Point 1" in html


# --- render_alert_email ---


def test_render_alert_email():
    """Alert email should contain document info and unsubscribe link."""
    item = {
        "doc_type": "agenda",
        "title": "Urgent Rezoning",
        "url": "https://example.com/doc.pdf",
        "summary": "Important rezoning decision.",
        "key_points": ["Density increase"],
        "matched_topics": ["zoning_density"],
        "verification_status": "unverified",
    }

    html = render_alert_email(item, "Colwood", "March 30, 2026", "https://example.com/unsub")

    assert "Colwood" in html
    assert "Urgent Rezoning" in html
    assert "AGENDA" in html
    assert "Important rezoning decision." in html
    assert "Density increase" in html
    assert "Unsubscribe" in html


def test_render_alert_email_partially_verified():
    """Partially verified items should show warning badge."""
    item = {
        "doc_type": "minutes",
        "title": "Minutes",
        "url": "#",
        "verification_status": "partially_verified",
    }

    html = render_alert_email(item, "Victoria", "March 30, 2026", "#")

    assert "Partially Verified" in html


# --- send_alert_via_smtp ---


def test_send_alert_skips_without_smtp_config():
    """Without SMTP credentials, should return False and not attempt send."""
    with patch("app.services.email.settings") as mock_settings:
        mock_settings.smtp_host = ""
        mock_settings.smtp_username = ""
        mock_settings.smtp_password = ""

        result = send_alert_via_smtp("user@test.com", "<html></html>", "Colwood", "March 30")

    assert result is False


def test_send_alert_with_smtp_config():
    """With SMTP credentials, should send email via SMTP."""
    with patch("app.services.email.send_email") as mock_send:
        mock_send.return_value = True

        result = send_alert_via_smtp("user@test.com", "<html></html>", "Colwood", "March 30")

    assert result is True
    mock_send.assert_called_once()


# --- send_immediate_alerts_for_documents ---


@pytest.mark.asyncio
async def test_immediate_alerts_empty_docs():
    """No documents should return zero stats."""
    db = AsyncMock()

    stats = await send_immediate_alerts_for_documents(db, [])

    assert stats["alerts_sent"] == 0
    assert stats["subscribers_checked"] == 0


@pytest.mark.asyncio
async def test_immediate_alerts_no_subscribers():
    """No subscribers with immediate_alerts should return zero stats."""
    db = AsyncMock()
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = []
    db.execute = AsyncMock(return_value=mock_result)

    doc = _make_document()

    stats = await send_immediate_alerts_for_documents(db, [doc])

    assert stats["subscribers_checked"] == 0


@pytest.mark.asyncio
async def test_immediate_alerts_skips_without_base_url():
    """Without APP_BASE_URL, should skip alerts (broken unsubscribe links)."""
    db = AsyncMock()
    subscriber = _make_subscriber(immediate_alerts=True)

    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = [subscriber]
    db.execute = AsyncMock(return_value=mock_result)

    doc = _make_document()

    with patch("app.services.instant_alerts.settings") as mock_settings:
        mock_settings.app_base_url = ""

        stats = await send_immediate_alerts_for_documents(db, [doc])

    assert stats["alerts_sent"] == 0


@pytest.mark.asyncio
async def test_immediate_alerts_matches_subscriber_municipalities():
    """Alerts should only be sent for docs matching subscriber's municipalities."""
    subscriber = _make_subscriber(
        municipalities=["Colwood"],
        topics=["zoning_density"],
        immediate_alerts=True,
    )
    muni = _make_municipality(id=1, short_name="Colwood")
    doc = _make_document(
        municipality_id=1,
        raw_text="Rezoning application for density increase",
    )

    db = AsyncMock()
    call_count = 0

    async def mock_execute(query):
        nonlocal call_count
        call_count += 1
        result = MagicMock()
        if call_count == 1:
            result.scalars.return_value.all.return_value = [subscriber]
        elif call_count == 2:
            result.scalars.return_value.all.return_value = [muni]
        return result

    db.execute = AsyncMock(side_effect=mock_execute)

    with patch("app.services.instant_alerts.settings") as mock_settings:
        mock_settings.app_base_url = "https://example.com"

        with patch("app.services.instant_alerts.send_alert_via_smtp") as mock_send:
            mock_send.return_value = True

            stats = await send_immediate_alerts_for_documents(db, [doc])

    assert stats["subscribers_checked"] == 1
    assert stats["documents_matched"] >= 1
    assert stats["alerts_sent"] >= 1


# --- run_weekly_digest ---


@pytest.mark.asyncio
async def test_weekly_digest_no_subscribers():
    """With no active subscribers, should return zero stats."""
    db = AsyncMock()
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = []
    db.execute = AsyncMock(return_value=mock_result)

    stats = await run_weekly_digest(db)

    assert stats["subscribers_processed"] == 0
    assert stats["emails_sent"] == 0


@pytest.mark.asyncio
async def test_weekly_digest_skips_without_base_url():
    """Without APP_BASE_URL, digest emails should fail."""
    subscriber = _make_subscriber()

    db = AsyncMock()
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = [subscriber]
    db.execute = AsyncMock(return_value=mock_result)

    with patch("app.services.digest.settings") as mock_settings:
        mock_settings.app_base_url = ""

        with patch("app.services.digest.get_recent_documents", new_callable=AsyncMock) as mock_docs:
            mock_docs.return_value = []

            stats = await run_weekly_digest(db)

    assert stats["subscribers_processed"] == 1
    assert stats["emails_failed"] == 1


@pytest.mark.asyncio
async def test_weekly_digest_sends_email():
    """Active subscriber with matching docs should receive digest email."""
    subscriber = _make_subscriber()
    doc = _make_document(raw_text="Rezoning application discussion")
    muni = _make_municipality()

    db = AsyncMock()
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = [subscriber]
    db.execute = AsyncMock(return_value=mock_result)

    with patch("app.services.digest.settings") as mock_settings:
        mock_settings.app_base_url = "https://example.com"

        with patch("app.services.digest.get_recent_documents", new_callable=AsyncMock) as mock_docs:
            mock_docs.return_value = [(doc, muni)]

            with patch("app.services.digest.send_digest_via_smtp") as mock_send:
                mock_send.return_value = True

                stats = await run_weekly_digest(db)

    assert stats["subscribers_processed"] == 1
    assert stats["emails_sent"] == 1
    assert stats["total_items"] >= 1
    mock_send.assert_called_once()


# --- render_timestamp_links_html ---


def test_render_timestamp_links_html_with_timestamps():
    """Timestamp links should render as clickable deep links."""
    timestamps = [
        {"t": "0:15:30", "label": "Public Hearing - OCP Amendment", "url": "https://youtube.com/watch?v=X&t=930"},
        {"t": "1:02:00", "label": "Rezoning Discussion", "url": "https://youtube.com/watch?v=X&t=3720"},
    ]

    html = render_timestamp_links_html(timestamps)

    assert "Video Timestamps" in html
    assert "0:15:30" in html
    assert "Public Hearing - OCP Amendment" in html
    assert "https://youtube.com/watch?v=X&amp;t=930" in html or "t=930" in html
    assert "1:02:00" in html
    assert "Rezoning Discussion" in html


def test_render_timestamp_links_html_empty():
    """No timestamps should return empty string."""
    assert render_timestamp_links_html(None) == ""
    assert render_timestamp_links_html([]) == ""


def test_render_timestamp_links_text_with_timestamps():
    """Plain text timestamps should include deep link URLs."""
    timestamps = [
        {"t": "0:15:30", "label": "Public Hearing", "url": "https://youtube.com/watch?v=X&t=930"},
    ]

    text = render_timestamp_links_text(timestamps)

    assert "Video Timestamps" in text
    assert "0:15:30" in text
    assert "Public Hearing" in text
    assert "t=930" in text


def test_render_timestamp_links_text_empty():
    """No timestamps should return empty string."""
    assert render_timestamp_links_text(None) == ""
    assert render_timestamp_links_text([]) == ""


# --- build_digest_items with TrackMatch AI data ---


def _make_track_match(**kwargs):
    """Create a mock TrackMatch."""
    tm = MagicMock()
    tm.document_id = kwargs.get("document_id", 1)
    tm.match_score = kwargs.get("match_score", 0.85)
    tm.summary = kwargs.get("summary", "AI-generated summary of the document.")
    tm.key_points = kwargs.get("key_points", ["Key point 1", "Key point 2"])
    tm.relevant_timestamps = kwargs.get("relevant_timestamps", None)
    tm.verification_status = kwargs.get("verification_status", "verified")
    return tm


def test_build_digest_items_includes_ai_summary_from_track_match():
    """When TrackMatches are provided, items should include AI summaries and key points."""
    doc = _make_document(id=1, raw_text="Rezoning application for density increase")
    muni = _make_municipality()
    tm = _make_track_match(document_id=1, summary="Council approved rezoning", key_points=["Approved"])

    items = build_digest_items([(doc, muni)], ["zoning_density"], "", track_matches=[tm])

    assert len(items) == 1
    assert items[0]["summary"] == "Council approved rezoning"
    assert items[0]["key_points"] == ["Approved"]
    assert items[0]["verification_status"] == "verified"


def test_build_digest_items_without_track_matches_has_none_summary():
    """Without TrackMatches, summary and key_points should be None."""
    doc = _make_document(id=1, raw_text="Rezoning application for density increase")
    muni = _make_municipality()

    items = build_digest_items([(doc, muni)], ["zoning_density"], "")

    assert len(items) == 1
    assert items[0]["summary"] is None
    assert items[0]["key_points"] is None


def test_build_digest_items_includes_video_timestamp_deep_links():
    """Video documents should include timestamp deep links in digest items."""
    doc = _make_document(
        id=1,
        doc_type=DocType.VIDEO,
        url="https://youtube.com/watch?v=ABC",
        raw_text="Rezoning discussion at council meeting",
        video_timestamps=[
            {"t": "0:15:30", "seconds": 930, "label": "Rezoning Discussion"},
        ],
    )
    muni = _make_municipality()

    items = build_digest_items([(doc, muni)], ["zoning_density"], "")

    assert len(items) == 1
    assert len(items[0]["relevant_timestamps"]) == 1
    ts = items[0]["relevant_timestamps"][0]
    assert ts["t"] == "0:15:30"
    assert ts["label"] == "Rezoning Discussion"
    assert ts["url"] == "https://youtube.com/watch?v=ABC&t=930"


def test_build_digest_items_prefers_gemini_timestamps_over_doc_timestamps():
    """Gemini-extracted timestamps should take precedence over raw doc timestamps."""
    doc = _make_document(
        id=1,
        url="https://youtube.com/watch?v=ABC",
        raw_text="Rezoning discussion",
        video_timestamps=[
            {"t": "0:00:00", "seconds": 0, "label": "Intro"},
        ],
    )
    muni = _make_municipality()
    tm = _make_track_match(
        document_id=1,
        relevant_timestamps=[
            {"t": "0:45:00", "seconds": 2700, "label": "Relevant Rezoning Section"},
        ],
    )

    items = build_digest_items([(doc, muni)], ["zoning_density"], "", track_matches=[tm])

    assert len(items) == 1
    assert len(items[0]["relevant_timestamps"]) == 1
    # Should use Gemini timestamps, not the raw doc timestamps
    assert items[0]["relevant_timestamps"][0]["label"] == "Relevant Rezoning Section"
    assert items[0]["relevant_timestamps"][0]["url"] == "https://youtube.com/watch?v=ABC&t=2700"


# --- Digest email renders timestamps ---


def test_render_digest_email_includes_timestamp_links():
    """Digest email HTML should contain video timestamp deep links."""
    items = [{
        "municipality": "Colwood",
        "doc_type": "video",
        "title": "Council Meeting Video",
        "url": "https://youtube.com/watch?v=ABC",
        "summary": "Meeting discussed rezoning.",
        "key_points": ["Rezoning approved"],
        "matched_topics": ["zoning_density"],
        "matched_keywords": [],
        "verification_status": "unverified",
        "relevant_timestamps": [
            {"t": "0:15:30", "label": "Rezoning Discussion", "url": "https://youtube.com/watch?v=ABC&t=930"},
        ],
    }]

    html = render_digest_email("user@example.com", items, "March 30, 2026", "#")

    assert "Video Timestamps" in html
    assert "0:15:30" in html
    assert "Rezoning Discussion" in html
    assert "t=930" in html


# --- Alert email renders timestamps ---


def test_render_alert_email_includes_timestamp_links():
    """Alert email HTML should contain video timestamp deep links."""
    item = {
        "doc_type": "video",
        "title": "Council Meeting Video",
        "url": "https://youtube.com/watch?v=ABC",
        "summary": "Meeting discussed rezoning.",
        "key_points": ["Rezoning approved"],
        "matched_topics": ["zoning_density"],
        "verification_status": "unverified",
        "relevant_timestamps": [
            {"t": "0:15:30", "label": "Rezoning Discussion", "url": "https://youtube.com/watch?v=ABC&t=930"},
        ],
    }

    html = render_alert_email(item, "Colwood", "March 30, 2026", "#")

    assert "Video Timestamps" in html
    assert "0:15:30" in html
    assert "Rezoning Discussion" in html
