"""Email subscriber model — email is the primary key, upsert on re-subscribe."""

import uuid
from datetime import datetime, timezone

from sqlalchemy import String, Text, Boolean, DateTime, text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class Subscriber(Base):
    __tablename__ = "subscribers"

    email: Mapped[str] = mapped_column(String(320), primary_key=True)
    municipalities: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    topics: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    keywords: Mapped[str | None] = mapped_column(Text)
    immediate_alerts: Mapped[bool] = mapped_column(Boolean, default=False)
    active: Mapped[bool] = mapped_column(Boolean, default=True)

    # Token used in unsubscribe URLs — never exposes the subscriber's email
    # in the URL, preventing anyone who knows an email from unsubscribing them.
    # server_default ensures existing rows get a UUID on the next DB migration.
    unsubscribe_token: Mapped[str] = mapped_column(
        String(36),
        nullable=False,
        server_default=text("gen_random_uuid()::text"),
        default=lambda: str(uuid.uuid4()),
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    def __repr__(self) -> str:
        return f"<Subscriber {self.email}>"
