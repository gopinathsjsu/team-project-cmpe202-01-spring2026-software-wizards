"""
Test fixtures: in-memory SQLite async DB, TestClient, and auth tokens for each role.
"""
import asyncio
import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.main import app
from app.database import Base, get_db
from app.models.user import User
from app.models.category import Category
from app.services.auth_service import auth_service
from datetime import datetime, timezone

TEST_DB_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def test_engine():
    engine = create_async_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def db(test_engine):
    session_factory = async_sessionmaker(test_engine, expire_on_commit=False)
    async with session_factory() as session:
        yield session
        await session.rollback()


@pytest_asyncio.fixture(scope="function")
async def client(db: AsyncSession):
    async def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()


async def _create_user(db: AsyncSession, email: str, role: str) -> tuple[User, str]:
    user = User(
        email=email,
        password_hash=auth_service.hash_password("Passw0rd!"),
        first_name="Test",
        last_name=role.capitalize(),
        role=role,
        is_active=True,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    token = auth_service.create_access_token(user.id, user.role)
    return user, token


@pytest_asyncio.fixture
async def attendee_token(db):
    _, token = await _create_user(db, "attendee@test.com", "attendee")
    return token


@pytest_asyncio.fixture
async def organizer_token(db):
    _, token = await _create_user(db, "organizer@test.com", "organizer")
    return token


@pytest_asyncio.fixture
async def organizer_user(db):
    user, _ = await _create_user(db, "org2@test.com", "organizer")
    return user


@pytest_asyncio.fixture
async def admin_token(db):
    _, token = await _create_user(db, "admin@test.com", "admin")
    return token


@pytest_asyncio.fixture
async def category(db):
    cat = Category(
        name="Technology",
        slug="technology",
        icon="💻",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    db.add(cat)
    await db.commit()
    await db.refresh(cat)
    return cat
