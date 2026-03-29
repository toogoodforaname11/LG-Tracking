"""Tests for custom CRD municipality scrapers and poller dispatch."""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock

from app.discovery.custom_saanich import SaanichScraper
from app.discovery.custom_sidney import SidneyScraper
from app.discovery.custom_esquimalt import EsquimaltScraper
from app.discovery.custom_viewroyal import ViewRoyalScraper
from app.discovery.custom_langford import LangfordScraper
from app.discovery.custom_highlands import HighlandsScraper
from app.discovery.custom_crd import CRDScraper, classify_crd_meeting_type
from app.discovery.civicweb import parse_civicweb_date, _extract_date, _classify_link
from app.discovery.poller import CUSTOM_SCRAPER_MAP, _get_custom_scraper


# --- CivicWeb helper tests (new helpers added in this batch) ---


def test_extract_date():
    assert _extract_date("Meeting on March 9, 2026 at 7pm") == "2026-03-09"
    assert _extract_date("2026-03-09 Regular Council") == "2026-03-09"
    assert _extract_date("Monday, March 9, 2026") == "2026-03-09"
    assert _extract_date("no date here") is None


def test_classify_link():
    assert _classify_link("Agenda Package", "/doc.pdf") == "agenda"
    assert _classify_link("Minutes", "/minutes.pdf") == "minutes"
    assert _classify_link("Watch Recording", "/video") == "video"
    assert _classify_link("Some Link", "https://youtube.com/watch?v=abc") == "video"
    assert _classify_link("Some Link", "/page.html") is None
    assert _classify_link("View Agenda", "/meeting/agenda") == "agenda"


def test_parse_civicweb_date_new_formats():
    """Test additional date formats added in the CivicWeb update."""
    assert parse_civicweb_date("March 9 2026") == "2026-03-09"
    assert parse_civicweb_date("09-March-2026") == "2026-03-09"


# --- CRD meeting type classification ---


def test_classify_crd_meeting_type():
    assert classify_crd_meeting_type("Board Meeting") == "regular"
    assert classify_crd_meeting_type("Finance Committee") == "committee"
    assert classify_crd_meeting_type("Planning Committee") == "committee"
    assert classify_crd_meeting_type("Public Hearing") == "public_hearing"
    assert classify_crd_meeting_type("Committee of the Whole") == "committee_of_the_whole"
    assert classify_crd_meeting_type("Special Meeting") == "special"
    assert classify_crd_meeting_type("Regional Water Committee") == "committee"


# --- Custom scraper registry ---


def test_custom_scraper_map_has_all_crd():
    crd_expected = {"Saanich", "Sidney", "Esquimalt", "View Royal", "Langford", "Highlands", "CRD"}
    assert crd_expected.issubset(set(CUSTOM_SCRAPER_MAP.keys()))


def test_get_custom_scraper_returns_correct_type():
    scraper = _get_custom_scraper("Saanich", "https://example.com")
    assert isinstance(scraper, SaanichScraper)

    scraper = _get_custom_scraper("CRD", "https://example.com")
    assert isinstance(scraper, CRDScraper)

    scraper = _get_custom_scraper("Unknown", "https://example.com")
    assert scraper is None


# --- Scraper instantiation ---


def test_all_scrapers_extend_base():
    """All custom scrapers should instantiate and have a discover method."""
    from app.discovery.base import BaseScraper

    scrapers = [
        SaanichScraper("Saanich", "https://example.com"),
        SidneyScraper("Sidney", "https://example.com"),
        EsquimaltScraper("Esquimalt", "https://example.com"),
        ViewRoyalScraper("View Royal", "https://example.com"),
        LangfordScraper("Langford", "https://example.com"),
        HighlandsScraper("Highlands", "https://example.com"),
        CRDScraper("CRD", "https://example.com"),
    ]
    for scraper in scrapers:
        assert isinstance(scraper, BaseScraper)
        assert hasattr(scraper, "discover")
        assert callable(scraper.discover)


# --- Date/link classification on individual scrapers ---


def test_saanich_classify_link():
    assert SaanichScraper._classify_link("View Agenda", "/doc.pdf") == "agenda"
    assert SaanichScraper._classify_link("Council Minutes", "/doc.pdf") == "minutes"
    assert SaanichScraper._classify_link("Random Link", "/page.html") is None


def test_saanich_extract_date():
    assert SaanichScraper._extract_date("January 15, 2026 Council") == "2026-01-15"
    assert SaanichScraper._extract_date("2026-01-15") == "2026-01-15"
    assert SaanichScraper._extract_date("no date") is None


def test_crd_classify_link():
    assert CRDScraper._classify_link("Board Agenda", "/board.pdf") == "agenda"
    assert CRDScraper._classify_link("Minutes of Meeting", "/minutes.pdf") == "minutes"
    assert CRDScraper._classify_link("Webcast", "/webcast") == "video"


# --- HTML parsing tests ---


SAMPLE_TABLE_HTML = """
<html><body>
<table>
<tr>
    <td>March 9, 2026</td>
    <td>Regular Council Meeting</td>
    <td><a href="/agendas/2026-03-09-agenda.pdf">Agenda</a></td>
    <td><a href="/minutes/2026-03-09-minutes.pdf">Minutes</a></td>
</tr>
<tr>
    <td>February 23, 2026</td>
    <td>Special Meeting</td>
    <td><a href="/agendas/2026-02-23-agenda.pdf">Agenda Package</a></td>
</tr>
</table>
</body></html>
"""


@pytest.mark.asyncio
async def test_saanich_parse_table_html():
    scraper = SaanichScraper("Saanich", "https://www.saanich.ca/test")
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(SAMPLE_TABLE_HTML, "lxml")
    items = scraper._parse_page(soup)
    assert len(items) >= 3  # 2 from first row + 1 from second row
    assert any(i.item_type == "agenda" for i in items)
    assert any(i.item_type == "minutes" for i in items)
    assert any(i.meeting_date == "2026-03-09" for i in items)


@pytest.mark.asyncio
async def test_crd_parse_table_html():
    scraper = CRDScraper("CRD", "https://www.crd.bc.ca/test")
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(SAMPLE_TABLE_HTML, "lxml")
    items = scraper._parse_page(soup, "https://www.crd.bc.ca/test")
    assert len(items) >= 2
    assert any(i.item_type == "agenda" for i in items)


SAMPLE_LIST_HTML = """
<html><body>
<ul>
    <li>
        <a href="/docs/agenda-jan-2026.pdf">January 12, 2026 Agenda</a>
    </li>
    <li>
        <a href="/docs/minutes-jan-2026.pdf">January 12, 2026 Minutes</a>
    </li>
    <li>
        <a href="https://youtube.com/watch?v=abc">Watch Recording</a>
    </li>
</ul>
</body></html>
"""


@pytest.mark.asyncio
async def test_esquimalt_parse_list_html():
    scraper = EsquimaltScraper("Esquimalt", "https://www.esquimalt.ca/test")
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(SAMPLE_LIST_HTML, "lxml")
    items = scraper._parse_page(soup, "https://www.esquimalt.ca/test")
    assert len(items) >= 3
    types = {i.item_type for i in items}
    assert "agenda" in types
    assert "minutes" in types
    assert "video" in types
