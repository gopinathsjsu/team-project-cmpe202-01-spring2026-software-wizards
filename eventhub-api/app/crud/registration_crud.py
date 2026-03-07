"""
Repository Pattern — RegistrationCRUD adds SELECT FOR UPDATE for concurrency-safe ticket booking.
"""
from typing import List, Optional, Tuple
from uuid import UUID
from datetime import datetime, timezone

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.crud.base_crud import BaseCRUD
from app.models.registration import Registration
from app.models.ticket_type import TicketType
from app.schemas.registration import RegistrationCreate


class RegistrationCRUD(BaseCRUD[Registration, RegistrationCreate, RegistrationCreate]):

    async def get_by_attendee(
        self,
        db: AsyncSession,
        attendee_id: UUID,
        status: Optional[str] = None,
        upcoming: bool = False,
        page: int = 1,
        size: int = 20,
    ) -> Tuple[List[Registration], int]:
        from app.models.event import Event

        query = (
            select(Registration)
            .join(Event, Registration.event_id == Event.id)
            .options(
                selectinload(Registration.event),
                selectinload(Registration.ticket_type),
            )
            .where(Registration.attendee_id == attendee_id)
        )
        if status:
            query = query.where(Registration.status == status)
        if upcoming:
            query = query.where(Event.start_at > datetime.now(timezone.utc))

        total_result = await db.execute(select(func.count()).select_from(query.subquery()))
        total = total_result.scalar_one()

        result = await db.execute(
            query.order_by(Registration.created_at.desc())
            .offset((page - 1) * size)
            .limit(size)
        )
        return list(result.scalars().all()), total

    async def select_for_update(
        self, db: AsyncSession, ticket_type_id: UUID
    ) -> Optional[TicketType]:
        """Lock the ticket_type row to prevent overselling (SELECT FOR UPDATE)."""
        result = await db.execute(
            select(TicketType)
            .where(TicketType.id == ticket_type_id)
            .with_for_update()
        )
        return result.scalar_one_or_none()

    async def get_confirmed(self, db: AsyncSession, event_id: UUID) -> List[Registration]:
        """Fetch confirmed registrations for an event (used by Observer pattern)."""
        result = await db.execute(
            select(Registration)
            .options(selectinload(Registration.attendee))
            .where(
                Registration.event_id == event_id,
                Registration.status == "confirmed",
            )
        )
        return list(result.scalars().all())

    async def get_unreminded(
        self, db: AsyncSession, event_id: UUID
    ) -> List[Registration]:
        """Confirmed registrations that haven't received a reminder yet."""
        result = await db.execute(
            select(Registration)
            .options(selectinload(Registration.attendee))
            .where(
                Registration.event_id == event_id,
                Registration.status == "confirmed",
                Registration.reminder_sent == False,
            )
        )
        return list(result.scalars().all())

    async def get_with_details(
        self, db: AsyncSession, registration_id: UUID
    ) -> Optional[Registration]:
        result = await db.execute(
            select(Registration)
            .options(
                selectinload(Registration.event),
                selectinload(Registration.ticket_type),
                selectinload(Registration.attendee),
            )
            .where(Registration.id == registration_id)
        )
        return result.scalar_one_or_none()

    async def checkin(self, db: AsyncSession, registration: Registration) -> Registration:
        registration.checked_in_at = datetime.now(timezone.utc)
        db.add(registration)
        await db.commit()
        await db.refresh(registration)
        return registration


registration_crud = RegistrationCRUD(Registration)
