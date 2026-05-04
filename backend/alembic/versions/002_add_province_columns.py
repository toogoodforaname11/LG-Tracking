"""Add province columns to municipalities and subscribers.

Revision ID: 002_add_province_columns
Revises: 001_add_relevant_timestamps
Create Date: 2026-05-04

Schema changes:
- Add ``province`` (String, NOT NULL, default 'BC') to ``municipalities``.
- Drop the single-column UNIQUE on ``municipalities.short_name`` and replace
  it with a composite UNIQUE on ``(short_name, province)`` so BC and Alberta
  can independently use the same short name (e.g. "Lacombe").
- Add ``province`` (String, NOT NULL, default 'BC') to ``subscribers`` so each
  subscriber is scoped to one province at a time.

Stored as plain strings (no Postgres enum) — adding more provinces later
should not require an enum-type ALTER. Validation happens at the API layer
via ``app.models.municipality.VALID_PROVINCES``.
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "002_add_province_columns"
down_revision: str = "001_add_relevant_timestamps"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # --- municipalities.province ---
    op.add_column(
        "municipalities",
        sa.Column(
            "province",
            sa.String(length=40),
            nullable=False,
            server_default="BC",
        ),
    )
    op.create_index(
        "ix_municipalities_province",
        "municipalities",
        ["province"],
    )

    # Drop the legacy single-column UNIQUE on short_name.
    # Postgres auto-names this constraint ``municipalities_short_name_key``
    # when SQLAlchemy emits ``UNIQUE`` inline. Use IF EXISTS so the migration
    # is safe on databases that may have an older non-default constraint name
    # (e.g. older deployments that ran ``Base.metadata.create_all``).
    op.execute(
        "ALTER TABLE municipalities DROP CONSTRAINT IF EXISTS municipalities_short_name_key"
    )

    op.create_unique_constraint(
        "uq_muni_short_province",
        "municipalities",
        ["short_name", "province"],
    )

    # --- subscribers.province ---
    op.add_column(
        "subscribers",
        sa.Column(
            "province",
            sa.String(length=40),
            nullable=False,
            server_default="BC",
        ),
    )


def downgrade() -> None:
    # subscribers
    op.drop_column("subscribers", "province")

    # municipalities
    op.drop_constraint("uq_muni_short_province", "municipalities", type_="unique")
    # Recreate the legacy single-column UNIQUE under the same auto-generated name
    # so re-running upgrade keeps drop-and-recreate symmetrical.
    op.create_unique_constraint(
        "municipalities_short_name_key",
        "municipalities",
        ["short_name"],
    )
    op.drop_index("ix_municipalities_province", table_name="municipalities")
    op.drop_column("municipalities", "province")
