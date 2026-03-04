"""
Repository Pattern — EventCRUD extends BaseCRUD with domain-specific queries:
- Full-text search via PostgreSQL tsvector GIN index
- Filter by category, city, date range, virtual, free
- Strategy pattern integration for sorting
- Stats aggregation (min_price, registration_count)
"""
from typing import Optional, List, Tuple
from uuid import UUID
from datetime import datetime

from sqlalchemy import select, func, text, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.crud.base_crud import BaseCRUD
from app.models.event import Event
from app.models.ticket_type import TicketType
from app.models.registration import Registration
from app.models.user import User
from app.models.category import Category
from app.schemas.event import EventCreate, EventUpdate


class EventCRUD(BaseCRUD[Event, EventCreate, EventUpdate]):

    async def get_with_details(self, db: AsyncSession, id: UUID) -> Optional[Event]:
        """Fetch a single event with all related data eagerly loaded."""
        result = await db.execute(
            select(Event)
            .options(
                selectinload(Event.organizer),
                selectinload(Event.category),
                selectinload(Event.ticket_types),
            )
            .where(Event.id == id)
        )
        return result.scalar_one_or_none()

    async def search_and_filter(
        self,
        db: AsyncSession,
        *,
        q: Optional[str] = None,
        category_id: Optional[UUID] = None,
        city: Optional[str] = None,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
        is_virtual: Optional[bool] = None,
        is_free: Optional[bool] = None,
        sort: str = "date",
        page: int = 1,
        size: int = 20,
        status: str = "published",
    ) -> Tuple[List[Event], int]:
        """Search + filter events. Returns (items, total)."""
        # Import here to avoid circular import
        from app.services.event_service import SORT_STRATEGIES

        query = (
            select(Event)
            .options(selectinload(Event.category), selectinload(Event.ticket_types))
            .where(Event.status == status)
        )

        # Full-text search
        if q:
            query = query.where(
                Event.search_vector.op("@@")(func.plainto_tsquery("english", q))
            )

        if category_id:
            query = query.where(Event.category_id == category_id)

        if city:
            query = query.where(func.lower(Event.city) == func.lower(city))

        if date_from:
            query = query.where(Event.start_at >= date_from)

        if date_to:
            query = query.where(Event.start_at <= date_to)

        if is_virtual is not None:
            query = query.where(Event.is_virtual == is_virtual)

        if is_free:
            # Has at least one free ticket type
            free_subq = (
                select(TicketType.event_id)
                .where(TicketType.price == 0, TicketType.is_active == True)
                .scalar_subquery()
            )
            query = query.where(Event.id.in_(free_subq))

        # Count total before pagination
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await db.execute(count_query)
        total = total_result.scalar_one()

        # Apply sort strategy
        strategy = SORT_STRATEGIES.get(sort, SORT_STRATEGIES["date"])
        query = strategy.apply(query)

        # Pagination
        skip = (page - 1) * size
        query = query.offset(skip).limit(size)
        result = await db.execute(query)
        events = list(result.scalars().all())
        return events, total

    async def get_by_organizer(
        self, db: AsyncSession, organizer_id: UUID, page: int = 1, size: int = 20
    ) -> Tuple[List[Event], int]:
        base_q = select(Event).where(Event.organizer_id == organizer_id)
        total_result = await db.execute(select(func.count()).select_from(base_q.subquery()))
        total = total_result.scalar_one()
        result = await db.execute(
            base_q
            .options(selectinload(Event.category), selectinload(Event.ticket_types))
            .order_by(Event.created_at.desc())
            .offset((page - 1) * size)
            .limit(size)
        )
        return list(result.scalars().all()), total

    async def get_attendees(
        self, db: AsyncSession, event_id: UUID, page: int = 1, size: int = 50
    ):
        """Return attendee records for organizer/admin view."""
        from app.models.user import User as UserModel

        query = (
            select(
                Registration.id,
                UserModel.id.label("attendee_id"),
                UserModel.first_name,
                UserModel.last_name,
                UserModel.email,
                TicketType.name.label("ticket_name"),
                Registration.quantity,
                Registration.total_amount,
                Registration.status,
                Registration.checked_in_at,
                Registration.created_at.label("registered_at"),
            )
            .join(UserModel, Registration.attendee_id == UserModel.id)
            .join(TicketType, Registration.ticket_type_id == TicketType.id)
            .where(Registration.event_id == event_id)
        )
        total_result = await db.execute(select(func.count()).select_from(query.subquery()))
        total = total_result.scalar_one()
        result = await db.execute(query.offset((page - 1) * size).limit(size))
        return list(result.mappings().all()), total

    async def get_stats(self, db: AsyncSession, event_id: UUID) -> dict:
        """Return min_price and registration_count for a single event."""
        min_price_result = await db.execute(
            select(func.min(TicketType.price))
            .where(TicketType.event_id == event_id, TicketType.is_active == True)
        )
        min_price = min_price_result.scalar_one_or_none() or 0.0

        reg_count_result = await db.execute(
            select(func.count(Registration.id))
            .where(Registration.event_id == event_id, Registration.status == "confirmed")
        )
        reg_count = reg_count_result.scalar_one()
        return {"min_price": float(min_price), "registration_count": reg_count}

    async def create_event(self, db: AsyncSession, data: EventCreate, organizer_id: UUID) -> Event:
        event = Event(
            organizer_id=organizer_id,
            **data.model_dump(),
        )
        db.add(event)
        await db.commit()
        await db.refresh(event)
        return event

    async def get_upcoming_for_reminder(
        self, db: AsyncSession, hours_from: int = 47, hours_to: int = 49
    ) -> List[Event]:
        """Find published events starting in 47–49 hours (for reminder job)."""
        from datetime import timedelta, timezone
        now = datetime.now(timezone.utc)
        window_start = now + timedelta(hours=hours_from)
        window_end = now + timedelta(hours=hours_to)
        result = await db.execute(
            select(Event)
            .where(
                Event.status == "published",
                Event.start_at >= window_start,
                Event.start_at <= window_end,
            )
        )
        return list(result.scalars().all())


event_crud = EventCRUD(Event)