"""Fixture-based tests for BCMunicipalScraper and CivicWebScraper parsing.

Tests the generic scraper heuristics against representative HTML fixtures
that mimic common municipal website patterns.  These tests validate that
the parsing logic works without hitting live websites.
"""

import os
from pathlib import Path

import pytest
from bs4 import BeautifulSoup

from app.discovery.custom_bc_municipal import BCMunicipalScraper, classify_link, extract_date
from app.discovery.civicweb import CivicWebScraper, _classify_link as cw_classify_link

FIXTURES_DIR = Path(__file__).parent / "fixtures"


def _read_fixture(name: str) -> str:
    return (FIXTURES_DIR / name).read_text()


# ---------------------------------------------------------------------------
# BCMunicipalScraper._parse_page tests
# ---------------------------------------------------------------------------


class _TestScraper(BCMunicipalScraper):
    """Concrete subclass for testing (BCMunicipalScraper is not abstract itself
    but we instantiate it with a test URL)."""
    pass


def _make_scraper(base_url: str = "https://www.testville.ca/council") -> _TestScraper:
    return _TestScraper("Testville", base_url)


# --- Table layout ---


def test_table_layout_finds_agendas():
    scraper = _make_scraper()
    html = _read_fixture("municipal_table_layout.html")
    soup = BeautifulSoup(html, "lxml")
    items = scraper._parse_page(soup, "https://www.testville.ca/council")

    agendas = [i for i in items if i.item_type == "agenda"]
    assert len(agendas) >= 4, f"Expected >=4 agendas, got {len(agendas)}"


def test_table_layout_finds_minutes():
    scraper = _make_scraper()
    html = _read_fixture("municipal_table_layout.html")
    soup = BeautifulSoup(html, "lxml")
    items = scraper._parse_page(soup, "https://www.testville.ca/council")

    minutes = [i for i in items if i.item_type == "minutes"]
    assert len(minutes) >= 3, f"Expected >=3 minutes, got {len(minutes)}"


def test_table_layout_finds_video():
    scraper = _make_scraper()
    html = _read_fixture("municipal_table_layout.html")
    soup = BeautifulSoup(html, "lxml")
    items = scraper._parse_page(soup, "https://www.testville.ca/council")

    videos = [i for i in items if i.item_type == "video"]
    assert len(videos) >= 1, f"Expected >=1 video, got {len(videos)}"


def test_table_layout_extracts_dates():
    scraper = _make_scraper()
    html = _read_fixture("municipal_table_layout.html")
    soup = BeautifulSoup(html, "lxml")
    items = scraper._parse_page(soup, "https://www.testville.ca/council")

    dated_items = [i for i in items if i.meeting_date is not None]
    assert len(dated_items) >= 3, f"Expected >=3 dated items, got {len(dated_items)}"
    dates = {i.meeting_date for i in dated_items}
    assert "2026-03-10" in dates


def test_table_layout_classifies_meeting_types():
    scraper = _make_scraper()
    html = _read_fixture("municipal_table_layout.html")
    soup = BeautifulSoup(html, "lxml")
    items = scraper._parse_page(soup, "https://www.testville.ca/council")

    types = {i.meeting_type for i in items if i.meeting_type}
    assert "regular" in types
    assert "public_hearing" in types


def test_table_layout_resolves_urls():
    scraper = _make_scraper()
    html = _read_fixture("municipal_table_layout.html")
    soup = BeautifulSoup(html, "lxml")
    items = scraper._parse_page(soup, "https://www.testville.ca/council")

    for item in items:
        assert item.url.startswith("http"), f"URL not absolute: {item.url}"


def test_table_layout_no_duplicates():
    scraper = _make_scraper()
    html = _read_fixture("municipal_table_layout.html")
    soup = BeautifulSoup(html, "lxml")
    items = scraper._parse_page(soup, "https://www.testville.ca/council")

    urls = [i.url for i in items]
    assert len(urls) == len(set(urls)), f"Duplicate URLs found: {urls}"


# --- List layout ---


def test_list_layout_finds_all_types():
    scraper = _make_scraper()
    html = _read_fixture("municipal_list_layout.html")
    soup = BeautifulSoup(html, "lxml")
    items = scraper._parse_page(soup, "https://www.testville.ca/council")

    types = {i.item_type for i in items}
    assert "agenda" in types, f"No agendas found. Types: {types}"
    assert "minutes" in types, f"No minutes found. Types: {types}"
    assert "video" in types, f"No videos found. Types: {types}"


def test_list_layout_extracts_dates():
    scraper = _make_scraper()
    html = _read_fixture("municipal_list_layout.html")
    soup = BeautifulSoup(html, "lxml")
    items = scraper._parse_page(soup, "https://www.testville.ca/council")

    dated = [i for i in items if i.meeting_date]
    assert len(dated) >= 2, f"Expected >=2 dated items, got {len(dated)}"


def test_list_layout_classifies_cow():
    scraper = _make_scraper()
    html = _read_fixture("municipal_list_layout.html")
    soup = BeautifulSoup(html, "lxml")
    items = scraper._parse_page(soup, "https://www.testville.ca/council")

    types = {i.meeting_type for i in items if i.meeting_type}
    assert "committee_of_the_whole" in types, f"COW not detected. Types: {types}"


