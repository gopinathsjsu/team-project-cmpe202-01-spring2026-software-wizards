import pytest
from datetime import datetime, timedelta, timezone

from app.models.user import User
from app.models.category import Category
from app.models.event import Event
from app.models.ticket_type import TicketType
from app.services.registration_service import luhn_check


def future_dt(days=10):
    return datetime.now(timezone.utc) + timedelta(days=days)


@pytest.mark.asyncio
async def test_luhn_valid():
    assert luhn_check("4242424242424242") is True


@pytest.mark.asyncio
async def test_luhn_invalid():
    assert luhn_check("1234567890123456") is False


async def _setup_published_event(db, organizer_user, category):
    """Helper to create a published event with a free ticket."""
    event = Event(
        organizer_id=organizer_user.id,
        category_id=category.id,
        title="Test Registration Event",
        description="For testing registration flow.",
        status="published",
        start_at=future_dt(10),
        end_at=future_dt(10),
        timezone="UTC",
        city="Austin",
        capacity=100,
        is_virtual=False,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    db.add(event)
    await db.commit()
    await db.refresh(event)

    ticket = TicketType(
        event_id=event.id,
        name="General Admission",
        price=0.00,
        quantity_total=50,
        quantity_sold=0,
        is_active=True,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    db.add(ticket)
    await db.commit()
    await db.refresh(ticket)
    return event, ticket


@pytest.mark.asyncio
async def test_register_free_ticket(client, db, attendee_token, organizer_user, category):
    event, ticket = await _setup_published_event(db, organizer_user, category)

    resp = await client.post(
        "/api/v1/registrations",
        json={
            "event_id": str(event.id),
            "ticket_type_id": str(ticket.id),
            "quantity": 1,
        },
        headers={"Authorization": f"Bearer {attendee_token}"},
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["status"] == "confirmed"
    assert "qr_token" in data


@pytest.mark.asyncio
async def test_register_paid_ticket_valid_card(client, db, attendee_token, organizer_user, category):
    event = Event(
        organizer_id=organizer_user.id,
        category_id=category.id,
        title="Paid Event",
        description="Paid event test.",
        status="published",
        start_at=future_dt(10),
        end_at=future_dt(10),
        timezone="UTC",
        city="Austin",
        capacity=100,
        is_virtual=False,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    db.add(event)
    await db.commit()
    await db.refresh(event)

    ticket = TicketType(
        event_id=event.id,
        name="VIP",
        price=25.00,
        quantity_total=50,
        quantity_sold=0,
        is_active=True,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    db.add(ticket)
    await db.commit()
    await db.refresh(ticket)

    resp = await client.post(
        "/api/v1/registrations",
        json={
            "event_id": str(event.id),
            "ticket_type_id": str(ticket.id),
            "quantity": 2,
            "payment": {
                "card_number": "4242424242424242",
                "expiry_month": 12,
                "expiry_year": 2028,
                "cvv": "123",
            },
        },
        headers={"Authorization": f"Bearer {attendee_token}"},
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["total_amount"] == 50.0
    assert data["payment_ref"].startswith("MOCK-")


@pytest.mark.asyncio
async def test_register_invalid_card(client, db, attendee_token, organizer_user, category):
    event = Event(
        organizer_id=organizer_user.id,
        category_id=category.id,
        title="Paid Event 2",
        description="Paid event test 2.",
        status="published",
        start_at=future_dt(10),
        end_at=future_dt(10),
        timezone="UTC",
        city="Austin",
        capacity=100,
        is_virtual=False,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    db.add(event)
    await db.commit()
    await db.refresh(event)

    ticket = TicketType(
        event_id=event.id,
        name="VIP",
        price=25.00,
        quantity_total=50,
        quantity_sold=0,
        is_active=True,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    db.add(ticket)
    await db.commit()
    await db.refresh(ticket)

    resp = await client.post(
        "/api/v1/registrations",
        json={
            "event_id": str(event.id),
            "ticket_type_id": str(ticket.id),
            "quantity": 1,
            "payment": {
                "card_number": "1234567890123456",
                "expiry_month": 12,
                "expiry_year": 2028,
                "cvv": "123",
            },
        },
        headers={"Authorization": f"Bearer {attendee_token}"},
    )
    assert resp.status_code == 422


@pytest.mark.asyncio
async def test_list_my_registrations(client, db, attendee_token, organizer_user, category):
    event, ticket = await _setup_published_event(db, organizer_user, category)
    await client.post(
        "/api/v1/registrations",
        json={"event_id": str(event.id), "ticket_type_id": str(ticket.id), "quantity": 1},
        headers={"Authorization": f"Bearer {attendee_token}"},
    )
    resp = await client.get(
        "/api/v1/registrations",
        headers={"Authorization": f"Bearer {attendee_token}"},
    )
    assert resp.status_code == 200
    assert resp.json()["total"] >= 1
