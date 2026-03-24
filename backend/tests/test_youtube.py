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
