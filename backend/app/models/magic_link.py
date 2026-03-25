"""Magic link tokens — short-lived tokens for confirming subscriber preference updates."""

import uuid
from datetime import datetime, timezone

from sqlalchemy import String, DateTime, text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class MagicLinkToken(Base):
    __tablename__ = "magic_link_tokens"

    id: Mapped[int] = mapped_column(primary_key=True)

    # The token embedded in the magic link URL — UUID, never reused.
    token: Mapped[str] = mapped_column(
        String(36),
        nullable=False,
        unique=True,
        index=True,
        default=lambda: str(uuid.uuid4()),
    )

    # Subscriber email this token is for.
    email: Mapped[str] = mapped_column(String(320), nullable=False, index=True)

    # The full preferences payload to apply when the token is verified.
    # Stored as JSONB so no separate columns are needed if fields change.
    pending_preferences: Mapped[dict] = mapped_column(JSONB, nullable=False)

    # Tokens expire after 24 hours — set server-side at creation.
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    # Null until the token is consumed — prevents replay.
    used_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )

    @property
    def is_valid(self) -> bool:
        """True if the token has not been used and has not expired."""
        return self.used_at is None and datetime.now(timezone.utc) < self.expires_at

    def __repr__(self) -> str:
        return f"<MagicLinkToken email={self.email} used={self.used_at is not None}>"
