"""
Registration service — orchestrates the full registration flow:
1. Validate event/ticket
2. SELECT FOR UPDATE (concurrency safety)
3. Luhn card validation
4. Create registration + increment sold count
5. Fire-and-forget confirmation email
"""
import asyncio
import secrets
import re
from datetime import datetime, timezone
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.schemas.registration import RegistrationCreate


def luhn_check(card_number: str) -> bool:
    """Luhn algorithm for mock card validation."""
    n = re.sub(r"\D", "", card_number)  # strip non-digits
    total = 0
    alt = False
    for i in range(len(n) - 1, -1, -1):
        d = int(n[i])
        if alt:
            d *= 2
            if d > 9:
                d -= 9
        total += d
        alt = not alt
    return total % 10 == 0


async def create_registration(
    db: AsyncSession,
    data: RegistrationCreate,
    current_user: User,
):
    """Full registration flow as specified in PRD §6.6."""
    from app.crud.event_crud import event_crud
    from app.crud.registration_crud import registration_crud
    from app.models.registration import Registration
    from app.services.notification_service import NotificationFactory, NotificationType
    from app.services.email_service import email_service

    # 1. Verify event is published
    event = await event_crud.get_with_details(db, data.event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    if event.status != "published":
        raise HTTPException(status_code=400, detail="Event is not available for registration")

    # 2 & 3. Lock the ticket_type row (SELECT FOR UPDATE) and validate
    ticket_type = await registration_crud.select_for_update(db, data.ticket_type_id)
    if not ticket_type or ticket_type.event_id != event.id:
        raise HTTPException(status_code=404, detail="Ticket type not found for this event")

    if not ticket_type.is_active:
        raise HTTPException(status_code=400, detail="Ticket type is not active")

    if ticket_type.sale_ends_at and ticket_type.sale_ends_at < datetime.now(timezone.utc):
        raise HTTPException(status_code=400, detail="Ticket sales have ended")

    # 4. Check availability
    if ticket_type.quantity_sold + data.quantity > ticket_type.quantity_total:
        raise HTTPException(status_code=409, detail="Sold out")

    # 5. Validate payment if ticket has a price
    total_amount = float(ticket_type.price) * data.quantity
    payment_ref = None

    if ticket_type.price > 0:
        if not data.payment:
            raise HTTPException(status_code=422, detail="Payment information required")
        if not luhn_check(data.payment.card_number):
            raise HTTPException(status_code=422, detail="Invalid card number")
        # Mock approval — always succeeds after Luhn passes
        payment_ref = "MOCK-" + secrets.token_hex(4).upper()

    # 6. Create registration row
    qr_token = secrets.token_urlsafe(32)
    registration = Registration(
        attendee_id=current_user.id,
        event_id=event.id,
        ticket_type_id=ticket_type.id,
        status="confirmed",
        quantity=data.quantity,
        total_amount=total_amount,
        payment_ref=payment_ref,
        qr_token=qr_token,
    )
    db.add(registration)

    # 7. Increment quantity_sold
    ticket_type.quantity_sold += data.quantity
    db.add(ticket_type)

    await db.commit()
    await db.refresh(registration)

    # Load relationships for the response
    reg_with_details = await registration_crud.get_with_details(db, registration.id)

    # 8. Fire-and-forget confirmation email
    if reg_with_details and reg_with_details.attendee:
        notif = NotificationFactory.create(
            NotificationType.REGISTRATION_CONFIRMATION,
            user=reg_with_details.attendee,
            registration=reg_with_details,
            event=event,
        )
        asyncio.create_task(email_service.send(notif))

    return reg_with_details


async def cancel_registration(
    db: AsyncSession,
    registration_id: UUID,
    current_user: User,
):
    """Cancel a registration — enforces 24h rule and decrements sold count."""
    from app.crud.registration_crud import registration_crud
    from app.services.notification_service import NotificationFactory, NotificationType
    from app.services.email_service import email_service

    reg = await registration_crud.get_with_details(db, registration_id)
    if not reg:
        raise HTTPException(status_code=404, detail="Registration not found")

    if reg.attendee_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not your registration")

    if reg.status == "cancelled":
        raise HTTPException(status_code=400, detail="Already cancelled")

    # Enforce 24h cancellation window
    event = reg.event
    if event and event.start_at:
        delta = event.start_at - datetime.now(timezone.utc)
        if delta.total_seconds() < 86400:  # 24 hours
            raise HTTPException(
                status_code=400,
                detail="Too close to event start — cancellations must be made at least 24 hours before",
            )

    # Decrement sold count
    ticket_type = reg.ticket_type
    if ticket_type:
        ticket_type.quantity_sold = max(0, ticket_type.quantity_sold - reg.quantity)
        db.add(ticket_type)

    reg.status = "cancelled"
    db.add(reg)
    await db.commit()

    # Fire-and-forget cancellation email
    if reg.attendee and event:
        notif = NotificationFactory.create(
            NotificationType.REGISTRATION_CANCELLATION,
            user=reg.attendee,
            registration=reg,
            event=event,
        )
        asyncio.create_task(email_service.send(notif))

    return reg
