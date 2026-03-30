"""Add relevant_timestamps column to track_matches.

Revision ID: 001_add_relevant_timestamps
Revises: 000_initial_schema
Create Date: 2026-03-30

Note: The relevant_timestamps column is now included in the initial schema
migration (000_initial_schema). This migration is kept as a no-op for
existing deployments where the initial schema was applied before
relevant_timestamps existed.
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "001_add_relevant_timestamps"
down_revision: str = "000_initial_schema"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Column is already created in 000_initial_schema; nothing to do.
    pass


def downgrade() -> None:
    # Nothing to undo since upgrade is a no-op.
    pass
