"""End-to-end-ish smoke test: Alberta subscriber → Calgary document match.

Asserts that the matching pipeline routes a discovered Calgary agenda to a
subscriber whose preferences include ``province="Alberta"`` and
``municipalities=["Calgary"]``. We mock the SMTP send and the database so the
test is hermetic.

The test exercises ``send_immediate_alerts_for_documents`` directly because
that function sits in the seam between the poller (which has just stored a
new ``Document``) and the email transport. If province routing breaks, this
test fails with a clear diff.
"""

from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.models.document import Document, DocType
from app.services.instant_alerts import send_immediate_alerts_for_documents


def _make_calgary_doc(*, municipality_id: int = 999) -> Document:
    """Build a Document representing a Calgary agenda hit on a TOD topic."""
    doc = Document(
        municipality_id=municipality_id,
        doc_type=DocType.AGENDA,
        title="Calgary Regular Council — Transit Oriented Development",
        url="https://pub-calgary.escribemeetings.com/FileStream.ashx?DocumentId=12345",
        content_hash="abc123",
        # build_digest_items uses raw_text (or title fallback) for keyword match.
        raw_text=(
            "Item 7.1 Transit Oriented Development around the Green Line. "
            "Recommended: approve TOD policy framework. Bill 47 implications discussed."
        ),
        is_new=True,
        is_processed=True,
        first_seen_at=datetime.now(timezone.utc),
    )
    return doc


def _make_municipality(*, id: int = 999, short_name: str = "Calgary") -> MagicMock:
    m = MagicMock()
    m.id = id
    m.short_name = short_name
    m.name = f"City of {short_name}"
    m.province = "Alberta"
    return m


def _make_subscriber(
    *,
    email: str,
    province: str,
    municipalities: list[str],
    topics: list[str],
    keywords: str = "",
) -> MagicMock:
    s = MagicMock()
    s.email = email
    s.province = province
    s.municipalities = municipalities
    s.topics = topics
    s.keywords = keywords
    s.immediate_alerts = True
    s.active = True
    s.unsubscribe_token = "test-unsub-token-uuid"
    return s


def _make_db(*, subscribers: list, municipalities: list) -> AsyncMock:
    """Build an AsyncMock DB whose ``execute`` returns the right results in
    the order ``send_immediate_alerts_for_documents`` calls them.
    """
    db = AsyncMock()

    sub_result = MagicMock()
    sub_result.scalars.return_value.all.return_value = list(subscribers)

    muni_result = MagicMock()
    muni_result.scalars.return_value.all.return_value = list(municipalities)

    call_count = {"n": 0}

    async def fake_execute(_query):
        call_count["n"] += 1
        # 1st call: select active subscribers with immediate_alerts=True
        # 2nd call: select municipalities for the doc municipality_ids
        return sub_result if call_count["n"] == 1 else muni_result

    db.execute = AsyncMock(side_effect=fake_execute)
    return db


@pytest.mark.asyncio
async def test_alberta_subscriber_matches_calgary_document():
    """An AB subscriber selecting Calgary should match a Calgary TOD agenda."""
    doc = _make_calgary_doc()
    muni = _make_municipality(id=doc.municipality_id, short_name="Calgary")

    subscriber = _make_subscriber(
        email="ab-tod@example.com",
        province="Alberta",
        municipalities=["Calgary"],
        topics=["tod"],
    )
    db = _make_db(subscribers=[subscriber], municipalities=[muni])

    with (
        patch("app.services.instant_alerts.settings") as mock_settings,
        patch(
            "app.services.instant_alerts.send_alert_via_smtp",
            return_value=True,
        ) as mock_send,
    ):
        mock_settings.app_base_url = "https://lg-tracker.ca"
        mock_settings.smtp_username = "x"
        mock_settings.smtp_password = "y"

        stats = await send_immediate_alerts_for_documents(db, [doc])

    assert stats["subscribers_checked"] == 1
    assert stats["documents_matched"] >= 1, stats
    assert stats["alerts_sent"] >= 1, stats
    mock_send.assert_called()
    # SMTP was called with our subscriber's email and a real unsubscribe URL.
    kwargs = mock_send.call_args.kwargs
    assert kwargs["to_email"] == "ab-tod@example.com"
    assert "Calgary" in kwargs["municipality_name"]


@pytest.mark.asyncio
async def test_bc_subscriber_does_not_match_calgary_document():
    """A BC subscriber for Vancouver shouldn't get an alert for a Calgary doc.

    Regression guard for the matching boundary — if AB documents leaked into
    BC subscriber alerts, this test would fail. Province is enforced at the
    subscribe step; here we double-check the runtime behaviour by feeding
    only a Calgary document and a BC-Vancouver subscriber.
    """
    doc = _make_calgary_doc()
    muni = _make_municipality(id=doc.municipality_id, short_name="Calgary")

    subscriber = _make_subscriber(
        email="bc-only@example.com",
        province="BC",
        municipalities=["Vancouver"],
        topics=["tod"],
    )
    db = _make_db(subscribers=[subscriber], municipalities=[muni])

    with (
        patch("app.services.instant_alerts.settings") as mock_settings,
        patch(
            "app.services.instant_alerts.send_alert_via_smtp",
            return_value=True,
        ) as mock_send,
    ):
        mock_settings.app_base_url = "https://lg-tracker.ca"

        stats = await send_immediate_alerts_for_documents(db, [doc])

    assert stats["subscribers_checked"] == 1
    assert stats["documents_matched"] == 0
    assert stats["alerts_sent"] == 0
    mock_send.assert_not_called()


@pytest.mark.asyncio
async def test_alberta_subscriber_with_keyword_only_match():
    """Keyword-only matching should also work for AB subscribers — the
    province filter doesn't disable keyword matches.
    """
    doc = _make_calgary_doc()
    muni = _make_municipality(id=doc.municipality_id, short_name="Calgary")

    subscriber = _make_subscriber(
        email="ab-kw@example.com",
        province="Alberta",
        municipalities=["Calgary"],
        topics=[],
        keywords="Green Line",  # appears in our raw_text
    )
    db = _make_db(subscribers=[subscriber], municipalities=[muni])

    with (
        patch("app.services.instant_alerts.settings") as mock_settings,
        patch(
            "app.services.instant_alerts.send_alert_via_smtp",
            return_value=True,
        ),
    ):
        mock_settings.app_base_url = "https://lg-tracker.ca"

        stats = await send_immediate_alerts_for_documents(db, [doc])

    assert stats["alerts_sent"] >= 1, stats
