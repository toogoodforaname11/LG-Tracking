"""Email subscriber model — email is the primary key, upsert on re-subscribe."""

from datetime import datetime

from sqlalchemy import String, Text, Boolean, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class Subscriber(Base):
    __tablename__ = "subscribers"

    email: Mapped[str] = mapped_column(String(320), primary_key=True)
    municipalities: Mapped[dict] = mapped_column(JSONB, nullable=False, default=list)
    topics: Mapped[dict] = mapped_column(JSONB, nullable=False, default=list)
    keywords: Mapped[str | None] = mapped_column(Text)
    immediate_alerts: Mapped[bool] = mapped_column(Boolean, default=False)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def __repr__(self) -> str:
        return f"<Subscriber {self.email}>"
