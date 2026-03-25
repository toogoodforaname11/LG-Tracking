"""User opt-in tracks — the core of the personalization system.

A Track represents a user's interest in specific topics/keywords
for specific municipalities. Only matched items get full AI processing.
"""

import enum
from datetime import datetime, timezone

from sqlalchemy import String, Text, DateTime, Integer, Boolean, ForeignKey, Index, JSON, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


# Predefined topics users can opt into
AVAILABLE_TOPICS = [
    "ocp_updates",        # Official Community Plan amendments
    "rezoning",           # Zoning changes and applications
    "development_permits", # Development permit applications
    "public_hearings",    # All public hearings
    "bylaws",             # New/amended bylaws
    "budget",             # Budget discussions and approvals
    "environment",        # Environmental assessments, climate action
    "transportation",     # Roads, transit, cycling infrastructure
    "housing",            # Affordable housing, housing strategy
    "parks_recreation",   # Parks, trails, community facilities
    "utilities",          # Water, sewer, stormwater
    "governance",         # Council procedures, elections, boundaries
]


class Track(Base):
    __tablename__ = "tracks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(String(100), nullable=False)  # demo-gov001 for now
    name: Mapped[str] = mapped_column(String(200), nullable=False)  # User-chosen label

    # Email address for digest notifications. Required when notify_email=True.
    notification_email: Mapped[str | None] = mapped_column(String(320))

    # What to track
    municipality_ids: Mapped[list] = mapped_column(JSON, nullable=False)  # [1, 3, 5]
    topics: Mapped[list] = mapped_column(JSON, nullable=False, default=[])  # ["rezoning", "ocp_updates"]
    keywords: Mapped[list] = mapped_column(JSON, nullable=False, default=[])  # ["OCP", "affordable housing"]

    # Status
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    notify_email: Mapped[bool] = mapped_column(Boolean, default=True)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    __table_args__ = (Index("ix_tracks_user", "user_id"),)


class TrackMatch(Base):
    """Records when a discovered document matches a user's track."""

    __tablename__ = "track_matches"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    track_id: Mapped[int] = mapped_column(Integer, ForeignKey("tracks.id"), nullable=False)
    document_id: Mapped[int] = mapped_column(Integer, ForeignKey("documents.id"), nullable=False)

    # Match details
    match_score: Mapped[float | None] = mapped_column()  # 0.0 - 1.0 confidence
    match_reason: Mapped[str | None] = mapped_column(Text)  # Why it matched
    matched_topics: Mapped[list | None] = mapped_column(JSON)  # Which topics triggered
    matched_keywords: Mapped[list | None] = mapped_column(JSON)  # Which keywords triggered

    # AI processing results
    summary: Mapped[str | None] = mapped_column(Text)  # Gemini-generated summary
    key_points: Mapped[list | None] = mapped_column(JSON)  # Extracted key points
    verification_status: Mapped[str | None] = mapped_column(String(20))  # verified, unverified
    verification_notes: Mapped[str | None] = mapped_column(Text)  # Perplexity notes

    # Notification
    notified_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    notification_status: Mapped[str | None] = mapped_column(String(20))  # sent, failed, pending

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )

    __table_args__ = (
        Index("ix_track_matches_track", "track_id"),
        Index("ix_track_matches_document", "document_id"),
        UniqueConstraint("track_id", "document_id", name="uq_track_matches_track_document"),
    )
