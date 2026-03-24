"""Instant alert service — send immediate email alerts when new matching items are detected."""

import logging
from datetime import datetime
from urllib.parse import quote

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.subscriber import Subscriber
from app.models.document import Document
from app.models.municipality import Municipality
from app.services.digest import build_digest_items
from app.config import settings

logger = logging.getLogger(__name__)


def render_alert_email(
    item: dict,
    municipality_name: str,
    date_str: str,
    unsubscribe_url: str,
) -> str:
    """Render a short, immediate alert HTML email for a single matched item."""
    verified_badge = ""
    if item.get("verification_status") == "verified":
        verified_badge = (
            ' <span style="display:inline-block;background:#d1fae5;color:#065f46;'
            'font-size:11px;padding:2px 6px;border-radius:4px;margin-left:6px;">'
            "&#10003; Verified</span>"
        )
    elif item.get("verification_status") == "partially_verified":
        verified_badge = (
            ' <span style="display:inline-block;background:#fef3c7;color:#92400e;'
            'font-size:11px;padding:2px 6px;border-radius:4px;margin-left:6px;">'
            "&#9888; Partially Verified</span>"
        )

    topics_html = ""
    if item.get("matched_topics"):
        topics_html = (
            '<p style="font-size:12px;color:#6b7280;margin:8px 0 0;">'
            f'Topics: {", ".join(item["matched_topics"])}</p>'
        )

    summary_html = ""
    if item.get("summary"):
        summary_html = (
            f'<p style="margin:12px 0 0;color:#4b5563;font-size:14px;line-height:1.5;">'
            f'{item["summary"]}</p>'
        )

    key_points_html = ""
    if item.get("key_points"):
        points = "".join(
            f'<li style="margin-bottom:4px;">{p}</li>' for p in item["key_points"]
        )
        key_points_html = (
            f'<ul style="margin:8px 0 0;padding-left:20px;color:#374151;">{points}</ul>'
        )

    doc_type = item.get("doc_type", "document").upper()
    title = item.get("title", "Untitled")
    url = item.get("url", "#")

    return f"""
    <html>
    <body style="font-family:system-ui,-apple-system,sans-serif;max-width:600px;margin:0 auto;padding:20px;color:#1a1a1a;background:#f9fafb;">
        <div style="background:white;border-radius:12px;padding:24px;border:1px solid #e5e7eb;">
            <div style="border-bottom:3px solid #1e40af;padding-bottom:16px;margin-bottom:24px;">
                <h1 style="color:#1e40af;margin:0;font-size:24px;">BC Hearing Watch</h1>
                <p style="color:#6b7280;margin:4px 0 0;font-size:14px;">Immediate Alert</p>
            </div>

            <div style="background:#eff6ff;border-radius:8px;padding:4px 12px;display:inline-block;margin-bottom:16px;">
                <span style="font-size:12px;color:#1e40af;font-weight:600;">{doc_type}</span>
            </div>

            <h2 style="color:#111;font-size:18px;margin:0 0 8px;">
                <a href="{url}" style="color:#1e40af;text-decoration:none;">{title}</a>
                {verified_badge}
            </h2>

            <p style="color:#6b7280;font-size:13px;margin:0 0 12px;">
                {municipality_name} &bull; {date_str}
            </p>

            {summary_html}
            {key_points_html}
            {topics_html}

            <div style="margin-top:20px;">
                <a href="{url}" style="display:inline-block;background:#1e40af;color:white;padding:10px 20px;border-radius:6px;text-decoration:none;font-size:14px;font-weight:500;">
                    View Full Document
                </a>
            </div>
        </div>

        <div style="margin-top:20px;padding:16px;text-align:center;">
            <p style="font-size:12px;color:#9ca3af;line-height:1.5;">
                This is an experimental personal tool using public data.
                AI summaries may contain errors. Always verify with original municipal sources.
                Not official government communication.
            </p>
            <p style="margin-top:12px;">
                <a href="{unsubscribe_url}" style="color:#9ca3af;font-size:12px;">
                    Unsubscribe from all emails
                </a>
            </p>
        </div>
    </body>
    </html>
    """


