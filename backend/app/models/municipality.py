import enum
from datetime import datetime, timezone

from sqlalchemy import (
    String, Text, Enum, DateTime, Integer, Boolean, ForeignKey, Index, UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


# Province constants — referenced from API, seed registry, and migrations.
# Stored as plain strings in Postgres (no enum type) so adding more provinces
# in the future doesn't require an enum-type ALTER. Keep these as the only
# source of truth for valid province values.
PROVINCE_BC = "BC"
PROVINCE_AB = "Alberta"
PROVINCE_ON = "Ontario"
VALID_PROVINCES: frozenset[str] = frozenset({PROVINCE_BC, PROVINCE_AB, PROVINCE_ON})


# Tier constants — Ontario distinguishes upper-tier (counties/regions),
# lower-tier (cities/towns/townships within an upper-tier) and single-tier
# (stand-alone municipalities). BC and AB rows default to "single" via the
# server_default on the column.
TIER_UPPER = "upper"
TIER_LOWER = "lower"
TIER_SINGLE = "single"
VALID_TIERS: frozenset[str] = frozenset({TIER_UPPER, TIER_LOWER, TIER_SINGLE})


class GovType(str, enum.Enum):
    CITY = "city"
    DISTRICT = "district"
    TOWN = "town"
    VILLAGE = "village"
    REGIONAL_DISTRICT = "regional_district"
    ISLAND_MUNICIPALITY = "island_municipality"
    MOUNTAIN_RESORT = "mountain_resort"
    REGIONAL_MUNICIPALITY = "regional_municipality"
    UNINCORPORATED = "unincorporated"


class Platform(str, enum.Enum):
    CIVICWEB = "civicweb"
    GRANICUS = "granicus"
    CIVICPLUS = "civicplus"
    ESCRIBE = "escribe"
    YOUTUBE = "youtube"
    CUSTOM = "custom"
    UNKNOWN = "unknown"


class SourceType(str, enum.Enum):
    AGENDA = "agenda"
    MINUTES = "minutes"
    VIDEO = "video"
    NOTICE = "notice"
    BYLAW = "bylaw"


class ScrapeStatus(str, enum.Enum):
    ACTIVE = "active"
    PENDING = "pending"
    BROKEN = "broken"
    DISABLED = "disabled"


class Municipality(Base):
    __tablename__ = "municipalities"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    # short_name is unique within a province (see UniqueConstraint below) so that
    # BC and Alberta can independently use names like "Lacombe" without collision.
    short_name: Mapped[str] = mapped_column(String(100), nullable=False)
    gov_type: Mapped[GovType] = mapped_column(Enum(GovType), nullable=False)
    # region is a *sub*-province grouping ("CRD", "BC", "Alberta", ...).
    # province is the authoritative top-level grouping for filtering on the
    # subscription form. Both are kept for backward compatibility.
    region: Mapped[str] = mapped_column(String(100), nullable=False, default="CRD")
    province: Mapped[str] = mapped_column(
        String(40),
        nullable=False,
        default=PROVINCE_BC,
        server_default=PROVINCE_BC,
        index=True,
    )
    # Tier captures Ontario's upper/lower/single municipal hierarchy. BC
    # and AB rows default to "single" via the server_default below.
    tier: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default=TIER_SINGLE,
        server_default=TIER_SINGLE,
        index=True,
    )
    website_url: Mapped[str | None] = mapped_column(Text)
    population: Mapped[int | None] = mapped_column(Integer)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    sources: Mapped[list["Source"]] = relationship(back_populates="municipality", cascade="all")

    __table_args__ = (
        UniqueConstraint("short_name", "province", name="uq_muni_short_province"),
    )

    def __repr__(self) -> str:
        return f"<Municipality {self.short_name} ({self.province})>"


class Source(Base):
    __tablename__ = "sources"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    municipality_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("municipalities.id"), nullable=False
    )
    platform: Mapped[Platform] = mapped_column(Enum(Platform), nullable=False)
    source_type: Mapped[SourceType] = mapped_column(Enum(SourceType), nullable=False)
    url: Mapped[str] = mapped_column(Text, nullable=False)
    label: Mapped[str] = mapped_column(String(200), nullable=False)
    scrape_status: Mapped[ScrapeStatus] = mapped_column(
        Enum(ScrapeStatus), default=ScrapeStatus.PENDING
    )
    scrape_config: Mapped[str | None] = mapped_column(Text)  # JSON config for scraper
    last_scraped_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    last_error: Mapped[str | None] = mapped_column(Text)
    consecutive_failures: Mapped[int] = mapped_column(Integer, default=0, server_default="0")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    municipality: Mapped["Municipality"] = relationship(back_populates="sources")

    __table_args__ = (
        Index("ix_sources_municipality_platform", "municipality_id", "platform"),
    )

    def __repr__(self) -> str:
        return f"<Source {self.label} ({self.platform.value})>"


class ScrapeRun(Base):
    __tablename__ = "scrape_runs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    source_id: Mapped[int] = mapped_column(Integer, ForeignKey("sources.id"), nullable=False)
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    status: Mapped[str] = mapped_column(String(20), default="running")  # running, success, error
    error_message: Mapped[str | None] = mapped_column(Text)
    documents_found: Mapped[int] = mapped_column(Integer, default=0)
    new_documents: Mapped[int] = mapped_column(Integer, default=0)

    __table_args__ = (Index("ix_scrape_runs_source_started", "source_id", "started_at"),)
