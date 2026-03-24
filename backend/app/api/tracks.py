"""User opt-in tracks API — CRUD for tracking preferences."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel

from app.db.database import get_db
from app.models.track import Track, TrackMatch, AVAILABLE_TOPICS
from app.models.municipality import Municipality

router = APIRouter()

# Demo user ID (Phase 5 will add real auth)
DEMO_USER_ID = "demo-gov001"


# --- Schemas ---


class TrackCreate(BaseModel):
    name: str
    municipality_ids: list[int]
    topics: list[str] = []
    keywords: list[str] = []
    notify_email: bool = True


class TrackUpdate(BaseModel):
    name: str | None = None
    municipality_ids: list[int] | None = None
    topics: list[str] | None = None
    keywords: list[str] | None = None
    is_active: bool | None = None
    notify_email: bool | None = None


class TrackOut(BaseModel):
    id: int
    user_id: str
    name: str
    municipality_ids: list[int]
    topics: list[str]
    keywords: list[str]
    is_active: bool
    notify_email: bool
    created_at: str
    updated_at: str

    model_config = {"from_attributes": True}


class TrackMatchOut(BaseModel):
    id: int
    track_id: int
    document_id: int
    match_score: float | None
    match_reason: str | None
    matched_topics: list[str] | None
    matched_keywords: list[str] | None
    summary: str | None
    verification_status: str | None
    notified_at: str | None

    model_config = {"from_attributes": True}


# --- Endpoints ---


@router.get("/topics")
async def list_available_topics():
    """List all available topics users can opt into."""
    return {"topics": AVAILABLE_TOPICS}


@router.post("/tracks", response_model=TrackOut, status_code=201)
async def create_track(track: TrackCreate, db: AsyncSession = Depends(get_db)):
    """Create a new tracking preference."""
    # Validate topics
    invalid_topics = [t for t in track.topics if t not in AVAILABLE_TOPICS]
    if invalid_topics:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid topics: {invalid_topics}. Available: {AVAILABLE_TOPICS}",
        )

    # Validate municipality IDs exist
    for muni_id in track.municipality_ids:
        result = await db.execute(select(Municipality).where(Municipality.id == muni_id))
        if not result.scalar_one_or_none():
            raise HTTPException(status_code=400, detail=f"Municipality ID {muni_id} not found")

    new_track = Track(
        user_id=DEMO_USER_ID,
        name=track.name,
        municipality_ids=track.municipality_ids,
        topics=track.topics,
        keywords=track.keywords,
        notify_email=track.notify_email,
    )
    db.add(new_track)
    await db.commit()
    await db.refresh(new_track)
    return new_track


@router.get("/tracks", response_model=list[TrackOut])
async def list_tracks(active_only: bool = False, db: AsyncSession = Depends(get_db)):
    """List all tracks for the demo user."""
    query = select(Track).where(Track.user_id == DEMO_USER_ID)
    if active_only:
        query = query.where(Track.is_active.is_(True))
    query = query.order_by(Track.created_at.desc())

    result = await db.execute(query)
    return result.scalars().all()


@router.get("/tracks/{track_id}", response_model=TrackOut)
async def get_track(track_id: int, db: AsyncSession = Depends(get_db)):
    """Get a specific track."""
    result = await db.execute(
        select(Track).where(Track.id == track_id, Track.user_id == DEMO_USER_ID)
    )
    track = result.scalar_one_or_none()
    if not track:
        raise HTTPException(status_code=404, detail="Track not found")
    return track


@router.patch("/tracks/{track_id}", response_model=TrackOut)
async def update_track(
    track_id: int, update: TrackUpdate, db: AsyncSession = Depends(get_db)
):
    """Update an existing track."""
    result = await db.execute(
        select(Track).where(Track.id == track_id, Track.user_id == DEMO_USER_ID)
    )
    track = result.scalar_one_or_none()
    if not track:
        raise HTTPException(status_code=404, detail="Track not found")

    if update.topics is not None:
        invalid = [t for t in update.topics if t not in AVAILABLE_TOPICS]
        if invalid:
            raise HTTPException(status_code=400, detail=f"Invalid topics: {invalid}")

    update_data = update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(track, key, value)

    await db.commit()
    await db.refresh(track)
    return track


@router.delete("/tracks/{track_id}")
async def delete_track(track_id: int, db: AsyncSession = Depends(get_db)):
    """Delete a track (soft-delete by deactivating)."""
    result = await db.execute(
        select(Track).where(Track.id == track_id, Track.user_id == DEMO_USER_ID)
    )
    track = result.scalar_one_or_none()
    if not track:
        raise HTTPException(status_code=404, detail="Track not found")

    track.is_active = False
    await db.commit()
    return {"status": "deactivated", "track_id": track_id}


@router.get("/tracks/{track_id}/matches", response_model=list[TrackMatchOut])
async def list_track_matches(
    track_id: int, limit: int = 20, db: AsyncSession = Depends(get_db)
):
    """List matches for a specific track."""
    result = await db.execute(
        select(TrackMatch)
        .where(TrackMatch.track_id == track_id)
        .order_by(TrackMatch.created_at.desc())
        .limit(limit)
    )
    return result.scalars().all()
