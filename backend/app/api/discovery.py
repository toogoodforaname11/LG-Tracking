from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, case, literal_column
from sqlalchemy.orm import selectinload

from app.db.database import get_db
from app.discovery.poller import run_discovery
from app.models.document import Document, Meeting
from app.models.municipality import Municipality, Source, ScrapeRun, ScrapeStatus
from app.api.dependencies import verify_cron_secret

router = APIRouter()


@router.post("/poll", dependencies=[Depends(verify_cron_secret)])
async def trigger_poll(
    municipality: str | None = Query(None, description="Filter by municipality short_name"),
    db: AsyncSession = Depends(get_db),
):
    """Trigger a discovery poll across active sources."""
    results = await run_discovery(db, municipality_filter=municipality)
    return {"status": "completed", "results": results}


@router.get("/documents")
async def list_documents(
    municipality: str | None = None,
    doc_type: str | None = None,
    new_only: bool = False,
    limit: int = 50,
    db: AsyncSession = Depends(get_db),
):
    """List discovered documents."""
    query = select(Document).order_by(Document.first_seen_at.desc()).limit(limit)
    if municipality:
        query = query.join(Municipality, Document.municipality_id == Municipality.id).where(
            Municipality.short_name == municipality
        )
    if new_only:
        query = query.where(Document.is_new.is_(True))
    if doc_type:
        query = query.where(Document.doc_type == doc_type)

    result = await db.execute(query)
    docs = result.scalars().all()

    return [
        {
            "id": d.id,
            "municipality_id": d.municipality_id,
            "doc_type": d.doc_type.value if d.doc_type else None,
            "title": d.title,
            "url": d.url,
            "meeting_date": None,
            "is_new": d.is_new,
            "is_processed": d.is_processed,
            "first_seen_at": d.first_seen_at.isoformat() if d.first_seen_at else None,
        }
        for d in docs
    ]


@router.get("/meetings")
async def list_meetings(
    municipality: str | None = None,
    limit: int = 20,
    db: AsyncSession = Depends(get_db),
):
    """List discovered meetings."""
    query = select(Meeting).order_by(Meeting.meeting_date.desc()).limit(limit)
    if municipality:
        query = query.join(Municipality, Meeting.municipality_id == Municipality.id).where(
            Municipality.short_name == municipality
        )
    result = await db.execute(query)
    meetings = result.scalars().all()

    return [
        {
            "id": m.id,
            "municipality_id": m.municipality_id,
            "title": m.title,
            "meeting_date": m.meeting_date,
            "meeting_time": m.meeting_time,
            "meeting_type": m.meeting_type.value if m.meeting_type else None,
            "source_url": m.source_url,
        }
        for m in meetings
    ]


@router.get("/scrape-runs")
async def list_scrape_runs(limit: int = 20, db: AsyncSession = Depends(get_db)):
    """List recent scrape runs for monitoring."""
    query = select(ScrapeRun).order_by(ScrapeRun.started_at.desc()).limit(limit)
    result = await db.execute(query)
    runs = result.scalars().all()

    return [
        {
            "id": r.id,
            "source_id": r.source_id,
            "started_at": r.started_at.isoformat() if r.started_at else None,
            "finished_at": r.finished_at.isoformat() if r.finished_at else None,
            "status": r.status,
            "error_message": r.error_message,
            "documents_found": r.documents_found,
            "new_documents": r.new_documents,
        }
        for r in runs
    ]


@router.get("/source-health")
async def source_health(
    status: str | None = Query(None, description="Filter by scrape status (ACTIVE, BROKEN, PENDING)"),
    platform: str | None = Query(None, description="Filter by platform"),
    db: AsyncSession = Depends(get_db),
):
    """Per-source health dashboard: shows each source with its last scrape result.

    Returns aggregate counts and per-source details including last scrape time,
    consecutive failures, and most recent error.
    """
    # Build the latest scrape run subquery
    latest_run = (
        select(
            ScrapeRun.source_id,
            func.max(ScrapeRun.started_at).label("last_run_at"),
        )
        .group_by(ScrapeRun.source_id)
        .subquery()
    )

    # Main query: sources with municipality names and latest run info
    query = (
        select(Source, Municipality.short_name.label("municipality_name"), latest_run.c.last_run_at)
        .join(Municipality, Source.municipality_id == Municipality.id)
        .outerjoin(latest_run, Source.id == latest_run.c.source_id)
        .order_by(Municipality.short_name, Source.platform)
    )

    if status:
        try:
            status_enum = ScrapeStatus(status.upper())
            query = query.where(Source.scrape_status == status_enum)
        except ValueError:
            pass
    if platform:
        query = query.where(Source.platform == platform.upper())

    result = await db.execute(query)
    rows = result.all()

    # Aggregate counts
    status_counts: dict[str, int] = {}
    sources_list = []
    for source, muni_name, last_run_at in rows:
        s_status = source.scrape_status.value if source.scrape_status else "UNKNOWN"
        status_counts[s_status] = status_counts.get(s_status, 0) + 1
        sources_list.append({
            "source_id": source.id,
            "municipality": muni_name,
            "platform": source.platform.value if source.platform else None,
            "label": source.label,
            "url": source.url,
            "scrape_status": s_status,
            "consecutive_failures": source.consecutive_failures,
            "last_scraped_at": source.last_scraped_at.isoformat() if source.last_scraped_at else None,
            "last_run_at": last_run_at.isoformat() if last_run_at else None,
            "last_error": source.last_error,
        })

    return {
        "total_sources": len(sources_list),
        "status_counts": status_counts,
        "sources": sources_list,
    }
