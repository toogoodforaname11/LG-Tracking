"""Cron API — endpoints triggered by Vercel cron or manual invocation."""

import logging

from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.services.digest import run_weekly_digest
from app.discovery.poller import run_discovery
from app.config import settings

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/weekly-digest")
async def trigger_weekly_digest(
    db: AsyncSession = Depends(get_db),
    authorization: str | None = Header(None),
):
    """Weekly digest cron job.

    Triggered by Vercel Cron every Sunday at 8 PM Pacific (03:00 UTC Monday).
    Can also be triggered manually for testing.
    """
    # Optional: verify cron secret for Vercel
    # In production, set CRON_SECRET env var and Vercel sends it as Authorization header
    stats = await run_weekly_digest(db)
    return {"status": "completed", "stats": stats}


@router.post("/poll-and-digest")
async def poll_then_digest(
    db: AsyncSession = Depends(get_db),
):
    """Full pipeline: poll sources for new documents, then run weekly digest.

    Useful for testing the complete flow.
    """
    # Step 1: Poll all active sources for new documents
    poll_stats = await run_discovery(db)
    logger.info(f"Poll complete: {poll_stats}")

    # Step 2: Run the weekly digest
    digest_stats = await run_weekly_digest(db)

    return {
        "status": "completed",
        "poll_stats": poll_stats,
        "digest_stats": digest_stats,
    }
