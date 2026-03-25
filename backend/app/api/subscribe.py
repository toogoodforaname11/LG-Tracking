"""Subscribe API — upsert subscriber preferences, unsubscribe, send confirmation."""

import logging
from datetime import datetime, timedelta, timezone
from urllib.parse import quote

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.database import get_db
from app.models.subscriber import Subscriber
from app.models.magic_link import MagicLinkToken
from app.config import settings

logger = logging.getLogger(__name__)

router = APIRouter()

MAGIC_LINK_TTL_HOURS = 24


# --- Pydantic schemas ---


class SubscribeRequest(BaseModel):
    email: EmailStr
    municipalities: list[str]  # list of short_names like ["Colwood", "Victoria"]
    topics: list[str]
    keywords: str = ""
    immediate_alerts: bool = False


class SubscribeResponse(BaseModel):
    status: str
    email: str
    message: str


class UnsubscribeResponse(BaseModel):
    status: str
    message: str


# --- Email helpers ---


def send_confirmation_email(
    email: str,
    municipalities: list[str],
    topics: list[str],
    immediate_alerts: bool,
    unsubscribe_url: str,
) -> None:
    """Send a new-subscriber confirmation email via Resend.

    Called as a BackgroundTask so it never blocks the API response.
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
        logger.info("Confirmation email sent to %s", email)

    except Exception as e:
        logger.error("Failed to send confirmation email to %s: %s", email, e)


def send_magic_link_email(email: str, confirm_url: str) -> None:
    """Send a magic link email so the subscriber can confirm their preference update.

    Called as a BackgroundTask. Errors are logged but do not surface to the caller —
    the pending token has already been stored in the database.
    """
    if not settings.resend_api_key:
        logger.warning("RESEND_API_KEY not set — skipping magic link email (token stored in DB)")
        return

    try:
        import resend
        resend.api_key = settings.resend_api_key

        html = f"""
        <html>
        <body style="font-family:system-ui,-apple-system,sans-serif;max-width:600px;margin:0 auto;padding:20px;color:#1a1a1a;">
            <div style="border-bottom:3px solid #1e40af;padding-bottom:16px;margin-bottom:24px;">
                <h1 style="color:#1e40af;margin:0;font-size:24px;">BC Local Government Council Tracker</h1>
                <p style="color:#6b7280;margin:4px 0 0;font-size:14px;">Municipal Council Alerts &amp; Digest</p>
            </div>

            <h2 style="color:#111;font-size:20px;">Confirm Your Preference Update</h2>
            <p style="color:#374151;line-height:1.6;">
                We received a request to update your subscription preferences.
                Click the button below to confirm the changes. This link expires in 24 hours.
            </p>

            <div style="text-align:center;margin:32px 0;">
                <a href="{confirm_url}"
                   style="background:#1e40af;color:#fff;padding:14px 32px;border-radius:8px;
                          text-decoration:none;font-size:16px;font-weight:600;display:inline-block;">
                    Confirm Preference Update
                </a>
            </div>

            <p style="color:#6b7280;font-size:13px;line-height:1.6;">
                If you did not request this change, you can safely ignore this email —
                your existing preferences will not be changed.
            </p>

            <p style="color:#6b7280;font-size:12px;">
                Or copy this link into your browser:<br>
                <span style="word-break:break-all;">{confirm_url}</span>
            </p>
        </body>
        </html>
        """

        resend.Emails.send({
            "from": settings.resend_from_email,
            "to": [email],
            "subject": "BC Local Government Council Tracker — Confirm Your Preference Update",
            "html": html,
        })
        logger.info("Magic link email sent to %s", email)

    except Exception as e:
        logger.error("Failed to send magic link email to %s: %s", email, e)


# --- Endpoints ---


@router.post("/subscribe", response_model=SubscribeResponse)
async def subscribe(
    req: SubscribeRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    """Subscribe or update preferences.

    - New email → subscriber created immediately, confirmation email sent.
    - Existing email → pending preferences stored as a magic link token,
      confirmation email sent to that address. Changes are only applied
      after the subscriber clicks the link, preventing anyone from changing
      another person's preferences without access to their inbox.
    """
    result = await db.execute(
        select(Subscriber).where(Subscriber.email == req.email)
    )
    existing = result.scalar_one_or_none()

    if existing:
        # --- Existing subscriber: require email verification ---
        expires_at = datetime.now(timezone.utc) + timedelta(hours=MAGIC_LINK_TTL_HOURS)
        token = MagicLinkToken(
            email=req.email,
            pending_preferences={
                "municipalities": req.municipalities,
                "topics": req.topics,
                "keywords": req.keywords,
                "immediate_alerts": req.immediate_alerts,
            },
            expires_at=expires_at,
        )
        db.add(token)
        await db.commit()
        await db.refresh(token)

        confirm_url = (
            f"{settings.app_base_url}/api/v1/auth/confirm"
            f"?token={quote(token.token)}"
        )
        background_tasks.add_task(send_magic_link_email, req.email, confirm_url)

        return SubscribeResponse(
            status="magic_link_sent",
            email=req.email,
            message=(
                "A confirmation link has been sent to your email. "
                "Click it to apply your updated preferences."
            ),
        )

    # --- New subscriber: create immediately ---
    subscriber = Subscriber(
        email=req.email,
        municipalities=req.municipalities,
        topics=req.topics,
        keywords=req.keywords,
        immediate_alerts=req.immediate_alerts,
        active=True,
    )
    db.add(subscriber)
    await db.commit()
    await db.refresh(subscriber)

    # Send confirmation email in background — does not block the API response
    # and does not cause the subscribe action to fail if email delivery fails.
    # Skip if APP_BASE_URL is not configured (unsubscribe links would be broken).
    alerts_msg = ""
    if req.immediate_alerts:
        alerts_msg = " You will also receive immediate alerts when new matching items are detected."

    if settings.app_base_url:
        unsubscribe_url = (
            f"{settings.app_base_url}/api/v1/unsubscribe"
            f"?token={quote(subscriber.unsubscribe_token)}"
        )
        background_tasks.add_task(
            send_confirmation_email,
            req.email,
            req.municipalities,
            req.topics,
            req.immediate_alerts,
            unsubscribe_url,
        )
    else:
        logger.warning("APP_BASE_URL not set — skipping confirmation email (unsubscribe links would be broken)")

    return SubscribeResponse(
        status="created",
        email=req.email,
        message=f"Preferences saved! You will receive weekly digests every Sunday.{alerts_msg}",
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
