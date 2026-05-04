"""Test YouTube timestamp extraction."""

from app.discovery.youtube import parse_timestamps, format_timestamps_for_embedding


def test_parse_timestamps_basic():
    desc = """City of Colwood Regular Council Meeting - March 9, 2026

0:00:00 Call to Order
0:02:15 Adoption of Agenda
0:15:30 Public Hearing - OCP Amendment Bylaw 1234
1:02:15 Rezoning Application - 123 Main St
1:45:00 New Business
2:10:30 Adjournment"""

    timestamps = parse_timestamps(desc)
    assert len(timestamps) == 6
    assert timestamps[0]["t"] == "0:00:00"
    assert timestamps[0]["seconds"] == 0
    assert timestamps[0]["label"] == "Call to Order"
    assert timestamps[2]["t"] == "0:15:30"
    assert timestamps[2]["seconds"] == 930
    assert "Public Hearing" in timestamps[2]["label"]
    assert timestamps[3]["seconds"] == 3735


def test_parse_timestamps_with_dashes():
    desc = """
0:05:00 - Welcome
0:10:00 – Budget Discussion
0:30:00 — Climate Action Report
"""
    timestamps = parse_timestamps(desc)
    assert len(timestamps) == 3
    assert timestamps[0]["label"] == "Welcome"
    assert timestamps[1]["label"] == "Budget Discussion"


def test_parse_timestamps_mm_ss_format():
    desc = """
15:30 Rezoning Vote
45:00 Council Break
"""
    timestamps = parse_timestamps(desc)
    assert len(timestamps) == 2
    assert timestamps[0]["seconds"] == 930
    assert timestamps[1]["seconds"] == 2700


def test_parse_timestamps_empty():
    assert parse_timestamps("No timestamps here") == []
    assert parse_timestamps("") == []


def test_format_timestamps_for_embedding():
    timestamps = [
        {"t": "0:15:30", "seconds": 930, "label": "Public Hearing - OCP"},
        {"t": "1:02:15", "seconds": 3735, "label": "Rezoning Application"},
    ]
    result = format_timestamps_for_embedding(timestamps, "https://www.youtube.com/watch?v=abc123")
    assert "VIDEO CHAPTERS/TIMESTAMPS:" in result
    assert "[0:15:30] Public Hearing - OCP" in result
    assert "t=930" in result
    assert "t=3735" in result


def test_format_timestamps_empty():
    assert format_timestamps_for_embedding([], "https://youtube.com/watch?v=x") == ""


# --- Channel-id resolver ---

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from app.discovery.youtube import resolve_channel_id


@pytest.mark.asyncio
async def test_resolve_channel_id_passes_through_real_id():
    """A real UCxxx id should be returned without any HTTP call."""
    real = "UC" + "X" * 22
    with patch("app.discovery.youtube.httpx.AsyncClient") as MockClient:
        result = await resolve_channel_id(real)
        assert result == real
        MockClient.assert_not_called()


def _stub_async_client(html: str | None, *, raise_on_get: bool = False):
    """Return a context-manager mock for ``httpx.AsyncClient`` that yields a
    fake response with ``html`` (or raises when ``raise_on_get`` is True).
    """
    fake_client = AsyncMock()
    if raise_on_get:
        fake_client.get = AsyncMock(side_effect=RuntimeError("boom"))
    else:
        resp = MagicMock(text=html or "")
        resp.raise_for_status = MagicMock()
        fake_client.get = AsyncMock(return_value=resp)
    fake_client.__aenter__.return_value = fake_client
    fake_client.__aexit__.return_value = None
    return fake_client


@pytest.mark.asyncio
async def test_resolve_channel_id_handles_handle_url():
    """A /@handle URL should be fetched and parsed for channelId."""
    fake_id = "UC" + "A" * 22
    html = f'<html>... "channelId":"{fake_id}" ... </html>'
    client = _stub_async_client(html)
    with patch("app.discovery.youtube.httpx.AsyncClient", return_value=client):
        result = await resolve_channel_id("https://www.youtube.com/@CityofCalgary")
    assert result == fake_id


@pytest.mark.asyncio
async def test_resolve_channel_id_returns_none_on_network_failure():
    """Network errors should produce None, not raise."""
    client = _stub_async_client(None, raise_on_get=True)
    with patch("app.discovery.youtube.httpx.AsyncClient", return_value=client):
        result = await resolve_channel_id("https://www.youtube.com/@DoesNotExist")
    assert result is None


@pytest.mark.asyncio
async def test_resolve_channel_id_returns_none_when_no_id_on_page():
    """If the resolver page has no UCxxx token, return None."""
    client = _stub_async_client("<html>nothing useful</html>")
    with patch("app.discovery.youtube.httpx.AsyncClient", return_value=client):
        result = await resolve_channel_id("@NoChannelHere")
    assert result is None


@pytest.mark.asyncio
async def test_resolve_channel_id_handles_meta_itemprop_form():
    """meta itemprop=channelId is the most reliable signal — must be parsed."""
    fake_id = "UC" + "M" * 22
    html = f'<meta itemprop="channelId" content="{fake_id}">'
    client = _stub_async_client(html)
    with patch("app.discovery.youtube.httpx.AsyncClient", return_value=client):
        result = await resolve_channel_id("https://www.youtube.com/@WithMeta")
    assert result == fake_id
