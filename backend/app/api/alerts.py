"""Alerts API — trigger digest generation and delivery."""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.services.alerts import process_and_notify, generate_digest, render_digest_html
from app.api.dependencies import verify_cron_secret

router = APIRouter()


@router.post("/notify", dependencies=[Depends(verify_cron_secret)])
async def trigger_notifications(db: AsyncSession = Depends(get_db)):
    """Generate and send digests for all tracks with pending matches."""
    stats = await process_and_notify(db)
    return {"status": "completed", "stats": stats}


@router.get("/digest/{track_id}", dependencies=[Depends(verify_cron_secret)])
async def preview_digest(track_id: int, db: AsyncSession = Depends(get_db)):
    """Preview a digest for a specific track (without sending)."""
    digest = await generate_digest(db, track_id)
    if not digest:
        return {"status": "empty", "message": "No pending matches for this track"}
    return digest


@router.get("/digest/{track_id}/html", dependencies=[Depends(verify_cron_secret)])
async def preview_digest_html(track_id: int, db: AsyncSession = Depends(get_db)):
    """Preview the HTML email for a track's digest."""
    from fastapi.responses import HTMLResponse

    digest = await generate_digest(db, track_id)
    if not digest:
        return HTMLResponse("<p>No pending matches for this track.</p>")
    html = render_digest_html(digest)
    return HTMLResponse(html)
