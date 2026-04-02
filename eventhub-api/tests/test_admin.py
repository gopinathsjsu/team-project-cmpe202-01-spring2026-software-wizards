import pytest


@pytest.mark.asyncio
async def test_health_check(client):
    resp = await client.get("/api/v1/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


@pytest.mark.asyncio
async def test_admin_list_users(client, admin_token):
    resp = await client.get(
        "/api/v1/admin/users",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert resp.status_code == 200
    assert "items" in resp.json()


@pytest.mark.asyncio
async def test_admin_endpoint_requires_admin(client, attendee_token):
    resp = await client.get(
        "/api/v1/admin/users",
        headers={"Authorization": f"Bearer {attendee_token}"},
    )
    assert resp.status_code == 403


@pytest.mark.asyncio
async def test_list_pending_events_admin(client, admin_token):
    resp = await client.get(
        "/api/v1/admin/events?status=pending",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert resp.status_code == 200


@pytest.mark.asyncio
async def test_reject_event(client, organizer_token, admin_token, category):
    from datetime import datetime, timedelta, timezone
    future = (datetime.now(timezone.utc) + timedelta(days=10)).isoformat()
    create_resp = await client.post(
        "/api/v1/events",
        json={
            "title": "Reject Me",
            "description": "This event will be rejected.",
            "start_at": future,
            "end_at": future,
            "timezone": "UTC",
            "city": "Boston",
            "capacity": 50,
            "is_virtual": False,
        },
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
    reject_resp = await client.put(
        f"/api/v1/admin/events/{event_id}/reject?reason=Missing+required+details",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert reject_resp.status_code == 200
    assert reject_resp.json()["status"] == "rejected"
    assert "Missing" in reject_resp.json()["rejection_reason"]
