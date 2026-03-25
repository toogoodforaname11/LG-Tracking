"""Cron API — endpoints triggered by Vercel cron or manual invocation."""

import logging
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.services.digest import run_weekly_digest
from app.discovery.poller import run_discovery
from app.ai.processor import process_new_documents
from app.api.dependencies import verify_cron_secret

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/weekly-digest", dependencies=[Depends(verify_cron_secret)])
async def trigger_weekly_digest(
    db: AsyncSession = Depends(get_db),
):
    """Weekly digest cron job.

    Triggered by Vercel Cron every Sunday at 8 PM Pacific (04:00 UTC Monday).
    Protected by X-Cron-Secret header when CRON_SECRET is configured.
    """
    stats = await run_weekly_digest(db)
    return {"status": "completed", "stats": stats}


@router.post("/poll", dependencies=[Depends(verify_cron_secret)])
async def trigger_poll(
    db: AsyncSession = Depends(get_db),
):
    """Poll all active sources for new documents.

    Triggered every 30 minutes by Vercel Cron.
    Automatically sends immediate alerts to subscribers when new docs are found.
    Protected by X-Cron-Secret header when CRON_SECRET is configured.
    """
    results = await run_discovery(db)
    processing_stats = await process_new_documents(db)
    return {"status": "completed", "results": results, "processing": processing_stats}


@router.post("/poll-and-digest", dependencies=[Depends(verify_cron_secret)])
async def poll_then_digest(
    db: AsyncSession = Depends(get_db),
):
    """Full pipeline: poll sources for new documents, then run weekly digest.

    Useful for testing the complete flow end-to-end.
    Protected by X-Cron-Secret header when CRON_SECRET is configured.
    """
    poll_results = await run_discovery(db)
    logger.info("Poll complete: %s", poll_results)

    processing_stats = await process_new_documents(db)
    logger.info("Processing complete: %s", processing_stats)

    digest_stats = await run_weekly_digest(db)

    return {
        "status": "completed",
        "poll_results": poll_results,
        "processing_stats": processing_stats,
        "digest_stats": digest_stats,
    }


@router.get("/trigger-alerts", dependencies=[Depends(verify_cron_secret)])
async def trigger_alerts_test(
    db: AsyncSession = Depends(get_db),
):
    """Manual test endpoint — sends immediate alerts for documents found in last 24 hours.

    Delivers alerts to all active subscribers who have immediate_alerts=True and
    whose preferences match the recent documents. This exercises the real alert
    delivery path, not a test-only code path.

    Protected by X-Cron-Secret header when CRON_SECRET is configured.
    """
    from app.models.document import Document
    from app.services.instant_alerts import send_immediate_alerts_for_documents

    cutoff = datetime.now(timezone.utc) - timedelta(hours=24)
    from sqlalchemy import select
    result = await db.execute(
        select(Document)
        .where(Document.first_seen_at >= cutoff)
        .order_by(Document.first_seen_at.desc())
        .limit(5)
    )
    recent_docs = list(result.scalars().all())

    if not recent_docs:
        return {
            "status": "no_documents",
            "message": "No documents found in the last 24 hours. Run /api/v1/cron/poll first.",
        }

    alert_stats = await send_immediate_alerts_for_documents(db, recent_docs)

    return {
        "status": "completed",
        "documents_found": len(recent_docs),
        "alert_stats": alert_stats,
    }
