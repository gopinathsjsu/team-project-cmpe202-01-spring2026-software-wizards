from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user, require_role
from app.models.user import User
from app.schemas.ticket import TicketTypeCreate, TicketTypeRead, TicketTypeUpdate
from app.crud.ticket_crud import ticket_crud
from app.crud.event_crud import event_crud

router = APIRouter(prefix="/events/{event_id}/tickets", tags=["tickets"])


async def _get_own_event(event_id: UUID, db: AsyncSession, current_user: User):
    event = await event_crud.get(db, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    if event.organizer_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not your event")
    return event


@router.get("", response_model=List[TicketTypeRead])
async def list_tickets(event_id: UUID, db: AsyncSession = Depends(get_db)):
    return await ticket_crud.get_by_event(db, event_id)


@router.post("", response_model=TicketTypeRead, status_code=201)
async def create_ticket(
    event_id: UUID,
    data: TicketTypeCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("organizer", "admin")),
):
    await _get_own_event(event_id, db, current_user)
    return await ticket_crud.create_for_event(db, event_id, data)


@router.put("/{ticket_id}", response_model=TicketTypeRead)
async def update_ticket(
    event_id: UUID,
    ticket_id: UUID,
    data: TicketTypeUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("organizer", "admin")),
):
    await _get_own_event(event_id, db, current_user)
    ticket = await ticket_crud.get(db, ticket_id)
    if not ticket or ticket.event_id != event_id:
        raise HTTPException(status_code=404, detail="Ticket type not found")
    return await ticket_crud.update(db, ticket, data)


@router.delete("/{ticket_id}", status_code=204)
async def delete_ticket(
    event_id: UUID,
    ticket_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("organizer", "admin")),
):
    await _get_own_event(event_id, db, current_user)
    ticket = await ticket_crud.get(db, ticket_id)
    if not ticket or ticket.event_id != event_id:
        raise HTTPException(status_code=404, detail="Ticket type not found")
    await ticket_crud.delete(db, ticket_id)
