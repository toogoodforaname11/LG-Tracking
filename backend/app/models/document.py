import enum
from datetime import datetime, timezone

from sqlalchemy import String, Text, Enum, DateTime, Integer, Boolean, ForeignKey, Index, JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class DocType(str, enum.Enum):
    AGENDA = "agenda"
    MINUTES = "minutes"
    VIDEO = "video"
    ADDENDUM = "addendum"
    BYLAW = "bylaw"
    NOTICE = "notice"
    STAFF_REPORT = "staff_report"


class MeetingType(str, enum.Enum):
    REGULAR = "regular"
    SPECIAL = "special"
    PUBLIC_HEARING = "public_hearing"
    COMMITTEE = "committee"
    COW = "committee_of_the_whole"


class Meeting(Base):
    __tablename__ = "meetings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    municipality_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("municipalities.id"), nullable=False
    )
    title: Mapped[str] = mapped_column(String(300), nullable=False)
    meeting_date: Mapped[str | None] = mapped_column(String(10))  # YYYY-MM-DD
    meeting_time: Mapped[str | None] = mapped_column(String(5))   # HH:MM
    meeting_type: Mapped[MeetingType | None] = mapped_column(Enum(MeetingType))
    source_url: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )

    __table_args__ = (
        Index("ix_meetings_muni_date_type", "municipality_id", "meeting_date", "meeting_type"),
    )


class Document(Base):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    meeting_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("meetings.id"))
    municipality_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("municipalities.id"), nullable=False
    )
    source_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("sources.id"))
    doc_type: Mapped[DocType] = mapped_column(Enum(DocType), nullable=False)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    url: Mapped[str] = mapped_column(Text, nullable=False)
    content_hash: Mapped[str | None] = mapped_column(String(64))  # SHA-256
    raw_text: Mapped[str | None] = mapped_column(Text)  # Extracted text for AI processing
    video_timestamps: Mapped[list | None] = mapped_column(JSON)  # [{t: "0:15:30", label: "..."}, ...]
    video_duration: Mapped[str | None] = mapped_column(String(10))  # HH:MM:SS
    is_new: Mapped[bool] = mapped_column(Boolean, default=True)
    is_processed: Mapped[bool] = mapped_column(Boolean, default=False)  # AI processing done
    first_seen_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )
    last_checked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    __table_args__ = (
        Index("ix_documents_muni_url", "municipality_id", "url", unique=True),
        Index("ix_documents_new", "is_new"),
    )
