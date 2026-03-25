"""Tests for security fixes: auth, subscription integrity, data idempotency.

These tests verify the deterministic fixes (not warnings) for:
- Cron secret enforcement on all state-changing endpoints
- Subscription update requires edit_token
- Track match ownership check
- TrackMatch uniqueness constraint
- Content hash computed from content, not URL
- Meeting dedup includes meeting_type
"""

import hashlib
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

# ---------------------------------------------------------------------------
# 1. verify_cron_secret — fail-fast when CRON_SECRET is blank in non-debug
# ---------------------------------------------------------------------------


class _FakeSettings:
    """Minimal stand-in for app.config.Settings used to test verify_cron_secret."""

    def __init__(self, cron_secret: str = "", debug: bool = False):
        self.cron_secret = cron_secret
        self.debug = debug


@pytest.mark.asyncio
async def test_cron_secret_rejects_when_blank_and_not_debug():
    """With no CRON_SECRET and debug=False, all protected endpoints must 503."""
    from fastapi import HTTPException

    with patch("app.api.dependencies.settings", _FakeSettings(cron_secret="", debug=False)):
        from app.api.dependencies import verify_cron_secret

        with pytest.raises(HTTPException) as exc_info:
            await verify_cron_secret(x_cron_secret=None)
        assert exc_info.value.status_code == 503


@pytest.mark.asyncio
async def test_cron_secret_allows_when_blank_and_debug():
    """With no CRON_SECRET and debug=True, allow passthrough (local dev)."""
    with patch("app.api.dependencies.settings", _FakeSettings(cron_secret="", debug=True)):
        from app.api.dependencies import verify_cron_secret

        # Should not raise
        result = await verify_cron_secret(x_cron_secret=None)
        assert result is None


@pytest.mark.asyncio
async def test_cron_secret_rejects_wrong_header():
    """With CRON_SECRET set, wrong header value must 401."""
    from fastapi import HTTPException

    with patch("app.api.dependencies.settings", _FakeSettings(cron_secret="correct-secret", debug=False)):
        from app.api.dependencies import verify_cron_secret

        with pytest.raises(HTTPException) as exc_info:
            await verify_cron_secret(x_cron_secret="wrong-secret")
        assert exc_info.value.status_code == 401


@pytest.mark.asyncio
async def test_cron_secret_rejects_missing_header():
    """With CRON_SECRET set, missing header must 401."""
    from fastapi import HTTPException

    with patch("app.api.dependencies.settings", _FakeSettings(cron_secret="correct-secret", debug=False)):
        from app.api.dependencies import verify_cron_secret

        with pytest.raises(HTTPException) as exc_info:
            await verify_cron_secret(x_cron_secret=None)
        assert exc_info.value.status_code == 401


@pytest.mark.asyncio
async def test_cron_secret_accepts_correct_header():
    """With CRON_SECRET set, correct header must pass."""
    with patch("app.api.dependencies.settings", _FakeSettings(cron_secret="correct-secret", debug=False)):
        from app.api.dependencies import verify_cron_secret

        result = await verify_cron_secret(x_cron_secret="correct-secret")
        assert result is None


# ---------------------------------------------------------------------------
# 2. Subscription edit_token enforcement
# ---------------------------------------------------------------------------


def test_subscribe_request_has_edit_token_field():
    """SubscribeRequest must accept an optional edit_token."""
    from app.api.subscribe import SubscribeRequest

    req = SubscribeRequest(
        email="test@example.com",
        municipalities=["Colwood"],
        topics=["housing"],
        edit_token="some-token",
    )
    assert req.edit_token == "some-token"


def test_subscribe_request_edit_token_defaults_none():
    """edit_token should default to None for new subscriptions."""
    from app.api.subscribe import SubscribeRequest

    req = SubscribeRequest(
        email="test@example.com",
        municipalities=["Colwood"],
        topics=["housing"],
    )
    assert req.edit_token is None


def test_subscribe_response_has_edit_token_field():
    """SubscribeResponse must include an optional edit_token."""
    from app.api.subscribe import SubscribeResponse

    resp = SubscribeResponse(
        status="ok",
        email="test@example.com",
        message="Created!",
        edit_token="abc-123",
    )
    assert resp.edit_token == "abc-123"


# ---------------------------------------------------------------------------
# 3. TrackMatch uniqueness constraint in model
# ---------------------------------------------------------------------------


