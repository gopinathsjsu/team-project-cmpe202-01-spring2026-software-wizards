import pytest
from datetime import datetime, timedelta, timezone


def future_dt(days=10):
    return (datetime.now(timezone.utc) + timedelta(days=days)).isoformat()


EVENT_PAYLOAD = {
    "title": "Test Event",
    "description": "A test event description for testing purposes.",
    "start_at": future_dt(10),
    "end_at": future_dt(10),
    "timezone": "UTC",
    "city": "Austin",
    "capacity": 100,
    "is_virtual": False,
}


@pytest.mark.asyncio
async def test_create_event_as_organizer(client, organizer_token, category):
    payload = {**EVENT_PAYLOAD, "category_id": str(category.id)}
    resp = await client.post(
        "/api/v1/events",
        json=payload,
        headers={"Authorization": f"Bearer {organizer_token}"},
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["title"] == "Test Event"
    assert data["status"] == "draft"


@pytest.mark.asyncio
async def test_create_event_as_attendee_forbidden(client, attendee_token):
    resp = await client.post(
        "/api/v1/events",
        json=EVENT_PAYLOAD,
        headers={"Authorization": f"Bearer {attendee_token}"},
    )
    assert resp.status_code == 403


@pytest.mark.asyncio
async def test_list_events_public(client):
    resp = await client.get("/api/v1/events")
    assert resp.status_code == 200
    data = resp.json()
    assert "items" in data
    assert "total" in data


@pytest.mark.asyncio
async def test_get_event_not_found(client):
    import uuid
    resp = await client.get(f"/api/v1/events/{uuid.uuid4()}")
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_event_submit_flow(client, organizer_token, category):
    # Create event
    payload = {**EVENT_PAYLOAD, "category_id": str(category.id)}
    create_resp = await client.post(
        "/api/v1/events",
        json=payload,
        headers={"Authorization": f"Bearer {organizer_token}"},
    )
    event_id = create_resp.json()["id"]

    # Add ticket type
    await client.post(
        f"/api/v1/events/{event_id}/tickets",
        json={"name": "General", "price": 0.0, "quantity_total": 50},
        headers={"Authorization": f"Bearer {organizer_token}"},
    )

    # Submit for review
    submit_resp = await client.post(
        f"/api/v1/events/{event_id}/submit",
        headers={"Authorization": f"Bearer {organizer_token}"},
    )
    assert submit_resp.status_code == 200
    assert submit_resp.json()["status"] == "pending"


@pytest.mark.asyncio
async def test_submit_without_tickets_fails(client, organizer_token):
    create_resp = await client.post(
        "/api/v1/events",
        json=EVENT_PAYLOAD,
        headers={"Authorization": f"Bearer {organizer_token}"},
    )
    event_id = create_resp.json()["id"]

    submit_resp = await client.post(
        f"/api/v1/events/{event_id}/submit",
        headers={"Authorization": f"Bearer {organizer_token}"},
    )
    assert submit_resp.status_code == 400


@pytest.mark.asyncio
async def test_admin_approve_event(client, organizer_token, admin_token, category):
    # Create and submit event
    payload = {**EVENT_PAYLOAD, "category_id": str(category.id)}
    create_resp = await client.post(
        "/api/v1/events", json=payload,
        headers={"Authorization": f"Bearer {organizer_token}"},
    )
    event_id = create_resp.json()["id"]
    await client.post(
        f"/api/v1/events/{event_id}/tickets",
        json={"name": "GA", "price": 0, "quantity_total": 50},
        headers={"Authorization": f"Bearer {organizer_token}"},
    )
    await client.post(
        f"/api/v1/events/{event_id}/submit",
        headers={"Authorization": f"Bearer {organizer_token}"},
    )
    # Admin approves
    approve_resp = await client.put(
        f"/api/v1/admin/events/{event_id}/approve",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert approve_resp.status_code == 200
    assert approve_resp.json()["status"] == "published"