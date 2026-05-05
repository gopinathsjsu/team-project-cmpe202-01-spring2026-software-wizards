"""Improve event search vector and add trigram index

Revision ID: 002_search_improvements
Revises: 001_initial_schema
Create Date: 2026-05-05 00:00:00.000000
"""
from alembic import op

revision = "002_search_improvements"
down_revision = "001_initial_schema"
branch_labels = None
depends_on = None


SEARCH_VECTOR_SQL = """
setweight(to_tsvector('english', coalesce(NEW.title, '')), 'A') ||
setweight(to_tsvector('english', coalesce(array_to_string(NEW.tags, ' '), '')), 'B') ||
setweight(to_tsvector('english', coalesce(NEW.city, '') || ' ' || coalesce(NEW.venue_name, '')), 'C')
"""


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm")

    op.execute(f"""
        CREATE OR REPLACE FUNCTION events_search_vector_update() RETURNS trigger AS $$
        BEGIN
          NEW.search_vector := {SEARCH_VECTOR_SQL};
          RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
    """)

    op.execute(f"""
        UPDATE events
        SET search_vector = {SEARCH_VECTOR_SQL.replace('NEW.', '')};
    """)

    op.create_index(
        "events_title_trgm_idx",
        "events",
        ["title"],
        postgresql_using="gin",
        postgresql_ops={"title": "gin_trgm_ops"},
    )


def downgrade() -> None:
    op.drop_index("events_title_trgm_idx", table_name="events")

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
        UPDATE events
        SET search_vector = to_tsvector('english',
            coalesce(title,'') || ' ' || coalesce(description,''));
    """)

    op.execute("DROP EXTENSION IF EXISTS pg_trgm")
