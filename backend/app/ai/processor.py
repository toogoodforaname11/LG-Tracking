"""Processing pipeline: match discovered documents against user tracks, then summarize."""

import logging
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.document import Document
from app.models.track import Track, TrackMatch
from app.models.municipality import Municipality
from app.ai.prompts import MATCH_PROMPT, SUMMARY_PROMPT
from app.ai.gemini import gemini_match, gemini_summarize, keyword_fallback_match

logger = logging.getLogger(__name__)


async def process_new_documents(db: AsyncSession) -> dict:
    """Process all new (unprocessed) documents against active tracks.

    Pipeline:
    1. Get all new documents
    2. For each document, check against all active tracks
    3. Quick match (keywords first, then Gemini if available)
    4. For matches with confidence > 0.5, run full summarization
    5. Store TrackMatch records

    Returns stats dict.
    """
    stats = {"documents_processed": 0, "matches_found": 0, "summaries_generated": 0}

    # Get unprocessed documents
    result = await db.execute(
        select(Document).where(Document.is_processed.is_(False)).limit(50)
    )
    documents = result.scalars().all()

    if not documents:
        logger.info("No new documents to process")
        return stats

    # Get active tracks
    result = await db.execute(select(Track).where(Track.is_active.is_(True)))
    tracks = result.scalars().all()

    if not tracks:
        logger.info("No active tracks — skipping processing")
        return stats

    # Build municipality lookup
    muni_ids = set()
    for doc in documents:
        muni_ids.add(doc.municipality_id)
    for track in tracks:
        muni_ids.update(track.municipality_ids)

    result = await db.execute(select(Municipality).where(Municipality.id.in_(muni_ids)))
    munis = {m.id: m for m in result.scalars().all()}

    for doc in documents:
        doc_muni = munis.get(doc.municipality_id)
        if not doc_muni:
            continue

        for track in tracks:
            # Skip if document's municipality is not in this track
            if doc.municipality_id not in track.municipality_ids:
                continue

            # Step 1: Quick keyword match (always works, no API needed)
            content_for_match = doc.raw_text or doc.title or ""
            fallback_result = keyword_fallback_match(
                content_for_match, track.topics, track.keywords
            )

            # Step 2: If keywords didn't match, try Gemini for smarter matching
            match_result = fallback_result
            if not fallback_result["is_match"]:
                track_munis = [munis[mid].short_name for mid in track.municipality_ids if mid in munis]
                gemini_result = await gemini_match(
                    MATCH_PROMPT.format(
                        municipalities=", ".join(track_munis),
                        topics=", ".join(track.topics),
                        keywords=", ".join(track.keywords),
                        document_municipality=doc_muni.short_name,
                        document_type=doc.doc_type.value if doc.doc_type else "unknown",
                        document_title=doc.title,
                        document_date="unknown",
                        content_excerpt=content_for_match[:2000],
                    )
                )
                if gemini_result:
                    match_result = gemini_result

            if not match_result.get("is_match"):
                continue

            confidence = match_result.get("confidence", 0.0)
            stats["matches_found"] += 1

            # Step 3: For good matches, generate full summary
            summary_result = None
            if confidence >= 0.5:
                track_munis = [munis[mid].short_name for mid in track.municipality_ids if mid in munis]
                summary_result = await gemini_summarize(
                    SUMMARY_PROMPT.format(
                        municipality=doc_muni.short_name,
                        meeting_type=doc.doc_type.value if doc.doc_type else "unknown",
                        meeting_date="unknown",
                        document_type=doc.doc_type.value if doc.doc_type else "unknown",
                        topics=", ".join(track.topics),
                        keywords=", ".join(track.keywords),
                        content=content_for_match[:8000],
                    )
                )
                if summary_result:
                    stats["summaries_generated"] += 1

            # Store the match
            track_match = TrackMatch(
                track_id=track.id,
                document_id=doc.id,
                match_score=confidence,
                match_reason=match_result.get("reason", ""),
                matched_topics=match_result.get("matched_topics", []),
                matched_keywords=match_result.get("matched_keywords", []),
                summary=summary_result.get("summary") if summary_result else None,
                key_points=summary_result.get("key_points") if summary_result else None,
                verification_status="unverified",
                notification_status="pending",
            )
            db.add(track_match)

        # Mark document as processed
        doc.is_processed = True
        doc.is_new = False
        stats["documents_processed"] += 1

    await db.commit()
    logger.info(
        f"Processing complete: {stats['documents_processed']} docs, "
        f"{stats['matches_found']} matches, {stats['summaries_generated']} summaries"
    )
    return stats
