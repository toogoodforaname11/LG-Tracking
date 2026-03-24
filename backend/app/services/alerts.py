"""Alert system — generate and deliver digests for matched tracks."""

import logging
import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.track import Track, TrackMatch
from app.models.document import Document
from app.models.municipality import Municipality
from app.ai.perplexity import verify_with_perplexity
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
            verification = await verify_with_perplexity(
                municipality=muni.short_name if muni else "Unknown",
                meeting_date="Unknown",
                document_type=doc.doc_type.value if doc.doc_type else "unknown",
                key_points=match.key_points,
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
        "generated_at": datetime.utcnow().isoformat(),
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
    """Send a digest email. Returns True on success."""
    # For now, just log the digest (email sending requires SMTP config)
    logger.info(f"Would send digest to {recipient}: {digest['track_name']} ({digest['total_matches']} items)")

    # Actual SMTP sending (enable when SMTP is configured)
    # try:
    #     msg = MIMEMultipart("alternative")
    #     msg["Subject"] = f"[BC Local Government Council Tracker] {digest['track_name']} — {digest['total_matches']} new matches"
    #     msg["From"] = "noreply@bchearingwatch.local"
    #     msg["To"] = recipient
    #     msg.attach(MIMEText(render_digest_text(digest), "plain"))
    #     msg.attach(MIMEText(render_digest_html(digest), "html"))
    #     with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as server:
    #         server.starttls()
    #         server.login(settings.smtp_user, settings.smtp_password)
    #         server.sendmail(msg["From"], [recipient], msg.as_string())
    #     return True
    # except Exception as e:
    #     logger.error(f"Email send failed: {e}")
    #     return False

    return True  # Stub success for now


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

        # Render and "send"
        if track.notify_email:
            success = await send_digest_email(digest, f"{track.user_id}@example.com")
            if success:
                stats["digests_sent"] += 1

        # Mark matches as notified
        result = await db.execute(
            select(TrackMatch).where(
                TrackMatch.track_id == track.id,
                TrackMatch.notification_status == "pending",
            )
        )
        pending_matches = result.scalars().all()
        for match in pending_matches:
            match.notification_status = "sent"
            match.notified_at = datetime.utcnow()
            stats["matches_notified"] += 1

        await db.commit()

    return stats
