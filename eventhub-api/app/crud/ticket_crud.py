from typing import List, Optional
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base_crud import BaseCRUD
from app.models.ticket_type import TicketType
from app.schemas.ticket import TicketTypeCreate, TicketTypeUpdate


class TicketCRUD(BaseCRUD[TicketType, TicketTypeCreate, TicketTypeUpdate]):

    async def get_by_event(self, db: AsyncSession, event_id: UUID) -> List[TicketType]:
        result = await db.execute(
            select(TicketType)
            .where(TicketType.event_id == event_id)
            .order_by(TicketType.price)
        )
        return list(result.scalars().all())

    async def create_for_event(
        self, db: AsyncSession, event_id: UUID, data: TicketTypeCreate
    ) -> TicketType:
        ticket = TicketType(
            event_id=event_id,
            **data.model_dump(),
        )
        db.add(ticket)
        await db.commit()
        await db.refresh(ticket)
        return ticket

    async def get_active_by_event(self, db: AsyncSession, event_id: UUID) -> List[TicketType]:
        result = await db.execute(
            select(TicketType).where(
                TicketType.event_id == event_id,
                TicketType.is_active == True,
            )
        )
        return list(result.scalars().all())


ticket_crud = TicketCRUD(TicketType)
