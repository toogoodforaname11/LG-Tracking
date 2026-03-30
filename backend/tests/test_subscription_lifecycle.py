"""Integration tests for the subscription lifecycle:
subscribe -> confirm -> update preferences -> unsubscribe.

Tests the full flow using mocked DB sessions and Resend email service.
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
    )


# --- New subscriber flow ---


@pytest.mark.asyncio
async def test_new_subscriber_created():
    """New email should create subscriber immediately with status='created'."""
    db = AsyncMock()
    background_tasks = MagicMock()

    # No existing subscriber
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = None
    db.execute = AsyncMock(return_value=mock_result)
    db.commit = AsyncMock()

    # db.refresh needs to set the unsubscribe_token (SQLAlchemy default
    # only fires at flush, not __init__)
    async def fake_refresh(obj):
        if hasattr(obj, "unsubscribe_token") and obj.unsubscribe_token is None:
            obj.unsubscribe_token = str(uuid.uuid4())

    db.refresh = AsyncMock(side_effect=fake_refresh)

    req = _make_subscribe_request()

    with patch("app.api.subscribe.settings") as mock_settings:
        mock_settings.app_base_url = "https://example.com"
        mock_settings.resend_api_key = "test-key"

        response = await subscribe(req, background_tasks, db)

    assert response.status == "created"
    assert response.email == "new@example.com"
    assert db.add.called
    assert db.commit.called


@pytest.mark.asyncio
async def test_new_subscriber_sends_confirmation_email():
    """New subscriber should trigger a confirmation email via BackgroundTasks."""
    db = AsyncMock()
    background_tasks = MagicMock()

    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = None
    db.execute = AsyncMock(return_value=mock_result)
    db.commit = AsyncMock()

    async def fake_refresh(obj):
        if hasattr(obj, "unsubscribe_token") and obj.unsubscribe_token is None:
            obj.unsubscribe_token = str(uuid.uuid4())

    db.refresh = AsyncMock(side_effect=fake_refresh)

    req = _make_subscribe_request()

    with patch("app.api.subscribe.settings") as mock_settings:
        mock_settings.app_base_url = "https://example.com"

        response = await subscribe(req, background_tasks, db)

    background_tasks.add_task.assert_called_once()
    task_args = background_tasks.add_task.call_args
    # First arg is the function (send_confirmation_email)
    assert task_args[0][0].__name__ == "send_confirmation_email"


@pytest.mark.asyncio
async def test_new_subscriber_skips_email_without_base_url():
    """Without APP_BASE_URL, confirmation email should be skipped."""
    db = AsyncMock()
    background_tasks = MagicMock()

    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = None
    db.execute = AsyncMock(return_value=mock_result)
    db.commit = AsyncMock()
    db.refresh = AsyncMock()

    req = _make_subscribe_request()

    with patch("app.api.subscribe.settings") as mock_settings:
        mock_settings.app_base_url = ""

        response = await subscribe(req, background_tasks, db)

    assert response.status == "created"
    background_tasks.add_task.assert_not_called()


# --- Existing subscriber flow (magic link) ---


@pytest.mark.asyncio
async def test_existing_subscriber_gets_magic_link():
    """Existing email should create a magic link token, not modify subscriber directly."""
    db = AsyncMock()
    background_tasks = MagicMock()

    existing = _make_subscriber()
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = existing
    db.execute = AsyncMock(return_value=mock_result)
    db.commit = AsyncMock()

    async def fake_refresh(obj):
        if hasattr(obj, "token") and obj.token is None:
            obj.token = str(uuid.uuid4())

    db.refresh = AsyncMock(side_effect=fake_refresh)

    req = _make_subscribe_request(email="test@example.com")

    with patch("app.api.subscribe.settings") as mock_settings:
        mock_settings.app_base_url = "https://example.com"

        response = await subscribe(req, background_tasks, db)

    assert response.status == "magic_link_sent"
    assert db.add.called
    background_tasks.add_task.assert_called_once()


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
    """Subscriber with immediate_alerts=True should get appropriate message."""
    db = AsyncMock()
    background_tasks = MagicMock()

    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = None
    db.execute = AsyncMock(return_value=mock_result)
    db.commit = AsyncMock()

    async def fake_refresh(obj):
        if hasattr(obj, "unsubscribe_token") and obj.unsubscribe_token is None:
            obj.unsubscribe_token = str(uuid.uuid4())

    db.refresh = AsyncMock(side_effect=fake_refresh)

    req = _make_subscribe_request(immediate_alerts=True)

    with patch("app.api.subscribe.settings") as mock_settings:
        mock_settings.app_base_url = "https://example.com"

        response = await subscribe(req, background_tasks, db)

    assert response.status == "created"
    assert "immediate alerts" in response.message.lower()
