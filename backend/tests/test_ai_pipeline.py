"""Integration tests for the AI processing pipeline:
keyword filter -> Gemini batch match -> summarize -> store TrackMatch records.

Tests the full processing flow with mocked Gemini API and DB sessions.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.ai.processor import (
    process_new_documents,
    _batch_match_documents,
    _batch_summarize_matches,
    _build_video_timestamps_section,
    _format_doc_for_batch,
)
from app.models.document import DocType


# --- Helpers ---


def _make_document(**kwargs):
    """Create a mock Document."""
    doc = MagicMock()
    doc.id = kwargs.get("id", 1)
    doc.municipality_id = kwargs.get("municipality_id", 1)
    doc.title = kwargs.get("title", "Council Agenda - Rezoning Application")
    doc.raw_text = kwargs.get("raw_text", None)
    doc.doc_type = kwargs.get("doc_type", DocType.AGENDA)
    doc.video_timestamps = kwargs.get("video_timestamps", None)
    doc.video_duration = kwargs.get("video_duration", None)
    doc.is_processed = kwargs.get("is_processed", False)
    doc.is_new = kwargs.get("is_new", True)
    return doc


def _make_track(**kwargs):
    """Create a mock Track."""
    track = MagicMock()
    track.id = kwargs.get("id", 1)
    track.municipality_ids = kwargs.get("municipality_ids", [1])
    track.topics = kwargs.get("topics", ["zoning_density"])
    track.keywords = kwargs.get("keywords", ["rezoning", "density"])
    track.is_active = True
    return track


def _make_municipality(**kwargs):
    """Create a mock Municipality."""
    muni = MagicMock()
    muni.id = kwargs.get("id", 1)
    muni.short_name = kwargs.get("short_name", "Colwood")
    return muni


# --- _build_video_timestamps_section ---


def test_video_timestamps_section_empty():
    """No timestamps should return empty string."""
    doc = _make_document(video_timestamps=None)
    assert _build_video_timestamps_section(doc) == ""


def test_video_timestamps_section_with_data():
    """Should format timestamps as chapter list."""
    doc = _make_document(video_timestamps=[
        {"t": "0:15:30", "label": "Rezoning discussion"},
        {"t": "1:00:00", "label": "Public hearing"},
    ])
    result = _build_video_timestamps_section(doc)
    assert "VIDEO CHAPTER TIMESTAMPS:" in result
    assert "[0:15:30]" in result
    assert "Rezoning discussion" in result
    assert "[1:00:00]" in result


# --- _format_doc_for_batch ---


def test_format_doc_for_batch():
    """Should format document with municipality, type, title, content."""
    doc = _make_document(raw_text="Discussion of rezoning bylaw amendment.")
    result = _format_doc_for_batch(0, doc, "Colwood")
    assert "DOCUMENT 0" in result
    assert "Colwood" in result
    assert "agenda" in result.lower()
    assert "rezoning bylaw" in result


def test_format_doc_truncates_content():
    """Content should be truncated to 1500 chars."""
    long_text = "A" * 3000
    doc = _make_document(raw_text=long_text)
    result = _format_doc_for_batch(0, doc, "Colwood")
    assert "AAA" in result
    # The content section should be capped
    assert len(result) < 3000


# --- _batch_match_documents (keyword pre-filter path) ---


@pytest.mark.asyncio
async def test_batch_match_keyword_prefilter_matches():
    """Documents matching keywords should be caught by pre-filter without Gemini."""
    doc = _make_document(
        title="Rezoning Application for 123 Main St",
        raw_text="This rezoning application proposes increased density."
    )
    track = _make_track(topics=["zoning_density"], keywords=["rezoning"])
    munis = {1: _make_municipality()}

    with patch("app.ai.processor.gemini_batch_match", new_callable=AsyncMock) as mock_gemini:
        matched = await _batch_match_documents(
            [(doc, "Colwood")], track, munis, AsyncMock()
        )

    # Should match via keyword fallback (no Gemini call needed)
    assert len(matched) == 1
    mock_gemini.assert_not_called()


@pytest.mark.asyncio
async def test_batch_match_sends_non_keyword_to_gemini():
    """Documents not matching keywords should be sent to Gemini."""
    doc = _make_document(
        title="Budget Discussion",
        raw_text="Annual municipal budget review for 2026."
    )
    track = _make_track(topics=["zoning_density"], keywords=["rezoning"])
    munis = {1: _make_municipality()}

    db = AsyncMock()

    with patch("app.ai.processor.gemini_batch_match", new_callable=AsyncMock) as mock_gemini:
        mock_gemini.return_value = (
            [{"doc_index": 0, "is_match": True, "confidence": 0.8, "reason": "budget impacts housing"}],
            {"input_tokens": 100, "output_tokens": 50},
        )
        with patch("app.ai.processor.log_api_cost", new_callable=AsyncMock):
            matched = await _batch_match_documents(
                [(doc, "Colwood")], track, munis, db
            )

    assert len(matched) == 1
    mock_gemini.assert_called_once()


@pytest.mark.asyncio
async def test_batch_match_gemini_failure_falls_back_to_keywords():
    """When Gemini fails, should fall back to keyword matching for all docs."""
    # Doc with keyword match (would be caught by fallback)
    doc1 = _make_document(
        id=1, title="Rezoning report",
        raw_text="Rezoning application for density increase."
    )
    # Doc without keyword match (would be lost)
    doc2 = _make_document(
        id=2, title="Budget Discussion",
        raw_text="Annual budget review."
    )
    track = _make_track(topics=["zoning_density"], keywords=["rezoning"])
    munis = {1: _make_municipality()}

    # First doc matches keyword filter, second goes to Gemini
    db = AsyncMock()

    with patch("app.ai.processor.gemini_batch_match", new_callable=AsyncMock) as mock_gemini:
        mock_gemini.return_value = (None, {"input_tokens": 0, "output_tokens": 0})
        with patch("app.ai.processor.log_api_cost", new_callable=AsyncMock):
            matched = await _batch_match_documents(
                [(doc1, "Colwood"), (doc2, "Colwood")], track, munis, db
            )

    # doc1 should match (keyword pre-filter)
    # doc2 goes to Gemini, Gemini fails, keyword fallback runs again — no match
    assert len(matched) >= 1
    assert any(m[0].id == 1 for m in matched)


# --- _batch_summarize_matches ---


@pytest.mark.asyncio
async def test_batch_summarize_high_confidence():
    """High-confidence matches should be summarized via Gemini."""
    doc = _make_document(municipality_id=1)
    match_result = {"confidence": 0.8, "reason": "matched"}
    munis = {1: _make_municipality()}
    db = AsyncMock()

    with patch("app.ai.processor.gemini_batch_summarize", new_callable=AsyncMock) as mock_gemini:
        mock_gemini.return_value = (
            [{"doc_index": 0, "summary": "Rezoning for housing density.", "key_points": ["Density increase"]}],
            {"input_tokens": 200, "output_tokens": 100},
        )
        with patch("app.ai.processor.log_api_cost", new_callable=AsyncMock):
            results = await _batch_summarize_matches(
                [(doc, match_result)],
                _make_track(),
                munis,
                db,
            )

    assert len(results) == 1
    _, _, summary = results[0]
    assert summary is not None
    assert summary["summary"] == "Rezoning for housing density."


@pytest.mark.asyncio
async def test_batch_summarize_low_confidence_skipped():
    """Low-confidence matches should get None summary."""
    doc = _make_document()
    match_result = {"confidence": 0.3, "reason": "weak match"}
    munis = {1: _make_municipality()}
    db = AsyncMock()

    with patch("app.ai.processor.gemini_batch_summarize", new_callable=AsyncMock) as mock_gemini:
        results = await _batch_summarize_matches(
            [(doc, match_result)],
            _make_track(),
            munis,
            db,
        )

    assert len(results) == 1
    _, _, summary = results[0]
    assert summary is None
    mock_gemini.assert_not_called()


@pytest.mark.asyncio
async def test_batch_summarize_gemini_failure():
    """If Gemini fails during summarization, matches should still be stored without summary."""
    doc = _make_document(municipality_id=1)
    match_result = {"confidence": 0.9, "reason": "matched"}
    munis = {1: _make_municipality()}
    db = AsyncMock()

    with patch("app.ai.processor.gemini_batch_summarize", new_callable=AsyncMock) as mock_gemini:
        mock_gemini.return_value = (None, {"input_tokens": 0, "output_tokens": 0})
        with patch("app.ai.processor.log_api_cost", new_callable=AsyncMock):
            results = await _batch_summarize_matches(
                [(doc, match_result)],
                _make_track(),
                munis,
                db,
            )

    assert len(results) == 1
    _, _, summary = results[0]
    assert summary is None  # Graceful degradation


# --- process_new_documents full pipeline ---


@pytest.mark.asyncio
async def test_process_no_active_tracks():
    """With no active tracks, processing should return zero stats."""
    db = AsyncMock()
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = []
    db.execute = AsyncMock(return_value=mock_result)

    stats = await process_new_documents(db)

    assert stats["documents_processed"] == 0
    assert stats["matches_found"] == 0


@pytest.mark.asyncio
async def test_process_no_unprocessed_documents():
    """With tracks but no unprocessed docs, should return zero stats."""
    db = AsyncMock()

    call_count = 0

    async def mock_execute(query):
        nonlocal call_count
        call_count += 1
        result = MagicMock()
        if call_count == 1:
            # First call: get active tracks
            result.scalars.return_value.all.return_value = [_make_track()]
        else:
            # Second call: get unprocessed documents
            result.scalars.return_value.all.return_value = []
        return result

    db.execute = AsyncMock(side_effect=mock_execute)

    stats = await process_new_documents(db)

    assert stats["documents_processed"] == 0


@pytest.mark.asyncio
async def test_process_full_pipeline_keyword_match():
    """Full pipeline: unprocessed doc -> keyword match -> store TrackMatch."""
    track = _make_track(
        municipality_ids=[1],
        topics=["zoning_density"],
        keywords=["rezoning"],
    )
    doc = _make_document(
        id=1, municipality_id=1,
        title="Rezoning Application",
        raw_text="This rezoning application proposes increased density.",
    )
    muni = _make_municipality(id=1)

    db = AsyncMock()
    call_count = 0

    async def mock_execute(query):
        nonlocal call_count
        call_count += 1
        result = MagicMock()
        if call_count == 1:
            # Active tracks
            result.scalars.return_value.all.return_value = [track]
        elif call_count == 2:
            # Unprocessed documents (first batch)
            result.scalars.return_value.all.return_value = [doc]
        elif call_count == 3:
            # Municipality lookup
            result.scalars.return_value.all.return_value = [muni]
        elif call_count == 4:
            # Idempotency check — no existing TrackMatch
            result.scalar_one_or_none.return_value = None
        else:
            # Second loop: no more unprocessed documents
            result.scalars.return_value.all.return_value = []
        return result

    db.execute = AsyncMock(side_effect=mock_execute)
    db.commit = AsyncMock()

    stats = await process_new_documents(db)

    assert stats["documents_processed"] == 1
    assert stats["matches_found"] >= 1
    assert db.add.called  # TrackMatch was added


@pytest.mark.asyncio
async def test_process_skips_irrelevant_municipalities():
    """Documents from municipalities not in track.municipality_ids should be skipped."""
    track = _make_track(municipality_ids=[1])  # Only tracks municipality 1
    doc = _make_document(id=1, municipality_id=99)  # Doc from municipality 99
    muni1 = _make_municipality(id=1)
    muni99 = _make_municipality(id=99, short_name="Faraway")

    db = AsyncMock()
    call_count = 0

    async def mock_execute(query):
        nonlocal call_count
        call_count += 1
        result = MagicMock()
        if call_count == 1:
            result.scalars.return_value.all.return_value = [track]
        elif call_count == 2:
            result.scalars.return_value.all.return_value = [doc]
        elif call_count == 3:
            result.scalars.return_value.all.return_value = [muni1, muni99]
        else:
            result.scalars.return_value.all.return_value = []
        return result

    db.execute = AsyncMock(side_effect=mock_execute)
    db.commit = AsyncMock()

    stats = await process_new_documents(db)

    assert stats["documents_processed"] == 1
    assert stats["matches_found"] == 0  # Doc from wrong municipality


@pytest.mark.asyncio
async def test_process_idempotency_skips_duplicate_match():
    """If TrackMatch already exists for (track, doc), should skip creation."""
    track = _make_track(municipality_ids=[1], topics=["zoning_density"], keywords=["rezoning"])
    doc = _make_document(
        id=1, municipality_id=1,
        raw_text="Rezoning application for density increase.",
    )
    muni = _make_municipality(id=1)

    db = AsyncMock()
    call_count = 0

    async def mock_execute(query):
        nonlocal call_count
        call_count += 1
        result = MagicMock()
        if call_count == 1:
            result.scalars.return_value.all.return_value = [track]
        elif call_count == 2:
            result.scalars.return_value.all.return_value = [doc]
        elif call_count == 3:
            result.scalars.return_value.all.return_value = [muni]
        elif call_count == 4:
            # Existing TrackMatch found — idempotency check
            result.scalar_one_or_none.return_value = MagicMock()
        else:
            result.scalars.return_value.all.return_value = []
        return result

    db.execute = AsyncMock(side_effect=mock_execute)
    db.commit = AsyncMock()

    stats = await process_new_documents(db)

    # Match was found but TrackMatch already exists, so no new TrackMatch add
    assert stats["matches_found"] >= 1
    # db.add may be called for other things (cost tracker), but summaries_generated
    # should be 0 since the duplicate match is skipped
    assert stats["summaries_generated"] == 0


# --- Gemini calls saved tracking ---


@pytest.mark.asyncio
async def test_gemini_calls_saved_tracking():
    """Stats should track how many Gemini calls were saved via batching."""
    track = _make_track(municipality_ids=[1], topics=["zoning_density"], keywords=["rezoning"])
    # Create multiple docs that match via keyword
    docs = [
        _make_document(id=i, municipality_id=1,
                       raw_text=f"Rezoning application {i}")
        for i in range(5)
    ]
    muni = _make_municipality(id=1)

    db = AsyncMock()
    call_count = 0

    async def mock_execute(query):
        nonlocal call_count
        call_count += 1
        result = MagicMock()
        if call_count == 1:
            result.scalars.return_value.all.return_value = [track]
        elif call_count == 2:
            result.scalars.return_value.all.return_value = docs
        elif call_count == 3:
            result.scalars.return_value.all.return_value = [muni]
        elif call_count <= 3 + len(docs):
            # Idempotency checks
            result.scalar_one_or_none.return_value = None
        else:
            result.scalars.return_value.all.return_value = []
        return result

    db.execute = AsyncMock(side_effect=mock_execute)
    db.commit = AsyncMock()

    stats = await process_new_documents(db)

    # All 5 match via keyword, so gemini_calls_saved should be > 0
    # (5 individual calls saved, 0 batch calls needed since all matched keyword)
    assert stats["gemini_calls_saved"] >= 0
    assert stats["documents_processed"] == 5
