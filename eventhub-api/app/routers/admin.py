import math
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from app.database import get_db, engine
from app.dependencies import require_role, get_current_user
from app.models.user import User
from app.schemas.user import UserRead
from app.schemas.event import EventRead, EventListItem
from app.schemas.common import PaginatedResponse
from app.crud.user_crud import user_crud
from app.crud.event_crud import event_crud
from app.services.event_service import event_subject

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/health")
async def health_check(db: AsyncSession = Depends(get_db)):
    """Health check endpoint for AWS ALB target group."""
    from datetime import datetime, timezone
    try:
        await db.execute(text("SELECT 1"))
        return {
            "status": "ok",
            "database": "connected",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception:
        from fastapi import Response
        return Response(
            content='{"status":"error","database":"unreachable"}',
            status_code=503,
            media_type="application/json",
        )


@router.get("/events", response_model=PaginatedResponse[EventListItem],
            dependencies=[Depends(require_role("admin"))])
async def list_pending_events(
    status: str = Query("pending", pattern="^(draft|pending|published|cancelled|rejected)$"),
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    events, total = await event_crud.search_and_filter(
        db, status=status, page=page, size=size
    )
    items = []
    for event in events:
        stats = await event_crud.get_stats(db, event.id)
        items.append(EventListItem(
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
        ))
    return PaginatedResponse(
        total=total, page=page, size=size,
        pages=math.ceil(total / size) if size else 1,
        items=items,
    )


@router.put("/events/{id}/approve", response_model=EventRead,
            dependencies=[Depends(require_role("admin"))])
async def approve_event(id: UUID, db: AsyncSession = Depends(get_db)):
    event = await event_crud.get_with_details(db, id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    if event.status != "pending":
        raise HTTPException(status_code=400, detail="Event is not pending review")

    old_status = event.status
    event.status = "published"
    db.add(event)
    await db.commit()

    # Observer: notify organizer
    await event_subject.notify(event, old_status, "published")
    return await event_crud.get_with_details(db, event.id)


@router.put("/events/{id}/reject", response_model=EventRead,
            dependencies=[Depends(require_role("admin"))])
async def reject_event(
    id: UUID,
    reason: str = "",
    db: AsyncSession = Depends(get_db),
):
    event = await event_crud.get_with_details(db, id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    if event.status != "pending":
        raise HTTPException(status_code=400, detail="Event is not pending review")

    old_status = event.status
    event.status = "rejected"
    event.rejection_reason = reason
    db.add(event)
    await db.commit()

    # Observer: notify organizer
    await event_subject.notify(event, old_status, "rejected")
    return await event_crud.get_with_details(db, event.id)


@router.get("/users", response_model=PaginatedResponse[UserRead],
            dependencies=[Depends(require_role("admin"))])
async def list_users(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    users = await user_crud.get_multi(db, skip=(page - 1) * size, limit=size)
    total = await user_crud.get_count(db)
    return PaginatedResponse(
        total=total, page=page, size=size,
        pages=math.ceil(total / size) if size else 1,
        items=[UserRead.model_validate(u) for u in users],
    )


@router.put("/users/{id}/suspend", response_model=UserRead,
            dependencies=[Depends(require_role("admin"))])
async def suspend_user(id: UUID, db: AsyncSession = Depends(get_db)):
    user = await user_crud.get(db, id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return await user_crud.set_active(db, user, False)


@router.put("/users/{id}/reactivate", response_model=UserRead,
            dependencies=[Depends(require_role("admin"))])
async def reactivate_user(id: UUID, db: AsyncSession = Depends(get_db)):
    user = await user_crud.get(db, id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return await user_crud.set_active(db, user, True)
