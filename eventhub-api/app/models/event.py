import uuid
from sqlalchemy import String, Text, Boolean, Numeric, Integer, DateTime, ForeignKey, Enum as SAEnum, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID, ARRAY, TSVECTOR
from datetime import datetime

from app.database import Base
from app.models.base import TimestampMixin


class Event(Base, TimestampMixin):
    __tablename__ = "events"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organizer_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    category_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("categories.id", ondelete="SET NULL"), nullable=True, index=True)

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(
        SAEnum("draft", "pending", "published", "cancelled", "rejected", name="event_status"),
        default="draft",
        nullable=False,
        index=True,
    )

    start_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    end_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    timezone: Mapped[str] = mapped_column(String(50), default="UTC", nullable=False)

    venue_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    address: Mapped[str | None] = mapped_column(String(512), nullable=True)
    city: Mapped[str | None] = mapped_column(String(100), nullable=True, index=True)
    latitude: Mapped[float | None] = mapped_column(Numeric(10, 7), nullable=True)
    longitude: Mapped[float | None] = mapped_column(Numeric(10, 7), nullable=True)

    capacity: Mapped[int] = mapped_column(Integer, default=100, nullable=False)
    is_virtual: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    banner_url: Mapped[str | None] = mapped_column(String(512), nullable=True)
    tags: Mapped[list[str] | None] = mapped_column(ARRAY(String), nullable=True)

    # Full-text search vector (populated by PostgreSQL trigger)
    search_vector = mapped_column(TSVECTOR, nullable=True)

    rejection_reason: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Relationships
    organizer = relationship("User", back_populates="events", lazy="noload")
    category = relationship("Category", back_populates="events", lazy="noload")
    ticket_types = relationship("TicketType", back_populates="event", lazy="noload", cascade="all, delete-orphan")
    registrations = relationship("Registration", back_populates="event", lazy="noload")

    __table_args__ = (
        Index("events_search_idx", "search_vector", postgresql_using="gin"),
    )