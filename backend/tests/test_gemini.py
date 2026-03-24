"""Test keyword fallback matching (no API key needed)."""

from app.ai.gemini import keyword_fallback_match


def test_keyword_match_exact():
    content = "The council will hold a public hearing on the OCP amendment bylaw."
    result = keyword_fallback_match(content, ["ocp_updates", "rezoning"], ["OCP"])
    assert result["is_match"] is True
    assert "ocp_updates" in result["matched_topics"]
    assert "OCP" in result["matched_keywords"]
    assert result["confidence"] > 0


def test_keyword_match_topic_only():
    content = "Discussion of the official community plan update for 2026."
    result = keyword_fallback_match(content, ["ocp_updates"], [])
    assert result["is_match"] is True
    assert "ocp_updates" in result["matched_topics"]


def test_keyword_match_keyword_only():
    content = "Affordable housing strategy report presented to council."
    result = keyword_fallback_match(content, [], ["affordable housing"])
    assert result["is_match"] is True
    assert "affordable housing" in result["matched_keywords"]


def test_keyword_no_match():
    content = "Minutes of the parks and recreation advisory committee."
    result = keyword_fallback_match(content, ["rezoning"], ["OCP", "development permit"])
    assert result["is_match"] is False
    assert result["confidence"] == 0


def test_keyword_match_multiple_topics():
    content = "Public hearing on rezoning bylaw amendment for affordable housing development."
    result = keyword_fallback_match(
        content,
        ["rezoning", "public_hearings", "housing", "bylaws"],
        ["affordable housing"],
    )
    assert result["is_match"] is True
    assert "rezoning" in result["matched_topics"]
    assert "public_hearings" in result["matched_topics"]
    assert "housing" in result["matched_topics"]
    assert "bylaws" in result["matched_topics"]
    assert "affordable housing" in result["matched_keywords"]
    assert result["confidence"] > 0.5


def test_keyword_case_insensitive():
    content = "REZONING APPLICATION for 456 Oak Street"
    result = keyword_fallback_match(content, ["rezoning"], [])
    assert result["is_match"] is True
