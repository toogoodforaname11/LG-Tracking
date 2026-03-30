"""Shared email service — sends emails via SMTP (Hostinger)."""

import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.config import settings

logger = logging.getLogger(__name__)


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
