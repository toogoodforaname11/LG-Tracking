"""Weekly digest service — run discovery, process, and email all active subscribers."""

import logging
from datetime import datetime, timedelta, timezone
from urllib.parse import quote

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.subscriber import Subscriber
from app.models.document import Document
from app.models.municipality import Municipality
from app.config import settings

logger = logging.getLogger(__name__)


def render_digest_email(
    subscriber_email: str,
    items: list[dict],
    date_str: str,
    unsubscribe_url: str,
) -> str:
    """Render a beautiful HTML digest email."""
    if not items:
        items_html = """
        <div style="text-align:center;padding:32px;color:#6b7280;">
            <p style="font-size:16px;">No new updates matched your preferences this week.</p>
            <p style="font-size:14px;">We'll keep watching and notify you when something comes up.</p>
        </div>
        """
    else:
        items_html = ""
        for item in items:
            verified_badge = ""
            if item.get("verification_status") == "verified":
                verified_badge = (
                    ' <span style="display:inline-block;background:#d1fae5;color:#065f46;'
                    'font-size:11px;padding:2px 6px;border-radius:4px;margin-left:6px;">'
                    "Verified</span>"
                )
            elif item.get("verification_status") == "partially_verified":
                verified_badge = (
                    ' <span style="display:inline-block;background:#fef3c7;color:#92400e;'
                    'font-size:11px;padding:2px 6px;border-radius:4px;margin-left:6px;">'
                    "Partially Verified</span>"
                )

            key_points_html = ""
            if item.get("key_points"):
                points = "".join(
                    f'<li style="margin-bottom:4px;">{p}</li>'
                    for p in item["key_points"]
                )
                key_points_html = (
                    f'<ul style="margin:8px 0 0;padding-left:20px;color:#374151;">'
                    f"{points}</ul>"
                )

            summary_html = ""
            if item.get("summary"):
                summary_html = (
                    f'<p style="margin:8px 0 0;color:#4b5563;font-size:14px;'
                    f'line-height:1.5;">{item["summary"]}</p>'
                )

            topics = ", ".join(item.get("matched_topics", []))
            topics_html = ""
            if topics:
                topics_html = (
                    f'<span style="font-size:12px;color:#6b7280;">Topics: {topics}</span>'
                )

            items_html += f"""
            <div style="border:1px solid #e5e7eb;border-radius:8px;padding:16px;margin-bottom:12px;">
                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
                    <span style="font-weight:600;color:#1e40af;">{item.get('municipality', 'Unknown')}</span>
                    <span style="background:#eff6ff;color:#1e40af;padding:2px 8px;border-radius:4px;font-size:12px;">
                        {item.get('doc_type', 'document').upper()}
                    </span>
                </div>
                <h3 style="margin:0 0 4px;font-size:15px;">
                    <a href="{item.get('url', '#')}" style="color:#1e40af;text-decoration:none;">
                        {item.get('title', 'Untitled')}
                    </a>
                    {verified_badge}
                </h3>
                {topics_html}
                {summary_html}
                {key_points_html}
            </div>
            """

    return f"""
    <html>
    <body style="font-family:system-ui,-apple-system,sans-serif;max-width:600px;margin:0 auto;padding:20px;color:#1a1a1a;background:#f9fafb;">
        <div style="background:white;border-radius:12px;padding:24px;border:1px solid #e5e7eb;">
            <div style="border-bottom:3px solid #1e40af;padding-bottom:16px;margin-bottom:24px;">
                <h1 style="color:#1e40af;margin:0;font-size:24px;">BC Local Government Council Tracker</h1>
                <p style="color:#6b7280;margin:4px 0 0;font-size:14px;">Your Weekly Municipal Digest</p>
            </div>

            <h2 style="color:#111;font-size:18px;margin:0 0 16px;">
                Week of {date_str}
            </h2>

            <p style="color:#374151;font-size:14px;margin-bottom:20px;">
                Here are the latest municipal council updates matching your preferences:
            </p>

            {items_html}
        </div>

        <div style="margin-top:20px;padding:16px;text-align:center;">
            <p style="font-size:12px;color:#9ca3af;line-height:1.5;">
                This is an experimental personal tool using public data.
                AI summaries may contain errors. Always verify with original municipal sources.
                Not official government communication.
            </p>
            <p style="margin-top:12px;">
                <a href="{unsubscribe_url}" style="color:#9ca3af;font-size:12px;">
                    Unsubscribe from these emails
                </a>
            </p>
        </div>
    </body>
    </html>
    """


