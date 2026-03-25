from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.db.database import engine, Base
import app.models  # noqa: F401 — ensure all models registered before create_all
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


@asynccontextmanager
async def lifespan(app: FastAPI):
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
