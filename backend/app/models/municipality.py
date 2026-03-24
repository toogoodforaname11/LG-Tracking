import enum
from datetime import datetime

from sqlalchemy import String, Text, Enum, DateTime, Integer, Boolean, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class GovType(str, enum.Enum):
    CITY = "city"
    DISTRICT = "district"
    TOWN = "town"
    VILLAGE = "village"
    REGIONAL_DISTRICT = "regional_district"
    ISLAND_MUNICIPALITY = "island_municipality"
    MOUNTAIN_RESORT = "mountain_resort"
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
    short_name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    gov_type: Mapped[GovType] = mapped_column(Enum(GovType), nullable=False)
    region: Mapped[str] = mapped_column(String(100), nullable=False, default="CRD")
    website_url: Mapped[str | None] = mapped_column(Text)
    population: Mapped[int | None] = mapped_column(Integer)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    sources: Mapped[list["Source"]] = relationship(back_populates="municipality", cascade="all")

    def __repr__(self) -> str:
        return f"<Municipality {self.short_name}>"


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
    last_scraped_at: Mapped[datetime | None] = mapped_column(DateTime)
    last_error: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
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
    started_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime)
    status: Mapped[str] = mapped_column(String(20), default="running")  # running, success, error
    error_message: Mapped[str | None] = mapped_column(Text)
    documents_found: Mapped[int] = mapped_column(Integer, default=0)
    new_documents: Mapped[int] = mapped_column(Integer, default=0)

    __table_args__ = (Index("ix_scrape_runs_source_started", "source_id", "started_at"),)