async def get_recent_documents(
    db: AsyncSession,
    municipality_names: list[str],
    since_days: int = 7,
) -> list[tuple[Document, Municipality]]:
    """Get documents from the past N days for given municipalities."""
    cutoff = datetime.now(timezone.utc) - timedelta(days=since_days)

    # Get municipality IDs by short_name
    result = await db.execute(
        select(Municipality).where(Municipality.short_name.in_(municipality_names))
    )
    munis = {m.id: m for m in result.scalars().all()}

    if not munis:
        return []

    result = await db.execute(
        select(Document)
        .where(
            Document.municipality_id.in_(munis.keys()),
            Document.first_seen_at >= cutoff,
        )
        .order_by(Document.first_seen_at.desc())
    )
    docs = result.scalars().all()

    return [(doc, munis[doc.municipality_id]) for doc in docs if doc.municipality_id in munis]


def build_digest_items(
    docs_with_munis: list[tuple[Document, Municipality]],
    subscriber_topics: list[str],
    subscriber_keywords: str,
) -> list[dict]:
    """Build digest items from documents, filtering by subscriber preferences.

    Uses keyword matching aligned to AVAILABLE_TOPICS from the track model.
    Each topic maps to the keywords likely to appear in matching documents.
    """
    items = []
    kw_list = [k.strip().lower() for k in (subscriber_keywords or "").split(",") if k.strip()]

    # Topic → keyword mapping.
    #
    # Keys MUST match the topic IDs sent by the frontend (page.tsx AVAILABLE_TOPICS).
    # A mismatch causes every subscriber topic to silently match zero documents.
    #
    # Keyword strategy: BC councils rarely name legislation in full. Agendas and
    # minutes use bylaw numbers, bill numbers, acronyms, and staff-report shorthand.
    # Each list captures the realistic surface forms a document will contain.
    #
    # Provincial legislation reference (BC):
    #   Bill 44 → Housing Statutes (Residential Development) Amendment Act — SSMUH
    #   Bill 47 → Housing Statutes (Transit-Oriented Areas) Amendment Act — TOA
    #   Bill 46 → Housing Statutes (Housing Needs Reports) Amendment Act
    #   Bill 35 → Short-Term Rental Accommodations Act
    topic_keywords: dict[str, list[str]] = {
        # Transit Oriented Development (broad)
        "tod": [
            "transit-oriented development", "transit oriented development",
            "tod", "transit hub", "transit node",
        ],
        # Transit Oriented Areas — BC Bill 47 station-area zones
        "toa_impl": [
            "transit-oriented area", "transit oriented area",
            "toa", "bill 47",
            "station area", "station precinct", "skytrain area",
            "frequent transit", "frequent transit network", "ftn",
            "400 metre", "400m", "800 metre", "800m",
            "bus exchange", "rapid transit station",
        ],
        # Local area / neighbourhood plans
        "area_plans": [
            "area plan", "neighbourhood plan", "local area plan",
            "community plan amendment", "area structure plan",
            "neighbourhood planning", "district plan",
        ],
        # Bus Rapid Transit / bus priority
        "brt": [
            "bus rapid transit", "brt", "bus priority",
            "rapid bus", "b-line", "bus lane", "queue jump",
            "bus exchange", "transit corridor",
        ],
        # Multimodal / active transportation
        "multimodal": [
            "multimodal", "active transportation", "cycling infrastructure",
            "bike lane", "cycle track", "cycling network",
            "pedestrian", "walkability", "greenway", "shared path",
            "complete streets", "sidewalk improvement",
        ],
        # Provincial housing targets / Housing Needs Reports (Bill 46)
        "provincial_targets": [
            "housing needs report", "housing needs assessment",
            "provincial housing target", "housing target",
            "hnr", "bill 46", "housing supply",
            "housing action plan", "housing strategy",
        ],
        # Small-Scale Multi-Unit Housing — BC Bill 44
        "ssmuh": [
            "small-scale multi-unit", "ssmuh",
            "bill 44",
            "duplex", "triplex", "fourplex", "multiplex", "sixplex",
            "missing middle", "gentle density",
            "secondary suite", "garden suite", "carriage house",
            "infill housing", "laneway home",
        ],
        # Housing Statutes Amendment Act / Related Bylaws
        # (covers the family of BC housing bills and their local bylaw responses)
        "housing_statutes": [
            "housing statutes", "housing statute",
            "bill 44", "bill 47", "bill 46", "bill 35",
            "short-term rental", "short term rental", "airbnb",
            "provincial housing legislation", "housing legislation",
            "housing amendment", "zoning bylaw amendment",
            "residential infill", "as-of-right", "as of right",
        ],
        # OCP updates (any official community plan work)
        "ocp_housing": [
            "official community plan", "ocp",
            "ocp amendment", "community plan amendment",
            "land use designation", "future land use",
            "ocp bylaw", "plan amendment",
        ],
        # Zoning / rezoning for housing density
        "zoning_density": [
            "rezoning", "rezone", "zoning bylaw amendment",
            "zoning amendment", "density bonus",
            "floor area ratio", "far", "floor space ratio", "fsr",
            "height increase", "density increase",
            "comprehensive development zone", "cd zone",
        ],
        # Development permits affecting housing supply
        "dev_permits_housing": [
            "development permit", "development variance permit", "dvp",
            "building permit", "construction permit",
            "development application", "form and character",
            "amenity contribution",
        ],
        # Development Cost Charges / affordability incentives
        "dev_cost_charges": [
            "development cost charge", "dcc", "development cost levy",
            "community amenity contribution", "cac",
            "amenity contribution", "density bonusing",
            "affordable housing reserve", "affordability incentive",
            "waiver of fees", "fee waiver",
        ],
        # Broad housing/transit bucket — catches anything not above
        "other_housing_transit": [
            "housing", "affordable housing", "rental housing",
            "market rental", "below-market", "below market",
            "transit", "bus route", "skytrain", "rapid transit",
            "transportation plan", "mobility",
        ],
    }

    for doc, muni in docs_with_munis:
        content = (doc.raw_text or doc.title or "").lower()
        title = (doc.title or "").lower()
        searchable = f"{content} {title}"

        matched_topics = []
        for topic in subscriber_topics:
            topic_kws = topic_keywords.get(topic, [])
            if topic_kws and any(kw in searchable for kw in topic_kws):
                matched_topics.append(topic)

        matched_keywords = [kw for kw in kw_list if kw in searchable]

        if matched_topics or matched_keywords:
            items.append({
                "municipality": muni.short_name,
                "doc_type": doc.doc_type.value if doc.doc_type else "document",
                "title": doc.title or "Untitled",
                "url": doc.url or "#",
                "summary": None,
                "key_points": None,
                "matched_topics": matched_topics,
                "matched_keywords": matched_keywords,
                "verification_status": "unverified",
            })

    return items


