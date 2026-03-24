from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from pydantic import BaseModel

from app.db.database import get_db
from app.models.municipality import Municipality, Source, ScrapeStatus
from app.services.seed_registry import seed_registry

router = APIRouter()


# --- Pydantic schemas ---


class SourceOut(BaseModel):
    id: int
    platform: str
    source_type: str
    url: str
    label: str
    scrape_status: str
    last_scraped_at: str | None = None

    model_config = {"from_attributes": True}


class MunicipalityOut(BaseModel):
    id: int
    name: str
    short_name: str
    gov_type: str
    region: str
    website_url: str | None = None
    population: int | None = None
    is_active: bool
    sources: list[SourceOut] = []

    model_config = {"from_attributes": True}


class MunicipalityListOut(BaseModel):
    municipalities: list[MunicipalityOut]
    total: int


class SourceCreate(BaseModel):
    municipality_id: int
    platform: str
    source_type: str
    url: str
    label: str


class SeedResult(BaseModel):
    municipalities_created: int
    municipalities_existed: int
    sources_created: int


# --- Endpoints ---


@router.get("/municipalities", response_model=MunicipalityListOut)
async def list_municipalities(
    region: str | None = None,
    active_only: bool = True,
    db: AsyncSession = Depends(get_db),
):
    """List all municipalities, optionally filtered by region."""
    query = select(Municipality).options(selectinload(Municipality.sources))
    if region:
        query = query.where(Municipality.region == region)
    if active_only:
        query = query.where(Municipality.is_active.is_(True))
    query = query.order_by(Municipality.name)

    result = await db.execute(query)
    munis = result.scalars().all()
    return MunicipalityListOut(municipalities=munis, total=len(munis))


@router.get("/municipalities/{muni_id}", response_model=MunicipalityOut)
async def get_municipality(muni_id: int, db: AsyncSession = Depends(get_db)):
    """Get a single municipality with its sources."""
    result = await db.execute(
        select(Municipality)
        .options(selectinload(Municipality.sources))
        .where(Municipality.id == muni_id)
    )
    muni = result.scalar_one_or_none()
    if not muni:
        raise HTTPException(status_code=404, detail="Municipality not found")
    return muni


@router.get("/sources", response_model=list[SourceOut])
async def list_sources(
    platform: str | None = None,
    status: str | None = None,
    db: AsyncSession = Depends(get_db),
):
    """List all sources, optionally filtered by platform or status."""
    query = select(Source)
    if platform:
        query = query.where(Source.platform == platform)
    if status:
        query = query.where(Source.scrape_status == status)
    query = query.order_by(Source.id)

    result = await db.execute(query)
    return result.scalars().all()


@router.post("/sources", response_model=SourceOut, status_code=201)
async def create_source(source: SourceCreate, db: AsyncSession = Depends(get_db)):
    """Add a new source to a municipality."""
    # Verify municipality exists
    result = await db.execute(
        select(Municipality).where(Municipality.id == source.municipality_id)
    )
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Municipality not found")

    new_source = Source(
        municipality_id=source.municipality_id,
        platform=source.platform,
        source_type=source.source_type,
        url=source.url,
        label=source.label,
        scrape_status=ScrapeStatus.PENDING,
    )
    db.add(new_source)
    await db.commit()
    await db.refresh(new_source)
    return new_source


@router.patch("/sources/{source_id}/status")
async def update_source_status(
    source_id: int,
    status: str,
    db: AsyncSession = Depends(get_db),
):
    """Update the scrape status of a source."""
    result = await db.execute(select(Source).where(Source.id == source_id))
    source = result.scalar_one_or_none()
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")
    source.scrape_status = status
    await db.commit()
    return {"id": source_id, "scrape_status": status}


@router.post("/seed", response_model=SeedResult)
async def seed_data(db: AsyncSession = Depends(get_db)):
    """Seed the registry with CRD municipalities and their known sources."""
    stats = await seed_registry(db)
    return stats
