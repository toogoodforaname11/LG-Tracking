"""Test CivicWeb scraper parsing logic."""

from app.discovery.civicweb import classify_meeting_type, parse_civicweb_date


def test_classify_meeting_type():
    assert classify_meeting_type("Regular Council Meeting") == "regular"
    assert classify_meeting_type("Public Hearing") == "public_hearing"
    assert classify_meeting_type("Special Council Meeting") == "special"
    assert classify_meeting_type("Committee of the Whole") == "committee_of_the_whole"
    assert classify_meeting_type("Planning Committee") == "committee"
    assert classify_meeting_type("Something Unknown") == "regular"


def test_parse_civicweb_date():
    assert parse_civicweb_date("March 9, 2026") == "2026-03-09"
    assert parse_civicweb_date("Mar 9, 2026") == "2026-03-09"
    assert parse_civicweb_date("2026-03-09") == "2026-03-09"
    assert parse_civicweb_date("03/09/2026") == "2026-03-09"
    assert parse_civicweb_date("Monday, March 9, 2026") == "2026-03-09"
    assert parse_civicweb_date("not a date") is None
    assert parse_civicweb_date("") is None
