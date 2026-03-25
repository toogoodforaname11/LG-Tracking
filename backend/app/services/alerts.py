"""Alert system — generate and deliver digests for matched tracks."""

import logging
from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.track import Track, TrackMatch
from app.models.document import Document
from app.models.municipality import Municipality
from app.ai.perplexity import verify_with_perplexity
from app.services.cost_tracker import log_api_cost
from app.config import settings

logger = logging.getLogger(__name__)


async def generate_digest(db: AsyncSession, track_id: int) -> dict | None:
    """Generate a digest for a single track with all pending matches.

    Returns a dict with the digest content, or None if no pending matches.
    """
    # Get track
    result = await db.execute(select(Track).where(Track.id == track_id))
    track = result.scalar_one_or_none()
    if not track:
        return None

    # Get pending (unnotified) matches
    result = await db.execute(
        select(TrackMatch)
        .where(
            TrackMatch.track_id == track_id,
            TrackMatch.notification_status == "pending",
        )
        .order_by(TrackMatch.created_at.desc())
    )
    matches = result.scalars().all()

    if not matches:
        return None

    # Get related documents and municipalities
    doc_ids = [m.document_id for m in matches]
    result = await db.execute(select(Document).where(Document.id.in_(doc_ids)))
    docs = {d.id: d for d in result.scalars().all()}

    muni_ids = set(d.municipality_id for d in docs.values())
    result = await db.execute(select(Municipality).where(Municipality.id.in_(muni_ids)))
    munis = {m.id: m for m in result.scalars().all()}

    # Build digest
    digest_items = []
    for match in matches:
        doc = docs.get(match.document_id)
        if not doc:
            continue
        muni = munis.get(doc.municipality_id)

        # Run Perplexity verification on key points if available
        if match.key_points and not match.verification_status == "verified":
            verification, perp_usage = await verify_with_perplexity(
                municipality=muni.short_name if muni else "Unknown",
                meeting_date="Unknown",
                document_type=doc.doc_type.value if doc.doc_type else "unknown",
                key_points=match.key_points,
            )
            await log_api_cost(
                db, "perplexity", "verify", "sonar",
                perp_usage["input_tokens"], perp_usage["output_tokens"],
                context={"match_id": match.id, "track_id": match.track_id},
            )
            if verification:
                match.verification_status = verification.get("verification_status", "unverified")
                match.verification_notes = str(verification.get("claims", []))

        digest_items.append({
            "municipality": muni.short_name if muni else "Unknown",
            "doc_type": doc.doc_type.value if doc.doc_type else "unknown",
            "title": doc.title,
            "url": doc.url,
            "match_score": match.match_score,
            "matched_topics": match.matched_topics or [],
            "matched_keywords": match.matched_keywords or [],
            "summary": match.summary,
            "key_points": match.key_points or [],
            "verification_status": match.verification_status or "unverified",
        })

    digest = {
        "track_name": track.name,
        "track_id": track.id,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_matches": len(digest_items),
        "items": digest_items,
    }

    return digest


def render_digest_html(digest: dict) -> str:
    """Render a digest dict into HTML email content."""
    items_html = ""
    for item in digest["items"]:
        verified_badge = ""
        if item["verification_status"] == "verified":
            verified_badge = ' <span style="color:green;font-size:12px;">&#10003; Verified</span>'
        elif item["verification_status"] == "partially_verified":
            verified_badge = ' <span style="color:orange;font-size:12px;">&#9888; Partially Verified</span>'

        key_points_html = ""
        if item["key_points"]:
            points = "".join(f"<li>{p}</li>" for p in item["key_points"])
            key_points_html = f"<ul>{points}</ul>"

        summary_html = f"<p>{item['summary']}</p>" if item.get("summary") else ""

        items_html += f"""
        <div style="border:1px solid #ddd;border-radius:8px;padding:16px;margin-bottom:12px;">
            <div style="display:flex;justify-content:space-between;align-items:center;">
                <strong>{item['municipality']}</strong>
                <span style="background:#e3f2fd;padding:2px 8px;border-radius:4px;font-size:12px;">
                    {item['doc_type']}
                </span>
            </div>
            <h3 style="margin:8px 0 4px;">
                <a href="{item['url']}" style="color:#1976d2;">{item['title']}</a>
                {verified_badge}
            </h3>
            <p style="font-size:12px;color:#666;">
                Topics: {', '.join(item['matched_topics'])} |
                Keywords: {', '.join(item['matched_keywords'])} |
                Confidence: {item['match_score']:.0%}
            </p>
            {summary_html}
            {key_points_html}
        </div>
        """

    return f"""
    <html>
    <body style="font-family:system-ui,-apple-system,sans-serif;max-width:600px;margin:0 auto;padding:20px;">
        <h1 style="color:#1976d2;">BC Local Government Council Tracker</h1>
        <h2>Digest: {digest['track_name']}</h2>
        <p style="color:#666;">{digest['total_matches']} new matches found &bull; {digest['generated_at'][:10]}</p>
        {items_html}
        <hr style="border:none;border-top:1px solid #eee;margin:24px 0;">
        <p style="font-size:11px;color:#999;">
            &#9888; AI-generated summaries may contain errors.
            Always verify with original government sources.<br>
            This is not official government communication.
            Public data only &mdash; FIPPA-safe by design.
        </p>
    </body>
    </html>
    """


