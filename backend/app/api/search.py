"""Search API — keyword search across documents and match summaries."""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_

from app.db.database import get_db
from app.models.document import Document
from app.models.track import TrackMatch

router = APIRouter()


@router.get("/search")
async def search_documents(
    q: str = Query(..., description="Search query"),
    limit: int = 20,
    db: AsyncSession = Depends(get_db),
):
    """Search across discovered documents and match summaries.

    Uses SQL LIKE for full-text keyword matching.
    """
    pattern = f"%{q}%"

    # Search documents by title
    result = await db.execute(
        select(Document)
        .where(
            or_(
                Document.title.ilike(pattern),
                Document.raw_text.ilike(pattern),
            )
        )
        .order_by(Document.first_seen_at.desc())
        .limit(limit)
    )
    docs = result.scalars().all()

    # Search match summaries
    result = await db.execute(
        select(TrackMatch)
        .where(
            or_(
                TrackMatch.summary.ilike(pattern),
                TrackMatch.match_reason.ilike(pattern),
            )
        )
        .limit(limit)
    )
    match_results = result.scalars().all()

    return {
        "query": q,
        "documents": [
            {
                "id": d.id,
                "doc_type": d.doc_type.value if d.doc_type else None,
                "title": d.title,
                "url": d.url,
                "first_seen_at": d.first_seen_at.isoformat() if d.first_seen_at else None,
            }
            for d in docs
        ],
        "matches": [
            {
                "id": m.id,
                "track_id": m.track_id,
                "summary": m.summary,
                "match_score": m.match_score,
                "verification_status": m.verification_status,
            }
            for m in match_results
        ],
        "total": len(docs) + len(match_results),
        "search_type": "keyword",
    }