# --- Mixed content layout ---


def test_mixed_layout_finds_items():
    scraper = _make_scraper()
    html = _read_fixture("municipal_mixed_content.html")
    soup = BeautifulSoup(html, "lxml")
    items = scraper._parse_page(soup, "https://www.testville.ca/meetings")

    assert len(items) >= 4, f"Expected >=4 items, got {len(items)}"
    types = {i.item_type for i in items}
    assert "agenda" in types
    assert "video" in types


def test_mixed_layout_iso_date():
    scraper = _make_scraper()
    html = _read_fixture("municipal_mixed_content.html")
    soup = BeautifulSoup(html, "lxml")
    items = scraper._parse_page(soup, "https://www.testville.ca/meetings")

    dates = {i.meeting_date for i in items if i.meeting_date}
    assert "2026-03-15" in dates, f"ISO date not found. Dates: {dates}"


# --- Empty page ---


def test_empty_page_returns_no_items():
    scraper = _make_scraper()
    html = _read_fixture("municipal_empty_page.html")
    soup = BeautifulSoup(html, "lxml")
    items = scraper._parse_page(soup, "https://www.emptyville.ca/")

    assert len(items) == 0, f"Expected 0 items from empty page, got {len(items)}"


# --- Subpage link detection ---


def test_landing_page_finds_subpage_links():
    scraper = _make_scraper("https://www.subville.ca/council")
    html = _read_fixture("municipal_landing_with_sublinks.html")
    soup = BeautifulSoup(html, "lxml")
    links = scraper._find_subpage_links(soup)

    assert len(links) >= 3, f"Expected >=3 subpage links, got {len(links)}: {links}"
    link_strs = " ".join(links)
    assert "agendas" in link_strs
    assert "minutes" in link_strs


def test_landing_page_excludes_external_links():
    scraper = _make_scraper("https://www.subville.ca/council")
    html = _read_fixture("municipal_landing_with_sublinks.html")
    soup = BeautifulSoup(html, "lxml")
    links = scraper._find_subpage_links(soup)

    for link in links:
        assert "external-site.com" not in link, f"External link leaked: {link}"


def test_landing_page_excludes_self():
    scraper = _make_scraper("https://www.subville.ca/council")
    html = _read_fixture("municipal_landing_with_sublinks.html")
    soup = BeautifulSoup(html, "lxml")
    links = scraper._find_subpage_links(soup)

    assert "https://www.subville.ca/council" not in links


def test_landing_page_follows_archive_links():
    scraper = _make_scraper("https://www.subville.ca/council")
    html = _read_fixture("municipal_landing_with_sublinks.html")
    soup = BeautifulSoup(html, "lxml")
    links = scraper._find_subpage_links(soup)

    archive_found = any("2025" in link for link in links)
    assert archive_found, f"Archive link not found. Links: {links}"


# --- CivicWeb fixture ---


def test_civicweb_schedule_parses_meetings():
    """CivicWeb schedule page parsed via BCMunicipalScraper heuristics."""
    scraper = _make_scraper("https://testville.civicweb.net/Portal/MeetingSchedule.aspx")
    html = _read_fixture("civicweb_schedule.html")
    soup = BeautifulSoup(html, "lxml")
    items = scraper._parse_page(soup, "https://testville.civicweb.net/Portal/MeetingSchedule.aspx")

    agendas = [i for i in items if i.item_type == "agenda"]
    minutes = [i for i in items if i.item_type == "minutes"]
    assert len(agendas) >= 3, f"Expected >=3 agendas, got {len(agendas)}"
    assert len(minutes) >= 2, f"Expected >=2 minutes, got {len(minutes)}"


# --- Helper function tests ---


def test_classify_link_agenda_variants():
    assert classify_link("Agenda", "/doc.pdf") == "agenda"
    assert classify_link("View Agenda", "/meeting/agenda.pdf") == "agenda"
    assert classify_link("Agenda Package", "/pkg.pdf") == "agenda"


def test_classify_link_minutes_variants():
    assert classify_link("Minutes", "/doc.pdf") == "minutes"
    assert classify_link("Meeting Minutes", "/minutes-jan.pdf") == "minutes"
    assert classify_link("View Minutes", "/doc.pdf") == "minutes"


def test_classify_link_video_variants():
    assert classify_link("Watch Recording", "/vid") == "video"
    assert classify_link("Some Link", "https://youtube.com/watch?v=x") == "video"
    assert classify_link("Video", "https://youtu.be/abc") == "video"
    assert classify_link("Webcast", "/webcast") == "video"


def test_classify_link_pdf_with_meeting_context():
    assert classify_link("Regular Council Meeting", "/doc.pdf") == "agenda"


def test_classify_link_returns_none_for_unrelated():
    assert classify_link("About Us", "/about") is None
    assert classify_link("Contact", "/contact.html") is None
    assert classify_link("Parks", "/parks/info") is None


def test_extract_date_formats():
    assert extract_date("March 10, 2026 - Regular Meeting") == "2026-03-10"
    assert extract_date("Meeting on 2026-03-10 at 7pm") == "2026-03-10"
    assert extract_date("Date: 03/10/2026") == "2026-03-10"
    assert extract_date("Monday, March 10, 2026") == "2026-03-10"
    assert extract_date("no date here") is None