def send_digest_via_resend(
    to_email: str,
    html: str,
    date_str: str,
) -> bool:
    """Send digest email via Resend. Returns True on success."""
    if not settings.resend_api_key:
        logger.warning("RESEND_API_KEY not set — skipping digest email")
        return False

    try:
        import resend
        resend.api_key = settings.resend_api_key

        resend.Emails.send({
            "from": settings.resend_from_email,
            "to": [to_email],
            "subject": f"Your BC Local Government Council Tracker Digest \u2013 {date_str}",
            "html": html,
        })
        logger.info(f"Digest email sent to {to_email}")
        return True
    except Exception as e:
        logger.error(f"Failed to send digest to {to_email}: {e}")
        return False


async def run_weekly_digest(db: AsyncSession) -> dict:
    """Main weekly digest job: for each active subscriber, gather docs, match, and email.

    Returns stats dict.
    """
    stats = {
        "subscribers_processed": 0,
        "emails_sent": 0,
        "emails_failed": 0,
        "total_items": 0,
    }

    # Get all active subscribers
    result = await db.execute(
        select(Subscriber).where(Subscriber.active.is_(True))
    )
    subscribers = result.scalars().all()

    if not subscribers:
        logger.info("No active subscribers — skipping digest")
        return stats

    date_str = datetime.now(timezone.utc).strftime("%B %d, %Y")

    for subscriber in subscribers:
        stats["subscribers_processed"] += 1

        municipalities = subscriber.municipalities or []
        topics = subscriber.topics or []

        if not municipalities and not topics:
            continue

        # Get recent documents for subscriber's municipalities
        docs_with_munis = await get_recent_documents(db, municipalities)

        # Build matching digest items
        items = build_digest_items(docs_with_munis, topics, subscriber.keywords)
        stats["total_items"] += len(items)

        # Build token-based unsubscribe URL
        unsubscribe_url = (
            f"{settings.app_base_url}/api/v1/unsubscribe"
            f"?token={quote(subscriber.unsubscribe_token)}"
        )

        # Render email
        html = render_digest_email(
            subscriber_email=subscriber.email,
            items=items,
            date_str=date_str,
            unsubscribe_url=unsubscribe_url,
        )

        # Send
        success = send_digest_via_resend(subscriber.email, html, date_str)
        if success:
            stats["emails_sent"] += 1
        else:
            stats["emails_failed"] += 1

    logger.info(
        f"Weekly digest complete: {stats['subscribers_processed']} subscribers, "
        f"{stats['emails_sent']} sent, {stats['emails_failed']} failed, "
        f"{stats['total_items']} total items"
    )
    return stats
