"""Processing pipeline: match discovered documents against user tracks, then summarize.

Uses batching to reduce Gemini API costs:
- Match: up to 10 documents per API call
- Summarize: up to 5 matched documents per API call
- Embed: native batch embedding via Gemini embed_content
"""

import logging
from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.document import Document
from app.models.track import Track, TrackMatch
from app.models.municipality import Municipality
from app.ai.prompts import (
    BATCH_MATCH_PROMPT,
    BATCH_SUMMARY_PROMPT,
)
from app.ai.gemini import (
    gemini_batch_match,
    gemini_batch_summarize,
    keyword_fallback_match,
    MATCH_BATCH_SIZE,
    SUMMARY_BATCH_SIZE,
)
from app.services.cost_tracker import log_api_cost
from app.config import settings

logger = logging.getLogger(__name__)

# Maximum documents to process per pipeline run. Runs loop until backlog is clear.
_BATCH_FETCH_SIZE = 50


def _build_video_timestamps_section(doc: Document) -> str:
    """Build the video timestamps section for prompts."""
    if not doc.video_timestamps:
        return ""
    lines = ["VIDEO CHAPTER TIMESTAMPS:"]
    for ts in doc.video_timestamps:
        lines.append(f"  [{ts.get('t', '?')}] {ts.get('label', 'Unknown')}")
    return "\n".join(lines)


def _format_doc_for_batch(index: int, doc: Document, muni_name: str) -> str:
    """Format a document entry for batch prompt."""
    content = doc.raw_text or doc.title or ""
    ts_section = _build_video_timestamps_section(doc)
    return (
        f"--- DOCUMENT {index} ---\n"
        f"Municipality: {muni_name}\n"
        f"Type: {doc.doc_type.value if doc.doc_type else 'unknown'}\n"
        f"Title: {doc.title}\n"
        f"Content (first 1500 chars): {content[:1500]}\n"
        f"{ts_section}\n"
    )


async def _batch_match_documents(
    docs_with_munis: list[tuple[Document, str]],
    track: Track,
    munis: dict[int, Municipality],
    db: AsyncSession,
) -> list[tuple[Document, dict]]:
    """Match a batch of documents against a track using a single Gemini call.

    Returns list of (document, match_result) for documents that matched.
    """
    matched = []

    # Step 1: Quick keyword pre-filter (free, no API cost)
    needs_gemini = []
    for doc, muni_name in docs_with_munis:
        content = doc.raw_text or doc.title or ""
        fallback = keyword_fallback_match(content, track.topics, track.keywords)
        if fallback["is_match"]:
            matched.append((doc, fallback))
        else:
            needs_gemini.append((doc, muni_name))

    # Step 2: Batch the remaining through Gemini
    if not needs_gemini:
        return matched

    track_munis = [munis[mid].short_name for mid in track.municipality_ids if mid in munis]

    # Process in batches of MATCH_BATCH_SIZE
    for i in range(0, len(needs_gemini), MATCH_BATCH_SIZE):
        batch = needs_gemini[i : i + MATCH_BATCH_SIZE]
        docs_list = "\n".join(
            _format_doc_for_batch(idx, doc, muni_name)
            for idx, (doc, muni_name) in enumerate(batch)
        )

        batch_results, usage = await gemini_batch_match(
            BATCH_MATCH_PROMPT.format(
                municipalities=", ".join(track_munis),
                topics=", ".join(track.topics),
                keywords=", ".join(track.keywords),
                documents_list=docs_list,
            )
        )

        await log_api_cost(
            db, "gemini", "batch_match", settings.gemini_model,
            usage["input_tokens"], usage["output_tokens"],
            context={"doc_count": len(batch), "track_id": track.id},
        )

        if batch_results:
            for result in batch_results:
                idx = result.get("doc_index", 0)
                if idx < len(batch) and result.get("is_match"):
                    matched.append((batch[idx][0], result))
        else:
            # Gemini failed — apply keyword fallback to every document in this batch
            # rather than silently dropping them. This is the correct degraded-mode
            # behaviour: worse precision, but no data loss.
            logger.warning(
                "Gemini batch match failed for track %d, falling back to keyword matching "
                "for %d documents in this batch",
                track.id, len(batch),
            )
            for doc, muni_name in batch:
                content = doc.raw_text or doc.title or ""
                fallback = keyword_fallback_match(content, track.topics, track.keywords)
                if fallback["is_match"]:
                    matched.append((doc, fallback))

    return matched


