import json
import logging
import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.db.database import engine, Base
import app.models  # noqa: F401 — ensure all models registered before create_all


class _JSONFormatter(logging.Formatter):
    """Emit each log record as a single JSON line."""

    def format(self, record: logging.LogRecord) -> str:
        entry = {
            "ts": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "logger": record.name,
            "msg": record.getMessage(),
        }
        if record.exc_info and record.exc_info[0]:
            entry["exc"] = self.formatException(record.exc_info)
        return json.dumps(entry, default=str)


def _configure_logging() -> None:
    """Set up root logging based on LOG_FORMAT config."""
    root = logging.getLogger()
    root.setLevel(logging.DEBUG if settings.debug else logging.INFO)
    handler = logging.StreamHandler(sys.stderr)
    if settings.log_format == "json":
        handler.setFormatter(_JSONFormatter())
    else:
        handler.setFormatter(logging.Formatter(
            "%(asctime)s %(levelname)-5s [%(name)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        ))
    root.handlers = [handler]


_configure_logging()
logger = logging.getLogger(__name__)
from app.api.registry import router as registry_router
from app.api.health import router as health_router
from app.api.discovery import router as discovery_router
from app.api.tracks import router as tracks_router
from app.api.processing import router as processing_router
from app.api.alerts import router as alerts_router
from app.api.search import router as search_router
from app.api.subscribe import router as subscribe_router
from app.api.cron import router as cron_router
from app.api.costs import router as costs_router
from app.api.auth import router as auth_router


def _validate_config() -> None:
    """Log critical warnings (or raise) for missing production config."""
    if not settings.app_base_url:
        msg = (
            "APP_BASE_URL is not set. All email features (immediate alerts, "
            "weekly digests, confirmation emails) are DISABLED. "
            "Set APP_BASE_URL to your public domain (e.g. https://lg-tracker.ca) "
            "to enable email delivery."
        )
        if settings.debug:
            logger.warning(msg)
        else:
            raise RuntimeError(msg)

    if not settings.cron_secret and not settings.debug:
        raise RuntimeError(
            "CRON_SECRET is not set in production. All cron/admin endpoints "
            "will return 503. Set CRON_SECRET to a random string."
        )

    if not settings.smtp_username or not settings.smtp_password:
        logger.warning(
            "SMTP credentials not set. Email sending will fail at runtime."
        )


@asynccontextmanager
async def lifespan(app: FastAPI):
    _validate_config()

    if settings.debug:
        # Auto-create tables in dev mode only.  Production must use explicit
        # migrations (Alembic) so that schema changes are versioned and
        # reversible.  Running create_all in production silently papers over
        # migration drift — a schema may appear to work locally but diverge
        # from the migrated production schema.
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="Track BC local government council hearing updates",
    lifespan=lifespan,
)

# Parse comma-separated allowed origins from config.
# Starlette's CORSMiddleware does NOT support wildcard patterns (e.g. "https://*.vercel.app")
# when allow_credentials=True — the origin list must contain exact strings only.
# Set ALLOWED_ORIGINS env var to a comma-separated list of your production domains.
allowed_origins = [o.strip() for o in settings.allowed_origins.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router, tags=["health"])
app.include_router(registry_router, prefix="/api/v1", tags=["registry"])
app.include_router(discovery_router, prefix="/api/v1/discovery", tags=["discovery"])
app.include_router(tracks_router, prefix="/api/v1", tags=["tracks"])
app.include_router(processing_router, prefix="/api/v1/ai", tags=["processing"])
app.include_router(alerts_router, prefix="/api/v1/alerts", tags=["alerts"])
app.include_router(search_router, prefix="/api/v1", tags=["search"])
app.include_router(subscribe_router, prefix="/api/v1", tags=["subscribe"])
app.include_router(cron_router, prefix="/api/v1/cron", tags=["cron"])
app.include_router(costs_router, prefix="/api/v1", tags=["costs"])
app.include_router(auth_router, prefix="/api/v1", tags=["auth"])
