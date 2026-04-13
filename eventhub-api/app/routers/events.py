import math
import csv
import io
from typing import Optional
from uuid import UUID
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user, require_role
from app.models.user import User
from app.schemas.event import EventCreate, EventUpdate, EventRead, EventListItem, AttendeeRecord, EventSubmitResponse
from app.schemas.common import PaginatedResponse
from app.crud.event_crud import event_crud
from app.crud.ticket_crud import ticket_crud
from app.crud.registration_crud import registration_crud
from app.services.event_service import event_subject, geocode_address
from app.services.calendar_service import build_google_link, build_outlook_link, build_ics

router = APIRouter(prefix="/events", tags=["events"])


def _to_event_list_item(event, stats: dict) -> EventListItem:
    return EventListItem(
        id=event.id,
        title=event.title,
        start_at=event.start_at,
        city=event.city,
        banner_url=event.banner_url,
        is_virtual=event.is_virtual,
        status=event.status,
        min_price=stats.get("min_price", 0.0),
        registration_count=stats.get("registration_count", 0),
        category=event.category,
    )


@router.get("", response_model=PaginatedResponse[EventListItem])
async def list_events(
    q: Optional[str] = None,
    category_id: Optional[UUID] = None,
    city: Optional[str] = None,
    date_from: Optional[datetime] = None,
    date_to: Optional[datetime] = None,
    is_virtual: Optional[bool] = None,
    is_free: Optional[bool] = None,
    sort: str = Query("date", pattern="^(date|popularity|recent)$"),
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    events, total = await event_crud.search_and_filter(
        db, q=q, category_id=category_id, city=city,
        date_from=date_from, date_to=date_to,
        is_virtual=is_virtual, is_free=is_free,
        sort=sort, page=page, size=size,
    )
    items = []
    for event in events:
        stats = await event_crud.get_stats(db, event.id)
        items.append(_to_event_list_item(event, stats))

    return PaginatedResponse(
        total=total,
        page=page,
        size=size,
        pages=math.ceil(total / size) if size else 1,
        items=items,
    )


@router.post("", response_model=EventRead, status_code=201)
async def create_event(
    data: EventCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("organizer", "admin")),
):
    # Auto-geocode if address provided but no lat/lng
    if data.address and not data.latitude:
        coords = await geocode_address(data.address)
        if coords:
            data = data.model_copy(update={"latitude": coords[0], "longitude": coords[1]})

    event = await event_crud.create_event(db, data, current_user.id)
    return await event_crud.get_with_details(db, event.id)


@router.get("/{id}", response_model=EventRead)
async def get_event(id: UUID, db: AsyncSession = Depends(get_db)):
    event = await event_crud.get_with_details(db, id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    stats = await event_crud.get_stats(db, event.id)
    # Attach stats to the response model
    result = EventRead.model_validate(event)
    result.registration_count = stats["registration_count"]
    return result


@router.put("/{id}", response_model=EventRead)
async def update_event(
    id: UUID,
    data: EventUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    event = await event_crud.get(db, id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    if event.organizer_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not your event")
    if event.status == "published":
        raise HTTPException(status_code=400, detail="Cannot edit a published event. Cancel it first.")

    # Re-geocode if address changed
    if data.address and data.address != event.address:
        coords = await geocode_address(data.address)
        if coords:
            data = data.model_copy(update={"latitude": coords[0], "longitude": coords[1]})

    updated = await event_crud.update(db, event, data)
    return await event_crud.get_with_details(db, updated.id)


@router.delete("/{id}", status_code=204)
async def delete_event(
    id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    event = await event_crud.get_with_details(db, id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    if event.organizer_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not your event")

    old_status = event.status
    event.status = "cancelled"
    db.add(event)
    await db.commit()

    # Trigger Observer notifications (emails all confirmed registrants)
    await event_subject.notify(event, old_status, "cancelled")


@router.post("/{id}/submit", response_model=EventSubmitResponse)
async def submit_event(
    id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("organizer", "admin")),
):
    event = await event_crud.get(db, id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    if event.organizer_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not your event")
    if event.status not in ("draft", "rejected"):
        raise HTTPException(status_code=400, detail="Only draft or rejected events can be submitted")

    active_tickets = await ticket_crud.get_active_by_event(db, event.id)
    if not active_tickets:
        raise HTTPException(status_code=400, detail="Event must have at least one active ticket type before submitting")

    event.status = "pending"
    db.add(event)
    await db.commit()
    return EventSubmitResponse(id=event.id, status="pending", message="Event submitted for review")


@router.get("/{id}/attendees", response_model=PaginatedResponse[AttendeeRecord])
async def get_attendees(
    id: UUID,
    format: Optional[str] = None,
    page: int = Query(1, ge=1),
    size: int = Query(50, ge=1, le=200),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    event = await event_crud.get(db, id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    if event.organizer_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Insufficient permissions")

    rows, total = await event_crud.get_attendees(db, id, page=page, size=size)

    if format == "csv":
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=[
            "attendee_id", "first_name", "last_name", "email",
            "ticket_name", "quantity", "total_amount", "status",
            "checked_in_at", "registered_at",
        ])
        writer.writeheader()
        for row in rows:
            writer.writerow(dict(row))
        output.seek(0)
        return StreamingResponse(
            iter([output.getvalue()]),
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename=attendees_{id}.csv"},
        )

    items = [AttendeeRecord(**dict(r)) for r in rows]
    return PaginatedResponse(
        total=total,
        page=page,
        size=size,
        pages=math.ceil(total / size) if size else 1,
        items=items,
    )


@router.post("/{id}/checkin/{registration_id}")
async def checkin(
    id: UUID,
    registration_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("organizer", "admin")),
):
    event = await event_crud.get(db, id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    if event.organizer_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not your event")

    reg = await registration_crud.get_with_details(db, registration_id)
    if not reg or reg.event_id != id:
        raise HTTPException(status_code=404, detail="Registration not found for this event")
    if reg.checked_in_at:
        raise HTTPException(status_code=409, detail="Already checked in")

    reg = await registration_crud.checkin(db, reg)
    return {"message": "Checked in successfully", "checked_in_at": reg.checked_in_at}


@router.get("/{id}/calendar.ics")
async def download_ics(id: UUID, db: AsyncSession = Depends(get_db)):
    event = await event_crud.get(db, id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    ics_bytes = build_ics(event)
    return Response(
        content=ics_bytes,
        media_type="text/calendar",
        headers={"Content-Disposition": f'attachment; filename="event_{id}.ics"'},
    )


@router.get("/{id}/calendar-link")
async def get_calendar_link(id: UUID, db: AsyncSession = Depends(get_db)):
    event = await event_crud.get(db, id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return {
        "google": build_google_link(event),
        "outlook": build_outlook_link(event),
    }