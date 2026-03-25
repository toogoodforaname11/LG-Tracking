"""Subscribe API — upsert subscriber preferences, unsubscribe, send confirmation."""

import logging
from datetime import datetime, timezone
from urllib.parse import quote

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.database import get_db
from app.models.subscriber import Subscriber
from app.config import settings

logger = logging.getLogger(__name__)

router = APIRouter()


# --- Pydantic schemas ---


class SubscribeRequest(BaseModel):
    email: EmailStr
    municipalities: list[str]  # list of short_names like ["Colwood", "Victoria"]
    topics: list[str]
    keywords: str = ""
    immediate_alerts: bool = False
    edit_token: str | None = None  # Required when updating an existing subscription


class SubscribeResponse(BaseModel):
    status: str
    email: str
    message: str
    edit_token: str | None = None  # Returned on new subscription for future updates


class UnsubscribeResponse(BaseModel):
    status: str
    message: str


# --- Email helper ---


def send_confirmation_email(
    email: str,
    municipalities: list[str],
    topics: list[str],
    immediate_alerts: bool,
    unsubscribe_url: str,
) -> None:
    """Send a confirmation email via Resend.

    Called as a BackgroundTask so it never blocks the API response.
    Logs errors but does not propagate — the subscribe action already succeeded.
    """
    if not settings.resend_api_key:
        logger.warning("RESEND_API_KEY not set — skipping confirmation email")
        return

    try:
        import resend
        resend.api_key = settings.resend_api_key

        muni_list = ", ".join(municipalities) if municipalities else "None selected"
        topic_list = ", ".join(topics) if topics else "None selected"

        alerts_note = ""
        if immediate_alerts:
            alerts_note = """
            <div style="background:#fef3c7;border-radius:8px;padding:12px 16px;margin:16px 0;border-left:4px solid #f59e0b;">
                <p style="margin:0;font-size:14px;color:#92400e;">
                    <strong>Immediate Alerts: ON</strong> — You will receive an email
                    within minutes whenever a new matching council item is detected.
                </p>
            </div>
            """

        html = f"""
        <html>
        <body style="font-family:system-ui,-apple-system,sans-serif;max-width:600px;margin:0 auto;padding:20px;color:#1a1a1a;">
            <div style="border-bottom:3px solid #1e40af;padding-bottom:16px;margin-bottom:24px;">
                <h1 style="color:#1e40af;margin:0;font-size:24px;">BC Local Government Council Tracker</h1>
                <p style="color:#6b7280;margin:4px 0 0;font-size:14px;">Municipal Council Alerts &amp; Digest</p>
            </div>

            <h2 style="color:#111;font-size:20px;">Preferences Saved!</h2>
            <p style="color:#374151;line-height:1.6;">
                Your subscription has been confirmed. Here's what you signed up for:
            </p>

            <div style="background:#f0f4ff;border-radius:8px;padding:16px;margin:16px 0;">
                <p style="margin:0 0 8px;"><strong>Municipalities:</strong> {muni_list}</p>
                <p style="margin:0 0 8px;"><strong>Topics:</strong> {topic_list}</p>
                <p style="margin:0;"><strong>Immediate Alerts:</strong> {'Enabled' if immediate_alerts else 'Disabled'}</p>
            </div>

            {alerts_note}

            <p style="color:#374151;line-height:1.6;">
                You will receive weekly digests every <strong>Sunday at 8 PM Pacific</strong>
                with AI-summarized updates from your selected municipalities.
            </p>

            <p style="color:#374151;line-height:1.6;">
                To update your preferences, visit the form again and submit with the same email address.
            </p>

            <hr style="border:none;border-top:1px solid #e5e7eb;margin:24px 0;">

            <p style="font-size:11px;color:#9ca3af;line-height:1.5;">
                This is an experimental personal tool using public data.
                AI summaries may contain errors. Always verify with original municipal sources.
                Not official government communication.<br><br>
                <a href="{unsubscribe_url}" style="color:#6b7280;">Unsubscribe from all emails</a>
            </p>
        </body>
        </html>
        """

        resend.Emails.send({
            "from": settings.resend_from_email,
            "to": [email],
            "subject": "BC Local Government Council Tracker — Subscription Confirmed",
            "html": html,
        })
        logger.info(f"Confirmation email sent to {email}")

    except Exception as e:
        logger.error(f"Failed to send confirmation email to {email}: {e}")


# --- Endpoints ---


@router.post("/subscribe", response_model=SubscribeResponse)
async def subscribe(
    req: SubscribeRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    """Subscribe or update preferences. Same email = overwrite."""
    result = await db.execute(
        select(Subscriber).where(Subscriber.email == req.email)
    )
    existing = result.scalar_one_or_none()

    if existing:
        # Updating an existing subscription requires proof of ownership via
        # the edit_token (which is the subscriber's unsubscribe_token UUID).
        # Without this check, anyone who knows an email address could
        # overwrite that subscriber's preferences — an account-integrity
        # violation.
        if not req.edit_token or req.edit_token != existing.unsubscribe_token:
            raise HTTPException(
                status_code=403,
                detail="edit_token is required to update an existing subscription. "
                "Check your confirmation email for the edit link.",
            )
        existing.municipalities = req.municipalities
        existing.topics = req.topics
        existing.keywords = req.keywords
        existing.immediate_alerts = req.immediate_alerts
        existing.active = True
        existing.updated_at = datetime.now(timezone.utc)
        subscriber = existing
        action = "updated"
    else:
        subscriber = Subscriber(
            email=req.email,
            municipalities=req.municipalities,
            topics=req.topics,
            keywords=req.keywords,
            immediate_alerts=req.immediate_alerts,
            active=True,
        )
        db.add(subscriber)
        action = "created"

    await db.commit()
    await db.refresh(subscriber)

    # Build token-based unsubscribe URL — never exposes the email in the URL.
    unsubscribe_url = (
        f"{settings.app_base_url}/api/v1/unsubscribe?token={quote(subscriber.unsubscribe_token)}"
    )

    # Send confirmation email in background — does not block the API response
    # and does not cause the subscribe action to fail if email delivery fails.
    background_tasks.add_task(
        send_confirmation_email,
        req.email,
        req.municipalities,
        req.topics,
        req.immediate_alerts,
        unsubscribe_url,
    )

    alerts_msg = ""
    if req.immediate_alerts:
        alerts_msg = " You will also receive immediate alerts when new matching items are detected."

    return SubscribeResponse(
        status="ok",
        email=req.email,
        message=(
            f"Preferences {action}! You will receive weekly digests every Sunday.{alerts_msg}"
        ),
        edit_token=subscriber.unsubscribe_token if action == "created" else None,
    )


@router.get("/unsubscribe")
async def unsubscribe(token: str, db: AsyncSession = Depends(get_db)):
    """One-click unsubscribe via signed token — sets active=False.

    The token parameter is the subscriber's unsubscribe_token (UUID), not their
    email address. This prevents any caller who knows someone's email from
    unsubscribing them without their consent.
    """
    result = await db.execute(
        select(Subscriber).where(Subscriber.unsubscribe_token == token)
    )
    subscriber = result.scalar_one_or_none()

    if not subscriber:
        raise HTTPException(status_code=404, detail="Invalid unsubscribe token")

    subscriber.active = False
    subscriber.updated_at = datetime.now(timezone.utc)
    await db.commit()

    return UnsubscribeResponse(
        status="ok",
        message="You have been unsubscribed. You will no longer receive emails.",
    )
