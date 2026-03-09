import math
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.registration import RegistrationCreate, RegistrationRead
from app.schemas.common import PaginatedResponse
from app.crud.registration_crud import registration_crud
from app.services.registration_service import create_registration, cancel_registration

router = APIRouter(prefix="/registrations", tags=["registrations"])


@router.post("", response_model=RegistrationRead, status_code=201)
async def register_for_event(
    data: RegistrationCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    reg = await create_registration(db, data, current_user)
    return RegistrationRead.model_validate(reg)


@router.get("", response_model=PaginatedResponse[RegistrationRead])
async def list_my_registrations(
    status: Optional[str] = None,
    upcoming: bool = False,
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    regs, total = await registration_crud.get_by_attendee(
        db, current_user.id,
        status=status,
        upcoming=upcoming,
        page=page,
        size=size,
    )
    items = [RegistrationRead.model_validate(r) for r in regs]
    return PaginatedResponse(
        total=total, page=page, size=size,
        pages=math.ceil(total / size) if size else 1,
        items=items,
    )


@router.get("/{id}", response_model=RegistrationRead)
async def get_registration(
    id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    reg = await registration_crud.get_with_details(db, id)
    if not reg:
        raise HTTPException(status_code=404, detail="Registration not found")

    # Access control: owner, event organizer, or admin
    is_owner = reg.attendee_id == current_user.id
    is_organizer = (
        reg.event
        and reg.event.organizer_id == current_user.id
    )
    is_admin = current_user.role == "admin"
    if not (is_owner or is_organizer or is_admin):
        raise HTTPException(status_code=403, detail="Access denied")

    return RegistrationRead.model_validate(reg)


@router.delete("/{id}", status_code=200)
async def cancel_my_registration(
    id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    reg = await cancel_registration(db, id, current_user)
    return {"message": "Registration cancelled", "id": str(reg.id)}