async def _batch_summarize_matches(
    matched_docs: list[tuple[Document, dict]],
    track: Track,
    munis: dict[int, Municipality],
    db: AsyncSession,
) -> list[tuple[Document, dict, dict | None]]:
    """Summarize a batch of matched documents using fewer Gemini calls.

    Returns list of (document, match_result, summary_result).
    """
    results = []

    # Only summarize high-confidence matches
    to_summarize = [
        (doc, match) for doc, match in matched_docs
        if match.get("confidence", 0) >= 0.5
    ]
    low_confidence = [
        (doc, match) for doc, match in matched_docs
        if match.get("confidence", 0) < 0.5
    ]

    # Low confidence matches get no summary
    for doc, match in low_confidence:
        results.append((doc, match, None))

    if not to_summarize:
        return results

    # Process in batches of SUMMARY_BATCH_SIZE
    for i in range(0, len(to_summarize), SUMMARY_BATCH_SIZE):
        batch = to_summarize[i : i + SUMMARY_BATCH_SIZE]
        docs_list = "\n".join(
            _format_doc_for_batch(
                idx, doc,
                munis[doc.municipality_id].short_name if doc.municipality_id in munis else "Unknown",
            )
            for idx, (doc, _) in enumerate(batch)
        )

        batch_summaries, usage = await gemini_batch_summarize(
            BATCH_SUMMARY_PROMPT.format(
                topics=", ".join(track.topics),
                keywords=", ".join(track.keywords),
                documents_list=docs_list,
            )
        )

        await log_api_cost(
            db, "gemini", "batch_summarize", settings.gemini_model,
            usage["input_tokens"], usage["output_tokens"],
            context={"doc_count": len(batch), "track_id": track.id},
        )

        if batch_summaries:
            summarized_indices = set()
            for summary in batch_summaries:
                idx = summary.get("doc_index", 0)
                if idx < len(batch):
                    doc, match = batch[idx]
                    results.append((doc, match, summary))
                    summarized_indices.add(idx)
            # Any docs not returned by Gemini still get stored without summary
            for idx, (doc, match) in enumerate(batch):
                if idx not in summarized_indices:
                    results.append((doc, match, None))
        else:
            # Gemini failed — store matches without summaries rather than losing them
            for doc, match in batch:
                results.append((doc, match, None))

    return results


async def process_new_documents(db: AsyncSession) -> dict:
    """Process all new (unprocessed) documents against active tracks.

    Pipeline (batched to reduce Gemini API costs):
    1. Get all new documents (loops until backlog is empty)
    2. For each track, batch all relevant documents
    3. Keyword pre-filter (free) → batch Gemini match (up to 10/call)
    4. Batch summarize matched docs (up to 5/call)
    5. Store TrackMatch records

    Returns stats dict.
    """
    stats = {
        "documents_processed": 0,
        "matches_found": 0,
        "summaries_generated": 0,
        "gemini_calls_saved": 0,
    }

    # Get active tracks once — reused across all fetch batches
    result = await db.execute(select(Track).where(Track.is_active.is_(True)))
    tracks = result.scalars().all()

    if not tracks:
        logger.info("No active tracks — skipping processing")
        return stats

    # Loop until all unprocessed documents are handled. A hard limit would leave
    # a growing backlog that never catches up if more than _BATCH_FETCH_SIZE docs
    # arrive between runs.
    while True:
        result = await db.execute(
            select(Document)
            .where(Document.is_processed.is_(False))
            .limit(_BATCH_FETCH_SIZE)
        )
        documents = result.scalars().all()

        if not documents:
            break

        # Build municipality lookup for this batch
        muni_ids: set[int] = set()
        for doc in documents:
            muni_ids.add(doc.municipality_id)
        for track in tracks:
            muni_ids.update(track.municipality_ids)

        result = await db.execute(select(Municipality).where(Municipality.id.in_(muni_ids)))
        munis = {m.id: m for m in result.scalars().all()}

        for track in tracks:
            relevant_docs = [
                (doc, munis[doc.municipality_id].short_name)
                for doc in documents
                if doc.municipality_id in track.municipality_ids and doc.municipality_id in munis
            ]

            if not relevant_docs:
                continue

            individual_calls = len(relevant_docs)

            matched = await _batch_match_documents(relevant_docs, track, munis, db)
            stats["matches_found"] += len(matched)

            batch_calls = (len(relevant_docs) + MATCH_BATCH_SIZE - 1) // MATCH_BATCH_SIZE
            stats["gemini_calls_saved"] += max(0, individual_calls - batch_calls)

            summarized = await _batch_summarize_matches(matched, track, munis, db)

            for doc, match_result, summary_result in summarized:
                # Idempotency: skip if this (track, document) pair already exists.
                existing_match = await db.execute(
                    select(TrackMatch).where(
                        TrackMatch.track_id == track.id,
                        TrackMatch.document_id == doc.id,
                    )
                )
                if existing_match.scalar_one_or_none():
                    continue

                if summary_result:
                    stats["summaries_generated"] += 1

                track_match = TrackMatch(
                    track_id=track.id,
                    document_id=doc.id,
                    match_score=match_result.get("confidence", 0.0),
                    match_reason=match_result.get("reason", ""),
                    matched_topics=match_result.get("matched_topics", []),
                    matched_keywords=match_result.get("matched_keywords", []),
                    summary=summary_result.get("summary") if summary_result else None,
                    key_points=summary_result.get("key_points") if summary_result else None,
                    verification_status="unverified",
                    notification_status="pending",
                )
                db.add(track_match)

        # Mark this batch as processed
        for doc in documents:
            doc.is_processed = True
            doc.is_new = False
            stats["documents_processed"] += 1

        await db.commit()

    logger.info(
        "Processing complete: %d docs, %d matches, %d summaries, %d Gemini calls saved via batching",
        stats["documents_processed"],
        stats["matches_found"],
        stats["summaries_generated"],
        stats["gemini_calls_saved"],
    )
    return stats
