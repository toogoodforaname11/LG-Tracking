"""Shared FastAPI dependencies."""

from fastapi import Header, HTTPException

from app.config import settings


async def verify_cron_secret(
    x_cron_secret: str | None = Header(None, alias="X-Cron-Secret"),
) -> None:
    """Enforce cron/admin endpoint authentication.

    When CRON_SECRET is set in the environment, every request to a protected
    endpoint MUST include the header:

        X-Cron-Secret: <value>

    A warning-only approach is not acceptable here: an unprotected cron endpoint
    allows any external caller to trigger full scraping runs (real cost), send
    emails to all subscribers (abuse), or reset the database seed.  The check
    must be deterministic — if the secret is configured and the header is wrong
    or missing, the request is rejected with 401, unconditionally.

    When CRON_SECRET is blank and debug mode is off, the server is
    misconfigured for production — reject with 503 rather than silently
    allowing unauthenticated access.
    """
    if not settings.cron_secret:
        if settings.debug:
            # Local development — allow unauthenticated access.
            return
        raise HTTPException(
            status_code=503,
            detail="Server misconfiguration: CRON_SECRET is not set. "
            "All protected endpoints are unavailable until it is configured.",
        )
    if x_cron_secret != settings.cron_secret:
        raise HTTPException(status_code=401, detail="Unauthorized: invalid or missing X-Cron-Secret")