def send_alert_via_resend(
    to_email: str,
    html: str,
    municipality_name: str,
    date_str: str,
) -> bool:
    """Send an immediate alert email via Resend. Returns True on success."""
    if not settings.resend_api_key:
        logger.warning("RESEND_API_KEY not set — skipping alert email")
        return False

    try:
        import resend
        resend.api_key = settings.resend_api_key

        resend.Emails.send({
            "from": settings.resend_from_email,
            "to": [to_email],
            "subject": f"BC Hearing Alert \u2013 {municipality_name} {date_str}",
            "html": html,
        })
        logger.info(f"Immediate alert sent to {to_email} for {municipality_name}")
        return True
    except Exception as e:
        logger.error(f"Failed to send alert to {to_email}: {e}")
        return False


async def send_immediate_alerts_for_documents(
    db: AsyncSession,
    new_documents: list[Document],
    base_url: str = "",
) -> dict:
    """Send immediate alerts to subscribers who have immediate_alerts=True.

    Called after polling discovers new documents.
    Matches each new document against each subscriber's preferences.

    Returns stats dict.
    """
    stats = {
        "subscribers_checked": 0,
        "alerts_sent": 0,
        "alerts_failed": 0,
        "documents_matched": 0,
    }

    if not new_documents:
        return stats

    # Get all active subscribers with immediate_alerts enabled
    result = await db.execute(
        select(Subscriber).where(
            Subscriber.active.is_(True),
            Subscriber.immediate_alerts.is_(True),
        )
    )
    subscribers = result.scalars().all()

    if not subscribers:
        logger.info("No subscribers with immediate alerts enabled")
        return stats

    # Build municipality lookup for the new documents
    muni_ids = {doc.municipality_id for doc in new_documents}
    result = await db.execute(
        select(Municipality).where(Municipality.id.in_(muni_ids))
    )
    munis = {m.id: m for m in result.scalars().all()}

    # Build (doc, muni) pairs
    docs_with_munis = [
        (doc, munis[doc.municipality_id])
        for doc in new_documents
        if doc.municipality_id in munis
    ]

    date_str = datetime.utcnow().strftime("%B %d, %Y")

    for subscriber in subscribers:
        stats["subscribers_checked"] += 1

        sub_munis = subscriber.municipalities or []
        sub_topics = subscriber.topics or []

        if not sub_munis and not sub_topics:
            continue

        # Filter docs to subscriber's municipalities
        relevant_docs = [
            (doc, muni) for doc, muni in docs_with_munis
            if muni.short_name in sub_munis
        ]

        if not relevant_docs:
            continue

        # Match against subscriber's topics/keywords
        matched_items = build_digest_items(relevant_docs, sub_topics, subscriber.keywords)

        if not matched_items:
            continue

        stats["documents_matched"] += len(matched_items)

        # Build unsubscribe URL
        unsubscribe_url = f"{base_url}/api/v1/unsubscribe?email={quote(subscriber.email)}"

        # Send one alert email per matched item
        for item in matched_items:
            html = render_alert_email(
                item=item,
                municipality_name=item.get("municipality", "Unknown"),
                date_str=date_str,
                unsubscribe_url=unsubscribe_url,
            )

            success = send_alert_via_resend(
                to_email=subscriber.email,
                html=html,
                municipality_name=item.get("municipality", "Unknown"),
                date_str=date_str,
            )
            if success:
                stats["alerts_sent"] += 1
            else:
                stats["alerts_failed"] += 1

    logger.info(
        f"Immediate alerts: {stats['subscribers_checked']} subscribers checked, "
        f"{stats['alerts_sent']} alerts sent, {stats['documents_matched']} docs matched"
    )
    return stats
