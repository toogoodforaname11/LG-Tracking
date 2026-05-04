"""Integration tests for the subscription lifecycle:
subscribe -> confirm -> update preferences -> unsubscribe.

Tests the full flow using mocked DB sessions and SMTP email service.
"""

import uuid
from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi import HTTPException

from app.api.subscribe import (
    subscribe,
    unsubscribe,
    SubscribeRequest,
    MAGIC_LINK_TTL_HOURS,
)
from app.api.auth import confirm_magic_link


def _muni_validation_result(known_short_names):
    """Build the result returned by the municipality-existence check.

    The subscribe handler runs ``select(Municipality.short_name).where(...)``
    and consumes the result via ``scalars().all()``; this helper produces a
    MagicMock that satisfies that exact shape with the supplied known names.
    """
    result = MagicMock()
    scalars = MagicMock()
    scalars.all.return_value = list(known_short_names)
    result.scalars.return_value = scalars
    return result


def _make_subscribe_db_mock(*, existing_subscriber, known_municipalities):
    """Build an AsyncMock DB whose ``execute`` returns the right results in
    the order the subscribe handler calls them: (1) municipality validation,
    (2) existing subscriber lookup.

    Subsequent execute calls (none today) reuse the subscriber-lookup result
    so tests don't crash if the production code ever adds another query.
    Also installs a ``refresh`` impl that backfills SQLAlchemy server defaults
    (``unsubscribe_token`` on Subscriber and ``token`` on MagicLinkToken)
    which would normally only populate after a flush against a real DB.
    """
    db = AsyncMock()
    # db.add is a synchronous SQLAlchemy method; AsyncMock turns every
    # attribute into a coroutine by default which leaks RuntimeWarnings when
    # the production code (correctly) does not await it.
    db.add = MagicMock()
    db.commit = AsyncMock()

    sub_result = MagicMock()
    sub_result.scalar_one_or_none.return_value = existing_subscriber
    muni_result = _muni_validation_result(known_municipalities)

    call_count = {"n": 0}

    async def fake_execute(_query):
        call_count["n"] += 1
        # First call validates municipalities, second looks up the subscriber.
        if call_count["n"] == 1:
            return muni_result
        return sub_result

    db.execute = AsyncMock(side_effect=fake_execute)

    async def fake_refresh(obj):
        if hasattr(obj, "unsubscribe_token") and getattr(obj, "unsubscribe_token", None) is None:
            obj.unsubscribe_token = str(uuid.uuid4())
        if hasattr(obj, "token") and getattr(obj, "token", None) is None:
            obj.token = str(uuid.uuid4())

    db.refresh = AsyncMock(side_effect=fake_refresh)
    return db


# --- Helpers ---


def _make_subscriber(**kwargs):
    """Create a mock Subscriber."""
    sub = MagicMock()
    sub.email = kwargs.get("email", "test@example.com")
    sub.municipalities = kwargs.get("municipalities", ["Colwood", "Victoria"])
    sub.topics = kwargs.get("topics", ["ocp_housing", "zoning_density"])
    sub.keywords = kwargs.get("keywords", "rezoning")
    sub.immediate_alerts = kwargs.get("immediate_alerts", False)
    sub.active = kwargs.get("active", True)
    sub.province = kwargs.get("province", "BC")
    sub.unsubscribe_token = kwargs.get("unsubscribe_token", str(uuid.uuid4()))
    sub.created_at = datetime.now(timezone.utc)
    sub.updated_at = datetime.now(timezone.utc)
    return sub


def _make_magic_link_token(email="test@example.com", **kwargs):
    """Create a mock MagicLinkToken."""
    token = MagicMock()
    token.id = kwargs.get("id", 1)
    token.token = kwargs.get("token", str(uuid.uuid4()))
    token.email = email
    token.pending_preferences = kwargs.get("pending_preferences", {
        "municipalities": ["Saanich"],
        "topics": ["tod"],
        "keywords": "transit",
        "immediate_alerts": True,
    })
    token.expires_at = kwargs.get(
        "expires_at",
        datetime.now(timezone.utc) + timedelta(hours=MAGIC_LINK_TTL_HOURS),
    )
    token.used_at = kwargs.get("used_at", None)
    token.is_valid = kwargs.get("is_valid", True)
    token.created_at = datetime.now(timezone.utc)
    return token


def _make_subscribe_request(**kwargs):
    return SubscribeRequest(
        email=kwargs.get("email", "new@example.com"),
        municipalities=kwargs.get("municipalities", ["Colwood"]),
        topics=kwargs.get("topics", ["ocp_housing"]),
        keywords=kwargs.get("keywords", ""),
        immediate_alerts=kwargs.get("immediate_alerts", False),
        province=kwargs.get("province", "BC"),
    )


# --- New subscriber flow ---


