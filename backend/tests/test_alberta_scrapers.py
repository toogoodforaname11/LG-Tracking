"""Regression tests for Alberta Phase 1 scrapers.

These tests use HTML snapshots captured from real Alberta eSCRIBE deployments
(saved under ``tests/fixtures/alberta/``) so they exercise the full scraper
parse pipeline without depending on the network.

The two snapshots were chosen to cover the two patterns that show up across
the 10 Phase 1 cities:

- **lethbridge_escribe_root.html** — eSCRIBE listing where FileStream agenda
  links are present as ``<a href>`` in the initial HTML. Tests the
  ``EScribeScraper._parse_meeting_list`` strategy.
- **calgary_escribe_root.html** — eSCRIBE listing where the meeting list is
  rendered client-side from JSON inside a Syncfusion grid script tag.
  Tests the ``EScribeScraper._scrape_meetings_from_json`` fallback.

The fixtures were captured on 2026-05-04. They will go stale eventually
(URLs change, FileStream IDs rotate); when they do, regenerate by running:

    SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt curl -L \
        -A 'Mozilla/5.0' "https://pub-lethbridge.escribemeetings.com/" \
        -o backend/tests/fixtures/alberta/lethbridge_escribe_root.html
"""

import os
import re
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.discovery.escribe import EScribeScraper


FIXTURES = Path(__file__).parent / "fixtures" / "alberta"


def _load(name: str) -> str:
    """Read a fixture by filename, or skip the test if it is missing."""
    path = FIXTURES / name
    if not path.exists():
        pytest.skip(f"missing AB fixture {name!r}; run the snapshot command")
    return path.read_text(encoding="utf-8", errors="replace")


def _stub_response(html: str, status_code: int = 200) -> MagicMock:
    resp = MagicMock()
    resp.status_code = status_code
    resp.text = html
    return resp


@pytest.mark.asyncio
async def test_escribe_lethbridge_anchor_path():
    """Lethbridge ships meeting links as <a href> in the initial HTML.

    The normal BeautifulSoup parse path should yield at least one agenda
    pointing at FileStream.ashx — no JSON fallback should be needed.
    """
    html = _load("lethbridge_escribe_root.html")

    scraper = EScribeScraper("Lethbridge", "https://pub-lethbridge.escribemeetings.com")

    # Stub the HTTP client so the test is fully offline. Every GET returns
    # the root fixture HTML; the scraper's per-path retry loop succeeds on
    # the first call.
    scraper.client.get = AsyncMock(return_value=_stub_response(html))
    try:
        items = await scraper.discover()
    finally:
        await scraper.close()

    assert items, "Lethbridge fixture should yield at least one item"

    agenda_urls = [
        item.url
        for item in items
        if item.item_type == "agenda" and "FileStream.ashx" in item.url
    ]
    assert agenda_urls, (
        f"Expected at least one FileStream agenda URL, got: "
        f"{[(i.item_type, i.url[:80]) for i in items[:5]]}"
    )

    # Items must be tagged for the right municipality.
    assert all(item.municipality == "Lethbridge" for item in items)


@pytest.mark.asyncio
async def test_escribe_calgary_yields_filestream_items():
    """Calgary's eSCRIBE root page should yield FileStream agenda items.

    The fixture is a real snapshot from pub-calgary.escribemeetings.com;
    Syncfusion populates the meeting grid client-side, but FileStream.ashx
    document links are still embedded as <a href> by the time the page is
    rendered, so the regular ``_parse_meeting_list`` strategy succeeds.
    Phase 2 will need a deeper fallback when this stops being true.
    """
    html = _load("calgary_escribe_root.html")

    # Sanity check: the fixture contains both meeting and FileStream URLs.
    assert re.search(r"Meeting\.aspx\?Id=[a-fA-F0-9-]{36}", html), \
        "Calgary fixture must contain Meeting.aspx?Id=GUID"
    assert "FileStream.ashx?DocumentId=" in html, \
        "Calgary fixture must contain FileStream.ashx links"

    scraper = EScribeScraper("Calgary", "https://pub-calgary.escribemeetings.com")
    scraper.client.get = AsyncMock(return_value=_stub_response(html))
    try:
        items = await scraper.discover()
    finally:
        await scraper.close()

    assert items, "Calgary fixture should yield at least one item"
    filestream = [i for i in items if "FileStream.ashx" in i.url]
    assert filestream, (
        f"Expected at least one FileStream agenda; got "
        f"{[(i.item_type, i.url[:80]) for i in items[:5]]}"
    )
    assert all(item.municipality == "Calgary" for item in items)


@pytest.mark.asyncio
async def test_escribe_json_fallback_runs_when_anchor_path_yields_nothing():
    """Synthetic test: when the listing page has no parseable <a> tags but
    embeds Meeting.aspx?Id=GUID in JSON, ``_scrape_meetings_from_json``
    should fan out to detail pages.
    """
    json_only_html = """
    <html><body>
    <script>
      var data = {"meetings":[
        {"link":"Meeting.aspx?Id=11111111-2222-3333-4444-555555555555"},
        {"link":"Meeting.aspx?Id=66666666-7777-8888-9999-aaaaaaaaaaaa"}
      ]};
    </script>
    </body></html>
    """
    detail_html = """
    <html><body>
      <a href="FileStream.ashx?DocumentId=999">Agenda Package</a>
    </body></html>
    """

    scraper = EScribeScraper("FakeCity", "https://example.escribemeetings.com")

    # Root call returns the JSON-only HTML; detail calls return the agenda link.
    def _route(url, *args, **kwargs):
        if "Meeting.aspx?Id=" in url:
            return _stub_response(detail_html)
        return _stub_response(json_only_html)

    scraper.client.get = AsyncMock(side_effect=_route)
    try:
        items = await scraper.discover()
    finally:
        await scraper.close()

    # The fallback must have triggered detail fetches and harvested the
    # FileStream agenda link.
    detail_calls = [
        c.args[0] for c in scraper.client.get.call_args_list
        if "Meeting.aspx?Id=" in c.args[0]
    ]
    assert len(detail_calls) >= 1, (
        f"JSON fallback should have requested detail pages; got {scraper.client.get.call_args_list}"
    )
    filestream = [i for i in items if "FileStream.ashx" in i.url]
    assert filestream, "JSON fallback should yield FileStream agenda items from detail pages"


def test_alberta_phase_1_seed_inventory():
    """Sanity-check that every Phase 1 muni still has 3 source rows.

    Phase 1's promise is "10 munis, fully configured". This test fails
    loudly if a muni or source is accidentally deleted from the seed.
    """
    from app.services.seed_registry import ALBERTA_MUNICIPALITIES_PHASE_1

    expected_short_names = {
        "Calgary",
        "Edmonton",
        "Red Deer",
        "Lethbridge",
        "Medicine Hat",
        "Airdrie",
        "Spruce Grove",
        "Grande Prairie",
        "St. Albert",
        "Fort McMurray",
    }
    actual = {m["short_name"] for m in ALBERTA_MUNICIPALITIES_PHASE_1}
    assert actual == expected_short_names, (
        f"Phase 1 inventory drift: missing={expected_short_names - actual}, "
        f"extra={actual - expected_short_names}"
    )

    for muni in ALBERTA_MUNICIPALITIES_PHASE_1:
        assert len(muni["sources"]) == 3, (
            f"{muni['short_name']!r} should have 3 sources, got {len(muni['sources'])}"
        )