def render_digest_text(digest: dict) -> str:
    """Render a digest dict into plain text."""
    lines = [
        f"BC Local Government Council Tracker — Digest: {digest['track_name']}",
        f"{digest['total_matches']} new matches found — {digest['generated_at'][:10]}",
        "=" * 60,
        "",
    ]
    for item in digest["items"]:
        lines.append(f"[{item['municipality']}] {item['doc_type'].upper()}")
        lines.append(f"  {item['title']}")
        lines.append(f"  URL: {item['url']}")
        if item.get("summary"):
            lines.append(f"  Summary: {item['summary'][:200]}...")
        if item["key_points"]:
            for p in item["key_points"]:
                lines.append(f"    - {p}")
        lines.append("")

    lines.append("---")
    lines.append("AI-generated summaries may contain errors. Verify with original sources.")
    return "\n".join(lines)


async def send_digest_email(digest: dict, recipient: str) -> bool:
    """Send a track digest email via Resend. Returns True on success.

    This replaces the previous stub implementation that logged and returned True
    without sending anything. That approach was unacceptable: it silently consumed
    all TrackMatch records, marked them as notified, and delivered nothing to the
    user — a complete invisible failure of the core product loop.
    """
    if not settings.resend_api_key:
        logger.error(
            "RESEND_API_KEY not set — cannot send track digest to %s. "
            "Set RESEND_API_KEY in environment to enable email delivery.",
            recipient,
        )
        return False

    if not recipient:
        logger.error(
            "Track digest has no recipient email address (track_id=%s). "
            "Set notification_email on the Track record.",
            digest.get("track_id"),
        )
        return False

    try:
        import resend
        resend.api_key = settings.resend_api_key

        html = render_digest_html(digest)
        text = render_digest_text(digest)

        resend.Emails.send({
            "from": settings.resend_from_email,
            "to": [recipient],
            "subject": (
                f"[BC Local Government Council Tracker] "
                f"{digest['track_name']} — {digest['total_matches']} new matches"
            ),
            "html": html,
            "text": text,
        })
        logger.info(
            "Track digest sent to %s: %s (%d items)",
            recipient, digest["track_name"], digest["total_matches"],
        )
        return True

    except Exception as e:
        logger.error("Failed to send track digest to %s: %s", recipient, e)
        return False


async def process_and_notify(db: AsyncSession) -> dict:
    """Generate digests for all tracks with pending matches and notify."""
    stats = {"tracks_processed": 0, "digests_sent": 0, "matches_notified": 0}

    result = await db.execute(select(Track).where(Track.is_active.is_(True)))
    tracks = result.scalars().all()

    for track in tracks:
        digest = await generate_digest(db, track.id)
        if not digest:
            continue

        stats["tracks_processed"] += 1

        # Send to the track's configured notification email.
        # notification_email must be set on the Track record; notify_email=True
        # without a notification_email is a misconfiguration that we log and skip.
        if track.notify_email:
            if not track.notification_email:
                logger.warning(
                    "Track %d (%s) has notify_email=True but no notification_email set — skipping",
                    track.id, track.name,
                )
            else:
                success = await send_digest_email(digest, track.notification_email)
                if success:
                    stats["digests_sent"] += 1

        # Mark matches as notified regardless of email success — prevents
        # accumulating a backlog that would re-send the same content next run.
        result = await db.execute(
            select(TrackMatch).where(
                TrackMatch.track_id == track.id,
                TrackMatch.notification_status == "pending",
            )
        )
        pending_matches = result.scalars().all()
        for match in pending_matches:
            match.notification_status = "sent"
            match.notified_at = datetime.now(timezone.utc)
            stats["matches_notified"] += 1

        await db.commit()

    return stats