@pytest.mark.asyncio
async def test_new_subscriber_created():
    """New email should create subscriber and send confirmation magic link."""
    db = _make_subscribe_db_mock(
        existing_subscriber=None,
        known_municipalities=["Colwood"],
    )
    background_tasks = MagicMock()

    req = _make_subscribe_request()

    with patch("app.api.subscribe.settings") as mock_settings:
        mock_settings.app_base_url = "https://example.com"
        mock_settings.smtp_username = "test@example.com"
        mock_settings.smtp_password = "test-password"

        response = await subscribe(req, background_tasks, db)

    # All subscribe paths now go through the magic-link flow (double opt-in).
    assert response.status == "magic_link_sent"
    assert response.email == "new@example.com"
    assert db.add.called
    assert db.commit.called


@pytest.mark.asyncio
async def test_new_subscriber_sends_confirmation_email():
    """New subscriber should trigger a confirmation magic-link email."""
    db = _make_subscribe_db_mock(
        existing_subscriber=None,
        known_municipalities=["Colwood"],
    )
    background_tasks = MagicMock()

    req = _make_subscribe_request()

    with patch("app.api.subscribe.settings") as mock_settings:
        mock_settings.app_base_url = "https://example.com"

        await subscribe(req, background_tasks, db)

    background_tasks.add_task.assert_called_once()
    task_args = background_tasks.add_task.call_args
    # First positional arg is the email-sending function used for new
    # subscribers — must match the actual function exported by the module.
    assert task_args[0][0].__name__ == "send_confirmation_link_email"


# --- Existing subscriber flow (magic link) ---


@pytest.mark.asyncio
async def test_existing_subscriber_gets_magic_link():
    """Existing email should create a magic link token, not modify subscriber directly."""
    existing = _make_subscriber()
    db = _make_subscribe_db_mock(
        existing_subscriber=existing,
        known_municipalities=["Colwood"],
    )
    background_tasks = MagicMock()

    req = _make_subscribe_request(email="test@example.com")

    with patch("app.api.subscribe.settings") as mock_settings:
        mock_settings.app_base_url = "https://example.com"

        response = await subscribe(req, background_tasks, db)

    assert response.status == "magic_link_sent"
    assert db.add.called
    background_tasks.add_task.assert_called_once()
    # Existing-subscriber path uses the magic-link template, not the
    # confirmation template.
    task_args = background_tasks.add_task.call_args
    assert task_args[0][0].__name__ == "send_magic_link_email"


# --- Magic link confirmation ---


@pytest.mark.asyncio
async def test_confirm_magic_link_applies_preferences():
    """Valid magic link should apply pending preferences to subscriber."""
    token = _make_magic_link_token()
    subscriber = _make_subscriber()

    db = AsyncMock()

    call_count = 0

    async def mock_execute(query):
        nonlocal call_count
        call_count += 1
        result = MagicMock()
        if call_count == 1:
            result.scalar_one_or_none.return_value = token
        else:
            result.scalar_one_or_none.return_value = subscriber
        return result

    db.execute = AsyncMock(side_effect=mock_execute)
    db.commit = AsyncMock()

    with patch("app.api.auth.settings") as mock_settings:
        mock_settings.app_base_url = ""  # No redirect, returns JSON

        result = await confirm_magic_link(token.token, db)

    assert result["status"] == "ok"
    # Preferences should be applied
    assert subscriber.municipalities == ["Saanich"]
    assert subscriber.topics == ["tod"]
    assert subscriber.keywords == "transit"
    assert subscriber.immediate_alerts is True
    assert subscriber.active is True
    # Token should be consumed
    assert token.used_at is not None


@pytest.mark.asyncio
async def test_confirm_magic_link_invalid_token():
    """Unknown token should return 404."""
    db = AsyncMock()
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = None
    db.execute = AsyncMock(return_value=mock_result)

    with pytest.raises(HTTPException) as exc_info:
        await confirm_magic_link("invalid-token", db)

    assert exc_info.value.status_code == 404


@pytest.mark.asyncio
async def test_confirm_magic_link_expired_token():
    """Expired or used token should return 410."""
    token = _make_magic_link_token(is_valid=False)

    db = AsyncMock()
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = token
    db.execute = AsyncMock(return_value=mock_result)

    with pytest.raises(HTTPException) as exc_info:
        await confirm_magic_link(token.token, db)

    assert exc_info.value.status_code == 410


@pytest.mark.asyncio
async def test_confirm_magic_link_deleted_subscriber():
    """If subscriber was deleted after token creation, should return 404."""
    token = _make_magic_link_token()

    db = AsyncMock()
    call_count = 0

    async def mock_execute(query):
        nonlocal call_count
        call_count += 1
        result = MagicMock()
        if call_count == 1:
            result.scalar_one_or_none.return_value = token
        else:
            result.scalar_one_or_none.return_value = None  # subscriber deleted
        return result

    db.execute = AsyncMock(side_effect=mock_execute)

    with pytest.raises(HTTPException) as exc_info:
        await confirm_magic_link(token.token, db)

    assert exc_info.value.status_code == 404


# --- Unsubscribe ---


