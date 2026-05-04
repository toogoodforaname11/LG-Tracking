"""Subscribe API — upsert subscriber preferences, unsubscribe, send confirmation."""

import logging
from datetime import datetime, timedelta, timezone
from urllib.parse import quote

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from pydantic import BaseModel, EmailStr, field_validator
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.database import get_db
from app.models.subscriber import Subscriber
from app.models.magic_link import MagicLinkToken
from app.models.municipality import Municipality, PROVINCE_BC, VALID_PROVINCES
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
    # Province scope for the selected municipalities. Defaults to BC for
    # backward compatibility with the legacy frontend.
    province: str = PROVINCE_BC

    @field_validator("province")
    @classmethod
    def _validate_province(cls, v: str) -> str:
        if v not in VALID_PROVINCES:
            raise ValueError(
                f"Invalid province '{v}'. Must be one of: {sorted(VALID_PROVINCES)}"
            )
        return v


class SubscribeResponse(BaseModel):
    status: str
    email: str
    message: str


class UnsubscribeResponse(BaseModel):
    status: str
    message: str


# --- Email helpers ---


def send_confirmation_link_email(email: str, confirm_url: str) -> None:
    """Send a confirmation email for new subscribers so they verify their address.

    Called as a BackgroundTask. The subscription stays inactive until they click.
    """
    from app.services.email import send_email

    html = f"""
    <html>
    <body style="font-family:system-ui,-apple-system,sans-serif;max-width:600px;margin:0 auto;padding:20px;color:#1a1a1a;">
        <div style="border-bottom:3px solid #1e40af;padding-bottom:16px;margin-bottom:24px;">
            <h1 style="color:#1e40af;margin:0;font-size:24px;">BC Local Government Council Tracker</h1>
            <p style="color:#6b7280;margin:4px 0 0;font-size:14px;">Municipal Council Alerts &amp; Digest</p>
        </div>

        <h2 style="color:#111;font-size:20px;">Confirm Your Email</h2>
        <p style="color:#374151;line-height:1.6;">
            Thanks for subscribing! Please click the button below to verify your
            email address and activate your subscription. This link expires in 24 hours.
        </p>

        <div style="text-align:center;margin:32px 0;">
            <a href="{confirm_url}"
               style="background:#1e40af;color:#fff;padding:14px 32px;border-radius:8px;
                      text-decoration:none;font-size:16px;font-weight:600;display:inline-block;">
                Confirm Subscription
            </a>
        </div>

        <p style="color:#6b7280;font-size:13px;line-height:1.6;">
            If you did not sign up for this service, you can safely ignore this email &mdash;
            no subscription will be created.
        </p>

        <p style="color:#6b7280;font-size:12px;">
            Or copy this link into your browser:<br>
            <span style="word-break:break-all;">{confirm_url}</span>
        </p>
    </body>
    </html>
    """

    send_email(
        to_email=email,
        subject="BC Local Government Council Tracker — Confirm Your Email",
        html=html,
    )


def send_magic_link_email(email: str, confirm_url: str) -> None:
    """Send a magic link email so the subscriber can confirm their preference update.

    Called as a BackgroundTask. Errors are logged but do not surface to the caller —
    the pending token has already been stored in the database.
    """
    from app.services.email import send_email

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

    send_email(
        to_email=email,
        subject="BC Local Government Council Tracker — Confirm Your Preference Update",
        html=html,
    )


# --- Endpoints ---


@router.post("/subscribe", response_model=SubscribeResponse)
async def subscribe(
    req: SubscribeRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    """Subscribe or update preferences (double opt-in).

    - New email → inactive subscriber created, confirmation link emailed.
      Subscription activates only after the email owner clicks the link.
    - Existing email → pending preferences stored as a magic link token,
      confirmation link emailed. Changes apply only after clicking the link.

    This prevents anyone from subscribing or modifying preferences for an
    email address they don't control.
    """
    # Validate that every selected municipality short_name actually exists in
    # the requested province. This prevents a malicious / mistyped client from
    # registering subscriptions for nonexistent or wrong-province munis.
    if req.municipalities:
        muni_result = await db.execute(
            select(Municipality.short_name).where(
                Municipality.province == req.province,
                Municipality.short_name.in_(req.municipalities),
                Municipality.is_active.is_(True),
            )
        )
        known = {row for row in muni_result.scalars().all()}
        unknown = [name for name in req.municipalities if name not in known]
        if unknown:
            raise HTTPException(
                status_code=422,
                detail=(
                    f"Unknown municipalities for province '{req.province}': "
                    f"{unknown}"
                ),
            )

    result = await db.execute(
        select(Subscriber).where(Subscriber.email == req.email)
    )
    existing = result.scalar_one_or_none()

    # Both new and existing subscribers go through email verification.
    # This prevents anyone from subscribing or changing preferences for
    # an email address they don't control.

    pending_prefs = {
        "municipalities": req.municipalities,
        "topics": req.topics,
        "keywords": req.keywords,
        "immediate_alerts": req.immediate_alerts,
        "province": req.province,
    }

    # An "unverified" subscriber is one that exists but has never confirmed
    # their email (active=False from initial sign-up).  Treat them the same
    # as a brand-new subscriber: update their pending prefs and re-send the
    # confirmation link.
    is_new = not existing
    is_unverified = existing and not existing.active

    if is_new:
        # Create an inactive subscriber row so the confirm endpoint
        # can activate it once the email owner clicks the link.
        subscriber = Subscriber(
            email=req.email,
            municipalities=req.municipalities,
            topics=req.topics,
            keywords=req.keywords,
            immediate_alerts=req.immediate_alerts,
            province=req.province,
            active=False,  # Stays inactive until email is verified
        )
        db.add(subscriber)
        await db.flush()
    elif is_unverified:
        # Update the inactive row with the latest preferences so the
        # confirm endpoint applies the most recent choices.
        existing.municipalities = req.municipalities
        existing.topics = req.topics
        existing.keywords = req.keywords
        existing.immediate_alerts = req.immediate_alerts
        existing.province = req.province

    expires_at = datetime.now(timezone.utc) + timedelta(hours=MAGIC_LINK_TTL_HOURS)
    token = MagicLinkToken(
        email=req.email,
        pending_preferences=pending_prefs,
        expires_at=expires_at,
    )
    db.add(token)
    await db.commit()
    await db.refresh(token)

    confirm_url = (
        f"{settings.app_base_url}/api/v1/auth/confirm"
        f"?token={quote(token.token)}"
    )

    if is_new or is_unverified:
        background_tasks.add_task(send_confirmation_link_email, req.email, confirm_url)
        message = (
            "A confirmation link has been sent to your email. "
            "Click it to activate your subscription."
        )
    else:
        background_tasks.add_task(send_magic_link_email, req.email, confirm_url)
        message = (
            "A confirmation link has been sent to your email. "
            "Click it to apply your updated preferences."
        )

    return SubscribeResponse(
        status="magic_link_sent",
        email=req.email,
        message=message,
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