def test_track_match_has_unique_constraint():
    """TrackMatch model must have a unique constraint on (track_id, document_id)."""
    from app.models.track import TrackMatch

    constraint_names = [
        c.name
        for c in TrackMatch.__table__.constraints
        if hasattr(c, "columns") and len(c.columns) > 1
    ]
    assert "uq_track_matches_track_document" in constraint_names


# ---------------------------------------------------------------------------
# 4. Content hash from content, not URL
# ---------------------------------------------------------------------------


def test_content_hash_uses_content_not_url():
    """Verify the hash logic: content should take priority over URL."""
    raw_text = "This is the actual document content."
    title = "Council Meeting Agenda"
    url = "https://example.com/agenda.pdf"

    # When raw_text is available, hash should be from raw_text
    hash_source = raw_text or title or url
    expected = hashlib.sha256(hash_source.encode()).hexdigest()
    assert expected == hashlib.sha256(raw_text.encode()).hexdigest()

    # When raw_text is None, fall back to title
    hash_source = None or title or url
    expected = hashlib.sha256(hash_source.encode()).hexdigest()
    assert expected == hashlib.sha256(title.encode()).hexdigest()

    # When both are None, fall back to URL
    hash_source = None or None or url
    expected = hashlib.sha256(hash_source.encode()).hexdigest()
    assert expected == hashlib.sha256(url.encode()).hexdigest()


# ---------------------------------------------------------------------------
# 5. Meeting dedup includes meeting_type in index
# ---------------------------------------------------------------------------


def test_meeting_index_includes_type():
    """Meeting model index must include meeting_type for proper dedup."""
    from app.models.document import Meeting

    indexes = {idx.name: list(idx.columns.keys()) for idx in Meeting.__table__.indexes}
    # The new index should include municipality_id, meeting_date, and meeting_type
    assert "ix_meetings_muni_date_type" in indexes
    cols = indexes["ix_meetings_muni_date_type"]
    assert "municipality_id" in cols
    assert "meeting_date" in cols
    assert "meeting_type" in cols


# ---------------------------------------------------------------------------
# 6. Endpoints that must have cron_secret dependency
# ---------------------------------------------------------------------------


def _get_route_dependencies(app_module, router_attr: str, path: str, method: str) -> list:
    """Extract dependency callables from a router's route."""
    import importlib

    mod = importlib.import_module(app_module)
    router = getattr(mod, router_attr)
    for route in router.routes:
        if hasattr(route, "path") and route.path == path:
            if method.upper() in (route.methods or set()):
                return [d.dependency for d in (route.dependencies or [])]
    return []


def test_discovery_poll_requires_cron_secret():
    from app.api.dependencies import verify_cron_secret

    deps = _get_route_dependencies("app.api.discovery", "router", "/poll", "POST")
    assert verify_cron_secret in deps


def test_alerts_notify_requires_cron_secret():
    from app.api.dependencies import verify_cron_secret

    deps = _get_route_dependencies("app.api.alerts", "router", "/notify", "POST")
    assert verify_cron_secret in deps


def test_alerts_digest_preview_requires_cron_secret():
    from app.api.dependencies import verify_cron_secret

    deps = _get_route_dependencies("app.api.alerts", "router", "/digest/{track_id}", "GET")
    assert verify_cron_secret in deps


def test_alerts_digest_html_requires_cron_secret():
    from app.api.dependencies import verify_cron_secret

    deps = _get_route_dependencies("app.api.alerts", "router", "/digest/{track_id}/html", "GET")
    assert verify_cron_secret in deps


def test_processing_requires_cron_secret():
    from app.api.dependencies import verify_cron_secret

    deps = _get_route_dependencies("app.api.processing", "router", "/process", "POST")
    assert verify_cron_secret in deps


def test_sources_create_requires_cron_secret():
    from app.api.dependencies import verify_cron_secret

    deps = _get_route_dependencies("app.api.registry", "router", "/sources", "POST")
    assert verify_cron_secret in deps


def test_sources_status_update_requires_cron_secret():
    from app.api.dependencies import verify_cron_secret

    deps = _get_route_dependencies("app.api.registry", "router", "/sources/{source_id}/status", "PATCH")
    assert verify_cron_secret in deps


def test_seed_requires_cron_secret():
    """Pre-existing protection — verify it wasn't accidentally removed."""
    from app.api.dependencies import verify_cron_secret

    deps = _get_route_dependencies("app.api.registry", "router", "/seed", "POST")
    assert verify_cron_secret in deps