@pytest.mark.asyncio
async def test_unsubscribe_deactivates_subscriber():
    """Valid unsubscribe token should set active=False."""
    subscriber = _make_subscriber()

    db = AsyncMock()
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = subscriber
    db.execute = AsyncMock(return_value=mock_result)
    db.commit = AsyncMock()

    result = await unsubscribe(subscriber.unsubscribe_token, db)

    assert result.status == "ok"
    assert subscriber.active is False


@pytest.mark.asyncio
async def test_unsubscribe_invalid_token():
    """Unknown unsubscribe token should return 404."""
    db = AsyncMock()
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = None
    db.execute = AsyncMock(return_value=mock_result)

    with pytest.raises(HTTPException) as exc_info:
        await unsubscribe("invalid-token", db)

    assert exc_info.value.status_code == 404


# --- Immediate alerts preference ---


@pytest.mark.asyncio
async def test_new_subscriber_with_immediate_alerts():
    """Subscriber with immediate_alerts=True still goes through magic link."""
    db = _make_subscribe_db_mock(
        existing_subscriber=None,
        known_municipalities=["Colwood"],
    )
    background_tasks = MagicMock()

    req = _make_subscribe_request(immediate_alerts=True)

    with patch("app.api.subscribe.settings") as mock_settings:
        mock_settings.app_base_url = "https://example.com"

        response = await subscribe(req, background_tasks, db)

    assert response.status == "magic_link_sent"
    # Either path should send a confirmation email.
    background_tasks.add_task.assert_called_once()


# --- Province handling ---


@pytest.mark.asyncio
async def test_subscribe_with_alberta_province():
    """Alberta subscription should validate against AB munis and persist province."""
    db = _make_subscribe_db_mock(
        existing_subscriber=None,
        known_municipalities=["Calgary", "Edmonton"],
    )
    background_tasks = MagicMock()

    req = _make_subscribe_request(
        email="ab@example.com",
        province="Alberta",
        municipalities=["Calgary", "Edmonton"],
    )

    with patch("app.api.subscribe.settings") as mock_settings:
        mock_settings.app_base_url = "https://example.com"

        response = await subscribe(req, background_tasks, db)

    assert response.status == "magic_link_sent"
    # The newly-added Subscriber model object should carry province="Alberta".
    from app.models.subscriber import Subscriber as SubscriberModel
    from app.models.magic_link import MagicLinkToken as TokenModel

    added_objects = [call.args[0] for call in db.add.call_args_list]
    new_subs = [o for o in added_objects if isinstance(o, SubscriberModel)]
    assert len(new_subs) == 1
    assert new_subs[0].province == "Alberta"
    assert new_subs[0].email == "ab@example.com"
    # The magic-link token should also remember the province for replay-safety.
    tokens = [o for o in added_objects if isinstance(o, TokenModel)]
    assert len(tokens) == 1
    assert tokens[0].pending_preferences["province"] == "Alberta"


def test_subscribe_request_rejects_unknown_province():
    """Pydantic should reject province values outside VALID_PROVINCES."""
    with pytest.raises(Exception):
        SubscribeRequest(
            email="x@example.com",
            municipalities=["Toronto"],
            topics=[],
            province="Ontario",  # not supported
        )


@pytest.mark.asyncio
async def test_subscribe_rejects_municipality_outside_province():
    """Posting Calgary with province=BC should be a 422."""
    db = _make_subscribe_db_mock(
        existing_subscriber=None,
        # The validation query in the BC branch wouldn't return Calgary
        # because Calgary lives in Alberta — simulate that here.
        known_municipalities=[],
    )
    background_tasks = MagicMock()

    req = _make_subscribe_request(
        email="bad@example.com",
        province="BC",
        municipalities=["Calgary"],
    )

    with pytest.raises(HTTPException) as exc_info:
        await subscribe(req, background_tasks, db)

    assert exc_info.value.status_code == 422
    assert "Calgary" in str(exc_info.value.detail)


@pytest.mark.asyncio
async def test_confirm_magic_link_applies_province():
    """Magic-link confirmation should propagate province from pending_preferences."""
    token = _make_magic_link_token(pending_preferences={
        "municipalities": ["Calgary"],
        "topics": ["tod"],
        "keywords": "",
        "immediate_alerts": False,
        "province": "Alberta",
    })
    subscriber = _make_subscriber(province="BC")

    db = AsyncMock()
    call_count = 0

    async def mock_execute(_query):
        nonlocal call_count
        call_count += 1
        result = MagicMock()
        if call_count == 1:
            result.scalar_one_or_none.return_value = token
        else:
            result.scalar_one_or_none.return_value = subscriber
        return result

    db.execute = AsyncMock(side_effect=mock_execute)
    db.commit = AsyncMock()

    with patch("app.api.auth.settings") as mock_settings:
        mock_settings.app_base_url = ""

        result = await confirm_magic_link(token.token, db)

    assert result["status"] == "ok"
    assert subscriber.province == "Alberta"
    assert subscriber.municipalities == ["Calgary"]
