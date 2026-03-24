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


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables on startup (dev mode — use Alembic migrations in prod)
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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://*.vercel.app"],
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
