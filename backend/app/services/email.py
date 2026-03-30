"""Shared email service — sends emails via SMTP (Hostinger)."""

import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.config import settings

logger = logging.getLogger(__name__)


def render_timestamp_links_html(timestamps: list[dict] | None) -> str:
    """Render video timestamp deep links as an HTML block.

    Each timestamp dict must have: t (display time), label, url (deep link).
    Returns empty string if no timestamps.
    """
    if not timestamps:
        return ""

    links = []
    for ts in timestamps:
        t = ts.get("t", "")
        label = ts.get("label", "")
        url = ts.get("url", "")
        if url and label:
            links.append(
                f'<a href="{url}" style="color:#1e40af;text-decoration:none;">'
                f'{t}</a> — {label}'
            )

    if not links:
        return ""

    items_html = "".join(f'<li style="margin-bottom:4px;font-size:13px;">{l}</li>' for l in links)
    return (
        '<div style="margin:10px 0 0;padding:10px 14px;background:#f0f4ff;border-radius:6px;">'
        '<p style="margin:0 0 6px;font-size:12px;font-weight:600;color:#1e40af;">'
        'Video Timestamps</p>'
        f'<ul style="margin:0;padding-left:18px;color:#374151;">{items_html}</ul>'
        '</div>'
    )


def render_timestamp_links_text(timestamps: list[dict] | None) -> str:
    """Render video timestamp deep links as plain text."""
    if not timestamps:
        return ""

    lines = ["  Video Timestamps:"]
    for ts in timestamps:
        t = ts.get("t", "")
        label = ts.get("label", "")
        url = ts.get("url", "")
        if url and label:
            lines.append(f"    [{t}] {label} — {url}")

    return "\n".join(lines) if len(lines) > 1 else ""


def send_email(
    to_email: str,
    subject: str,
    html: str,
    text: str | None = None,
) -> bool:
    """Send an email via Hostinger SMTP. Returns True on success."""
    if not settings.smtp_host or not settings.smtp_username or not settings.smtp_password:
        logger.warning("SMTP not configured — skipping email to %s", to_email)
        return False

    msg = MIMEMultipart("alternative")
    msg["From"] = settings.smtp_from_email
    msg["To"] = to_email
    msg["Subject"] = subject

    if text:
        msg.attach(MIMEText(text, "plain"))
    msg.attach(MIMEText(html, "html"))

    try:
        with smtplib.SMTP_SSL(settings.smtp_host, settings.smtp_port) as server:
            server.login(settings.smtp_username, settings.smtp_password)
            server.sendmail(settings.smtp_from_email, [to_email], msg.as_string())
        logger.info("Email sent to %s: %s", to_email, subject)
        return True
    except Exception as e:
        logger.error("Failed to send email to %s: %s", to_email, e)
        return False
