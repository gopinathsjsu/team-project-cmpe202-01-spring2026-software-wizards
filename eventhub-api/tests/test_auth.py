import pytest


@pytest.mark.asyncio
async def test_register_success(client):
    resp = await client.post("/api/v1/auth/register", json={
        "email": "newuser@test.com",
        "password": "Passw0rd!",
        "first_name": "New",
        "last_name": "User",
        "role": "attendee",
    })
    assert resp.status_code == 201
    data = resp.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["user"]["email"] == "newuser@test.com"
    assert data["user"]["role"] == "attendee"


@pytest.mark.asyncio
async def test_register_duplicate_email(client):
    payload = {
        "email": "dup@test.com",
        "password": "Passw0rd!",
        "first_name": "A",
        "last_name": "B",
        "role": "attendee",
    }
    await client.post("/api/v1/auth/register", json=payload)
    resp = await client.post("/api/v1/auth/register", json=payload)
    assert resp.status_code == 409


@pytest.mark.asyncio
async def test_register_admin_role_rejected(client):
    resp = await client.post("/api/v1/auth/register", json={
        "email": "badmin@test.com",
        "password": "Passw0rd!",
        "first_name": "A",
        "last_name": "B",
        "role": "admin",
    })
    assert resp.status_code == 422


@pytest.mark.asyncio
async def test_register_short_password(client):
    resp = await client.post("/api/v1/auth/register", json={
        "email": "short@test.com",
        "password": "abc",
        "first_name": "A",
        "last_name": "B",
        "role": "attendee",
    })
    assert resp.status_code == 422


@pytest.mark.asyncio
async def test_login_success(client):
    await client.post("/api/v1/auth/register", json={
        "email": "login@test.com",
        "password": "Passw0rd!",
        "first_name": "A",
        "last_name": "B",
        "role": "attendee",
    })
    resp = await client.post("/api/v1/auth/login", json={
        "email": "login@test.com",
        "password": "Passw0rd!",
    })
    assert resp.status_code == 200
    assert "access_token" in resp.json()


@pytest.mark.asyncio
async def test_login_wrong_password(client):
    await client.post("/api/v1/auth/register", json={
        "email": "wrongpw@test.com",
        "password": "Passw0rd!",
        "first_name": "A",
        "last_name": "B",
        "role": "attendee",
    })
    resp = await client.post("/api/v1/auth/login", json={
        "email": "wrongpw@test.com",
        "password": "wrongpassword",
    })
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_login_unknown_email(client):
    resp = await client.post("/api/v1/auth/login", json={
        "email": "nobody@test.com",
        "password": "Passw0rd!",
    })
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_refresh_token(client):
    reg = await client.post("/api/v1/auth/register", json={
        "email": "refresh@test.com",
        "password": "Passw0rd!",
        "first_name": "A",
        "last_name": "B",
        "role": "attendee",
    })
    refresh_token = reg.json()["refresh_token"]
    resp = await client.post("/api/v1/auth/refresh", json={"refresh_token": refresh_token})
    assert resp.status_code == 200
    assert "access_token" in resp.json()


@pytest.mark.asyncio
async def test_get_me(client, attendee_token):
    resp = await client.get(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {attendee_token}"},
    )
    assert resp.status_code == 200
    assert resp.json()["role"] == "attendee"


@pytest.mark.asyncio
async def test_me_unauthorized(client):
    resp = await client.get("/api/v1/users/me")
    assert resp.status_code == 401
