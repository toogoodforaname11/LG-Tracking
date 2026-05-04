"""Add municipalities.tier column for Ontario upper/lower/single distinction.

Revision ID: 003_add_municipality_tier
Revises: 002_add_province_columns
Create Date: 2026-05-04

Schema changes:
- Add ``tier`` (String(20), NOT NULL, server_default='single') to
  ``municipalities``. Existing 457 BC + AB rows backfill automatically.
- Index on tier for cheap filtering by tier on the registry endpoint.

Stored as a plain string (no Postgres enum) — same rationale as the
province column: adding a hypothetical 4th tier later should not require
an enum-type ALTER. Validation lives at the API layer in
``app.models.municipality.VALID_TIERS``.

We deliberately do NOT extend the existing UNIQUE constraint
``uq_muni_short_province`` to include tier. Ontario today has no
``(short_name, province)`` collisions where the only differentiator is
tier; adding tier to the constraint would let two "Caledon" rows coexist
which is more confusing than helpful. The constraint can be widened
later non-destructively if a real collision appears.
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "003_add_municipality_tier"
down_revision: str = "002_add_province_columns"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "municipalities",
        sa.Column(
            "tier",
            sa.String(length=20),
            nullable=False,
            server_default="single",
        ),
    )
    op.create_index(
        "ix_municipalities_tier",
        "municipalities",
        ["tier"],
    )


def downgrade() -> None:
    op.drop_index("ix_municipalities_tier", table_name="municipalities")
    op.drop_column("municipalities", "tier")
