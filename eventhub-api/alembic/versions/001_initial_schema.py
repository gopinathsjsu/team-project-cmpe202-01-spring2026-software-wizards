"""Initial schema with all tables and search trigger

Revision ID: 001_initial_schema
Revises:
Create Date: 2026-01-01 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "001_initial_schema"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Enums
    op.execute("CREATE TYPE user_role AS ENUM ('attendee', 'organizer', 'admin')")
    op.execute("CREATE TYPE event_status AS ENUM ('draft', 'pending', 'published', 'cancelled', 'rejected')")
    op.execute("CREATE TYPE registration_status AS ENUM ('confirmed', 'cancelled', 'pending')")

    # users
    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("email", sa.String(255), nullable=False, unique=True),
        sa.Column("password_hash", sa.String(255), nullable=False),
        sa.Column("first_name", sa.String(100), nullable=False),
        sa.Column("last_name", sa.String(100), nullable=False),
        sa.Column("role", sa.Enum("attendee", "organizer", "admin", name="user_role"), nullable=False),
        sa.Column("bio", sa.Text, nullable=True),
        sa.Column("avatar_url", sa.String(512), nullable=True),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_users_email", "users", ["email"])

    # categories
    op.create_table(
        "categories",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String(100), nullable=False, unique=True),
        sa.Column("slug", sa.String(100), nullable=False, unique=True),
        sa.Column("icon", sa.String(10), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_categories_slug", "categories", ["slug"])

    # events
    op.create_table(
        "events",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("organizer_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("category_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("categories.id", ondelete="SET NULL"), nullable=True),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("description", sa.Text, nullable=False),
        sa.Column("status", sa.Enum("draft", "pending", "published", "cancelled", "rejected", name="event_status"), nullable=False, server_default="draft"),
        sa.Column("start_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("end_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("timezone", sa.String(50), nullable=False, server_default="UTC"),
        sa.Column("venue_name", sa.String(255), nullable=True),
        sa.Column("address", sa.String(512), nullable=True),
        sa.Column("city", sa.String(100), nullable=True),
        sa.Column("latitude", sa.Numeric(10, 7), nullable=True),
        sa.Column("longitude", sa.Numeric(10, 7), nullable=True),
        sa.Column("capacity", sa.Integer, nullable=False, server_default="100"),
        sa.Column("is_virtual", sa.Boolean, nullable=False, server_default="false"),
        sa.Column("banner_url", sa.String(512), nullable=True),
        sa.Column("tags", postgresql.ARRAY(sa.String), nullable=True),
        sa.Column("search_vector", postgresql.TSVECTOR, nullable=True),
        sa.Column("rejection_reason", sa.Text, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_events_organizer_id", "events", ["organizer_id"])
    op.create_index("ix_events_status", "events", ["status"])
    op.create_index("ix_events_city", "events", ["city"])
    op.create_index("events_search_idx", "events", ["search_vector"], postgresql_using="gin")

    # PostgreSQL full-text search trigger
    op.execute("""
        CREATE OR REPLACE FUNCTION events_search_vector_update() RETURNS trigger AS $$
        BEGIN
          NEW.search_vector := to_tsvector('english',
            coalesce(NEW.title,'') || ' ' || coalesce(NEW.description,''));
          RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
    """)
    op.execute("""
        CREATE TRIGGER events_search_vector_trigger
        BEFORE INSERT OR UPDATE ON events
        FOR EACH ROW EXECUTE FUNCTION events_search_vector_update();
    """)

    # ticket_types
    op.create_table(
        "ticket_types",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("event_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("events.id", ondelete="CASCADE"), nullable=False),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("price", sa.Numeric(10, 2), nullable=False, server_default="0.00"),
        sa.Column("quantity_total", sa.Integer, nullable=False),
        sa.Column("quantity_sold", sa.Integer, nullable=False, server_default="0"),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default="true"),
        sa.Column("sale_ends_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_ticket_types_event_id", "ticket_types", ["event_id"])

    # registrations
    op.create_table(
        "registrations",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("attendee_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("event_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("events.id", ondelete="CASCADE"), nullable=False),
        sa.Column("ticket_type_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("ticket_types.id", ondelete="CASCADE"), nullable=False),
        sa.Column("status", sa.Enum("confirmed", "cancelled", "pending", name="registration_status"), nullable=False, server_default="confirmed"),
        sa.Column("quantity", sa.Integer, nullable=False, server_default="1"),
        sa.Column("total_amount", sa.Numeric(10, 2), nullable=False, server_default="0.00"),
        sa.Column("payment_ref", sa.String(100), nullable=True),
        sa.Column("qr_token", sa.String(64), nullable=False, unique=True),
        sa.Column("checked_in_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("reminder_sent", sa.Boolean, nullable=False, server_default="false"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_registrations_attendee_id", "registrations", ["attendee_id"])
    op.create_index("ix_registrations_event_id", "registrations", ["event_id"])
    op.create_index("ix_registrations_qr_token", "registrations", ["qr_token"])

    # password_reset_tokens
    op.create_table(
        "password_reset_tokens",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("token", sa.String(64), nullable=False, unique=True),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("used", sa.Boolean, nullable=False, server_default="false"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_password_reset_tokens_token", "password_reset_tokens", ["token"])


def downgrade() -> None:
    op.drop_table("password_reset_tokens")
    op.drop_table("registrations")
    op.drop_table("ticket_types")
    op.execute("DROP TRIGGER IF EXISTS events_search_vector_trigger ON events")
    op.execute("DROP FUNCTION IF EXISTS events_search_vector_update()")
    op.drop_table("events")
    op.drop_table("categories")
    op.drop_table("users")
    op.execute("DROP TYPE IF EXISTS registration_status")
    op.execute("DROP TYPE IF EXISTS event_status")
    op.execute("DROP TYPE IF EXISTS user_role")
