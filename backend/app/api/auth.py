"""Auth API — magic link confirmation for subscriber preference updates."""

import logging
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.database import get_db
from app.models.magic_link import MagicLinkToken
from app.models.subscriber import Subscriber
from app.config import settings

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/auth/confirm")
async def confirm_magic_link(token: str, db: AsyncSession = Depends(get_db)):
    """Apply pending preference changes when a subscriber clicks a magic link.

    Looks up the token, validates it has not been used or expired, applies the
    stored pending_preferences to the subscriber row, marks the token as used,
    and redirects to the frontend with ?confirmed=true.

    Returns 404 for unknown tokens and 410 for expired or already-used tokens
    so the subscriber gets a clear error rather than a silent no-op.
    """
    result = await db.execute(
        select(MagicLinkToken).where(MagicLinkToken.token == token)
    )
    magic_link = result.scalar_one_or_none()

    if not magic_link:
        raise HTTPException(status_code=404, detail="Invalid confirmation link.")

    if not magic_link.is_valid:
        raise HTTPException(
            status_code=410,
            detail=(
                "This confirmation link has already been used or has expired. "
                "Submit the preferences form again to receive a new link."
            ),
        )

    # Apply the pending preferences to the subscriber row.
    sub_result = await db.execute(
        select(Subscriber).where(Subscriber.email == magic_link.email)
    )
    subscriber = sub_result.scalar_one_or_none()

    if not subscriber:
        # Subscriber was deleted between token creation and confirmation.
        raise HTTPException(status_code=404, detail="Subscriber not found.")

    prefs = magic_link.pending_preferences
    subscriber.municipalities = prefs.get("municipalities", subscriber.municipalities)
    subscriber.topics = prefs.get("topics", subscriber.topics)
    subscriber.keywords = prefs.get("keywords", subscriber.keywords)
    subscriber.immediate_alerts = prefs.get("immediate_alerts", subscriber.immediate_alerts)
    subscriber.active = True
    subscriber.updated_at = datetime.now(timezone.utc)

    # Consume the token — prevents replay.
    magic_link.used_at = datetime.now(timezone.utc)

    await db.commit()
    logger.info("Preferences updated for %s via magic link", magic_link.email)

    # Redirect to the frontend success page.
    # If app_base_url is not configured (local dev) return JSON instead.
    if settings.app_base_url:
        return RedirectResponse(url=f"{settings.app_base_url}?confirmed=true", status_code=302)

    return {"status": "ok", "message": "Preferences updated successfully."}
