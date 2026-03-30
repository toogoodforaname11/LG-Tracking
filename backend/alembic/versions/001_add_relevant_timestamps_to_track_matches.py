"""Add relevant_timestamps column to track_matches.

Revision ID: 001_add_relevant_timestamps
Revises:
Create Date: 2026-03-30
"""

from alembic import op
import sqlalchemy as sa

revision = "001_add_relevant_timestamps"
down_revision = "000_initial_tables"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "track_matches",
        sa.Column("relevant_timestamps", sa.JSON(), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("track_matches", "relevant_timestamps")
