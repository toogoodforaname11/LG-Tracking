"""Tests for Batch 2 scrapers: Granicus platform, BCMunicipal base, and 4 custom scrapers."""

import pytest
from bs4 import BeautifulSoup

from app.discovery.base import BaseScraper
from app.discovery.granicus import GranicusScraper, _extract_date, _classify_link
from app.discovery.custom_bc_municipal import (
    BCMunicipalScraper,
    extract_date as bc_extract_date,
    classify_link as bc_classify_link,
    GENERIC_SCRAPER_KEYWORDS,
    make_generic_scraper,
)
from app.discovery.poller import CUSTOM_SCRAPER_MAP, _get_custom_scraper


# --- Granicus helper tests ---


def test_granicus_extract_date():
    assert _extract_date("March 10, 2026 Regular Council") == "2026-03-10"
    assert _extract_date("2026-03-10") == "2026-03-10"
    assert _extract_date("no date") is None


def test_granicus_classify_link():
    assert _classify_link("Agenda", "/doc.pdf") == "agenda"
    assert _classify_link("Minutes", "/doc.pdf") == "minutes"
    assert _classify_link("View", "/MetaViewer.php?id=1") == "agenda"
    assert _classify_link("Minutes", "/MetaViewer.php?id=2") == "minutes"
    assert _classify_link("View", "/GeneratedAgendaViewer.php?id=1") == "agenda"
    assert _classify_link("Random", "/page.html") is None


def test_granicus_classify_video_links():
    assert _classify_link("Watch Recording", "/video") == "video"
    assert _classify_link("Link", "https://youtube.com/watch?v=x") == "video"


# --- BCMunicipal base class helpers ---


def test_bc_extract_date():
    assert bc_extract_date("January 20, 2026 Council") == "2026-01-20"
    assert bc_extract_date("2026-01-20") == "2026-01-20"
    assert bc_extract_date("no date here") is None


def test_bc_classify_link():
    assert bc_classify_link("View Agenda", "/doc.pdf") == "agenda"
    assert bc_classify_link("Minutes of Council", "/doc.pdf") == "minutes"
    assert bc_classify_link("Watch", "https://youtube.com/x") == "video"
    assert bc_classify_link("Random", "/page.html") is None
    # PDF near meeting content should classify
    assert bc_classify_link("Council Meeting", "/doc.pdf") == "agenda"


# --- Scraper instantiation ---


def test_granicus_extends_base():
    scraper = GranicusScraper("Campbell River", "https://campbellriver.ca.granicus.com")
    assert isinstance(scraper, BaseScraper)
    assert hasattr(scraper, "discover")


def test_bc_municipal_extends_base():
    scraper = BCMunicipalScraper("Test", "https://example.com")
    assert isinstance(scraper, BaseScraper)


def test_generic_scrapers_extend_bc_municipal():
    """Config-driven generic scrapers should be BCMunicipalScraper instances."""
    for name in ["100 Mile House", "Armstrong", "Castlegar", "Enderby"]:
        scraper = make_generic_scraper(name, "https://example.com")
        assert scraper is not None, f"No generic scraper for {name}"
        assert isinstance(scraper, BCMunicipalScraper)
        assert isinstance(scraper, BaseScraper)
        assert hasattr(scraper, "discover")


# --- Custom scraper map updated ---


def test_batch2_custom_scrapers_in_config():
    assert "100 Mile House" in GENERIC_SCRAPER_KEYWORDS
    assert "Armstrong" in GENERIC_SCRAPER_KEYWORDS
    assert "Castlegar" in GENERIC_SCRAPER_KEYWORDS
    assert "Enderby" in GENERIC_SCRAPER_KEYWORDS


def test_get_custom_scraper_batch2():
    scraper = _get_custom_scraper("100 Mile House", "https://example.com")
    assert isinstance(scraper, BCMunicipalScraper)

    scraper = _get_custom_scraper("Armstrong", "https://example.com")
    assert isinstance(scraper, BCMunicipalScraper)


# --- HTML parsing tests ---


GRANICUS_TABLE_HTML = """
<html><body>
<table>
<tr>
    <td>March 10, 2026</td>
    <td>Regular Council Meeting</td>
    <td><a href="/GeneratedAgendaViewer.php?view_id=1&clip_id=100">Agenda</a></td>
    <td><a href="/MetaViewer.php?view_id=2&clip_id=100">Minutes</a></td>
</tr>
<tr>
    <td>February 24, 2026</td>
    <td>Special Meeting</td>
    <td><a href="/agendas/2026-02-24.pdf">Agenda Package</a></td>
</tr>
</table>
</body></html>
"""


def test_granicus_parse_table():
    scraper = GranicusScraper("Test", "https://example.granicus.com")
    soup = BeautifulSoup(GRANICUS_TABLE_HTML, "lxml")
    items = scraper._parse_page(soup, "https://example.granicus.com")
    assert len(items) >= 3
    types = {i.item_type for i in items}
    assert "agenda" in types
    assert "minutes" in types
    assert any(i.meeting_date == "2026-03-10" for i in items)


BC_MUNICIPAL_HTML = """
<html><body>
<ul>
    <li><a href="/docs/agenda-march-2026.pdf">March 10, 2026 Council Agenda</a></li>
    <li><a href="/docs/minutes-march-2026.pdf">March 10, 2026 Council Minutes</a></li>
    <li><a href="/docs/agenda-feb-2026.pdf">February 24, 2026 Council Agenda</a></li>
</ul>
</body></html>
"""


def test_bc_municipal_parse_list():
    scraper = BCMunicipalScraper("Test", "https://example.com")
    soup = BeautifulSoup(BC_MUNICIPAL_HTML, "lxml")
    items = scraper._parse_page(soup, "https://example.com")
    assert len(items) >= 3
    assert any(i.item_type == "agenda" for i in items)
    assert any(i.item_type == "minutes" for i in items)
    assert any(i.meeting_date == "2026-03-10" for i in items)


def test_bc_municipal_find_subpage_links():
    html = """
    <html><body>
    <a href="/council/agendas">Agendas and Minutes</a>
    <a href="/other">Other Page</a>
    <a href="/council/schedule">Council Schedule</a>
    <a href="https://external.com/agenda">External Agenda</a>
    </body></html>
    """
    scraper = BCMunicipalScraper("Test", "https://example.com/council")
    soup = BeautifulSoup(html, "lxml")
    links = scraper._find_subpage_links(soup)
    # Should find agenda and schedule links but not external
    assert any("agendas" in l for l in links)
    assert any("schedule" in l for l in links)
    assert not any("external.com" in l for l in links)
