"""Cron API — endpoints triggered by Vercel cron or manual invocation."""

import logging
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.database import get_db
from app.services.digest import run_weekly_digest
from app.services.instant_alerts import send_immediate_alerts_for_documents
from app.discovery.poller import run_discovery
from app.ai.processor import process_new_documents
from app.models.document import Document

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/weekly-digest")
async def trigger_weekly_digest(
    db: AsyncSession = Depends(get_db),
):
    """Weekly digest cron job.

    Triggered by Vercel Cron every Sunday at 8 PM Pacific (03:00 UTC Monday).
    Can also be triggered manually for testing.
    """
    stats = await run_weekly_digest(db)
    return {"status": "completed", "stats": stats}


@router.post("/poll")
async def trigger_poll(
    db: AsyncSession = Depends(get_db),
):
    """Poll all active sources for new documents.

    Triggered every 30 minutes by Vercel Cron.
    Automatically sends immediate alerts to subscribers when new docs are found.
    """
    results = await run_discovery(db)
    processing_stats = await process_new_documents(db)
    return {"status": "completed", "results": results, "processing": processing_stats}


@router.post("/poll-and-digest")
async def poll_then_digest(
    db: AsyncSession = Depends(get_db),
):
    """Full pipeline: poll sources for new documents, then run weekly digest.

    Useful for testing the complete flow.
    """
    poll_results = await run_discovery(db)
    logger.info(f"Poll complete: {poll_results}")

    processing_stats = await process_new_documents(db)
    logger.info(f"Processing complete: {processing_stats}")

    digest_stats = await run_weekly_digest(db)

    return {
        "status": "completed",
        "poll_results": poll_results,
        "processing_stats": processing_stats,
        "digest_stats": digest_stats,
    }


@router.get("/trigger-alerts")
async def trigger_alerts_test(
    email: str = Query(..., description="Email address to send test alerts to"),
    db: AsyncSession = Depends(get_db),
):
    """Manual test endpoint — sends immediate alerts for recent documents.

    Sends alerts to the specified email address for any documents
    discovered in the last 24 hours, regardless of subscriber preferences.
    Useful for testing the alert email rendering and delivery.
    """
    # Get recent documents (last 24 hours)
    cutoff = datetime.utcnow() - timedelta(hours=24)
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

    # Send alerts for these docs
    alert_stats = await send_immediate_alerts_for_documents(db, recent_docs)

    return {
        "status": "completed",
        "test_email": email,
        "documents_found": len(recent_docs),
        "alert_stats": alert_stats,
    }
