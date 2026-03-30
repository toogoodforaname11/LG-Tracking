"""Create all initial tables.

Revision ID: 000_initial_tables
Revises:
Create Date: 2026-03-30
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "000_initial_tables"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # --- municipalities ---
    op.create_table(
        "municipalities",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("short_name", sa.String(100), nullable=False),
        sa.Column(
            "gov_type",
            sa.Enum(
                "city", "district", "town", "village", "regional_district",
                "island_municipality", "mountain_resort", "regional_municipality",
                "unincorporated",
                name="govtype",
            ),
            nullable=False,
        ),
        sa.Column("region", sa.String(100), nullable=False, server_default="CRD"),
        sa.Column("website_url", sa.Text(), nullable=True),
        sa.Column("population", sa.Integer(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=True, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("short_name"),
    )

    # --- sources ---
    op.create_table(
        "sources",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("municipality_id", sa.Integer(), nullable=False),
        sa.Column(
            "platform",
            sa.Enum(
                "civicweb", "granicus", "civicplus", "escribe", "youtube", "custom", "unknown",
                name="platform",
            ),
            nullable=False,
        ),
        sa.Column(
            "source_type",
            sa.Enum("agenda", "minutes", "video", "notice", "bylaw", name="sourcetype"),
            nullable=False,
        ),
        sa.Column("url", sa.Text(), nullable=False),
        sa.Column("label", sa.String(200), nullable=False),
        sa.Column(
            "scrape_status",
            sa.Enum("active", "pending", "broken", "disabled", name="scrapestatus"),
            nullable=True,
        ),
        sa.Column("scrape_config", sa.Text(), nullable=True),
        sa.Column("last_scraped_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("last_error", sa.Text(), nullable=True),
        sa.Column("consecutive_failures", sa.Integer(), nullable=True, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["municipality_id"], ["municipalities.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_sources_municipality_platform", "sources", ["municipality_id", "platform"]
    )

    # --- scrape_runs ---
    op.create_table(
        "scrape_runs",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("source_id", sa.Integer(), nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("finished_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("status", sa.String(20), nullable=True, server_default="running"),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("documents_found", sa.Integer(), nullable=True, server_default="0"),
        sa.Column("new_documents", sa.Integer(), nullable=True, server_default="0"),
        sa.ForeignKeyConstraint(["source_id"], ["sources.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_scrape_runs_source_started", "scrape_runs", ["source_id", "started_at"]
    )

    # --- meetings ---
    op.create_table(
        "meetings",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("municipality_id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(300), nullable=False),
        sa.Column("meeting_date", sa.String(10), nullable=True),
        sa.Column("meeting_time", sa.String(5), nullable=True),
        sa.Column(
            "meeting_type",
            sa.Enum(
                "regular", "special", "public_hearing", "committee", "committee_of_the_whole",
                name="meetingtype",
            ),
            nullable=True,
        ),
        sa.Column("source_url", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["municipality_id"], ["municipalities.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_meetings_muni_date_type",
        "meetings",
        ["municipality_id", "meeting_date", "meeting_type"],
    )

    # --- documents ---
    op.create_table(
        "documents",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("meeting_id", sa.Integer(), nullable=True),
        sa.Column("municipality_id", sa.Integer(), nullable=False),
        sa.Column("source_id", sa.Integer(), nullable=True),
        sa.Column(
            "doc_type",
            sa.Enum(
                "agenda", "minutes", "video", "addendum", "bylaw", "notice", "staff_report",
                name="doctype",
            ),
            nullable=False,
        ),
        sa.Column("title", sa.String(500), nullable=False),
        sa.Column("url", sa.Text(), nullable=False),
        sa.Column("content_hash", sa.String(64), nullable=True),
        sa.Column("raw_text", sa.Text(), nullable=True),
        sa.Column("video_timestamps", sa.JSON(), nullable=True),
        sa.Column("video_duration", sa.String(10), nullable=True),
        sa.Column("is_new", sa.Boolean(), nullable=True, server_default="true"),
        sa.Column("is_processed", sa.Boolean(), nullable=True, server_default="false"),
        sa.Column("first_seen_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("last_checked_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["meeting_id"], ["meetings.id"]),
        sa.ForeignKeyConstraint(["municipality_id"], ["municipalities.id"]),
        sa.ForeignKeyConstraint(["source_id"], ["sources.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_documents_muni_url", "documents", ["municipality_id", "url"], unique=True
    )
    op.create_index("ix_documents_new", "documents", ["is_new"])

    # --- tracks ---
    op.create_table(
        "tracks",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.String(100), nullable=False),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("notification_email", sa.String(320), nullable=True),
        sa.Column("municipality_ids", sa.JSON(), nullable=False),
        sa.Column("topics", sa.JSON(), nullable=False),
        sa.Column("keywords", sa.JSON(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=True, server_default="true"),
        sa.Column("notify_email", sa.Boolean(), nullable=True, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_tracks_user", "tracks", ["user_id"])

    # --- track_matches (without relevant_timestamps — added in 001) ---
    op.create_table(
        "track_matches",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("track_id", sa.Integer(), nullable=False),
        sa.Column("document_id", sa.Integer(), nullable=False),
        sa.Column("match_score", sa.Float(), nullable=True),
        sa.Column("match_reason", sa.Text(), nullable=True),
        sa.Column("matched_topics", sa.JSON(), nullable=True),
        sa.Column("matched_keywords", sa.JSON(), nullable=True),
        sa.Column("summary", sa.Text(), nullable=True),
        sa.Column("key_points", sa.JSON(), nullable=True),
        sa.Column("verification_status", sa.String(20), nullable=True),
        sa.Column("verification_notes", sa.Text(), nullable=True),
        sa.Column("notified_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("notification_status", sa.String(20), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["track_id"], ["tracks.id"]),
        sa.ForeignKeyConstraint(["document_id"], ["documents.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("track_id", "document_id", name="uq_track_matches_track_document"),
    )
    op.create_index("ix_track_matches_track", "track_matches", ["track_id"])
    op.create_index("ix_track_matches_document", "track_matches", ["document_id"])

    # --- subscribers ---
    op.create_table(
        "subscribers",
        sa.Column("email", sa.String(320), nullable=False),
        sa.Column("municipalities", postgresql.JSONB(), nullable=False),
        sa.Column("topics", postgresql.JSONB(), nullable=False),
        sa.Column("keywords", sa.Text(), nullable=True),
        sa.Column("immediate_alerts", sa.Boolean(), nullable=True, server_default="false"),
        sa.Column("active", sa.Boolean(), nullable=True, server_default="true"),
        sa.Column(
            "unsubscribe_token",
            sa.String(36),
            nullable=False,
            server_default=sa.text("gen_random_uuid()::text"),
        ),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("email"),
    )

    # --- magic_link_tokens ---
    op.create_table(
        "magic_link_tokens",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("token", sa.String(36), nullable=False),
        sa.Column("email", sa.String(320), nullable=False),
        sa.Column("pending_preferences", postgresql.JSONB(), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("used_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_magic_link_tokens_token", "magic_link_tokens", ["token"], unique=True)
    op.create_index("ix_magic_link_tokens_email", "magic_link_tokens", ["email"])

    # --- api_cost_logs ---
    op.create_table(
        "api_cost_logs",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("service", sa.String(20), nullable=True),
        sa.Column("operation", sa.String(50), nullable=True),
        sa.Column("model", sa.String(100), nullable=True),
        sa.Column("input_tokens", sa.Integer(), nullable=True, server_default="0"),
        sa.Column("output_tokens", sa.Integer(), nullable=True, server_default="0"),
        sa.Column("total_tokens", sa.Integer(), nullable=True, server_default="0"),
        sa.Column("estimated_cost_usd", sa.Float(), nullable=True, server_default="0.0"),
        sa.Column("call_context", postgresql.JSONB(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_api_cost_logs_created_at", "api_cost_logs", ["created_at"])


def downgrade() -> None:
    op.drop_table("api_cost_logs")
    op.drop_table("magic_link_tokens")
    op.drop_table("subscribers")
    op.drop_table("track_matches")
    op.drop_table("tracks")
    op.drop_table("documents")
    op.drop_table("meetings")
    op.drop_table("scrape_runs")
    op.drop_table("sources")
    op.drop_table("municipalities")

    # Drop enum types
    for name in [
        "govtype", "platform", "sourcetype", "scrapestatus",
        "meetingtype", "doctype",
    ]:
        op.execute(f"DROP TYPE IF EXISTS {name}")
