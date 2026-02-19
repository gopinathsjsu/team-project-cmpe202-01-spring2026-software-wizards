"""
Singleton Pattern — engine and AsyncSessionLocal are module-level singletons.
One engine is created at import time; sessions are yielded per request via get_db().
"""
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from typing import AsyncGenerator

from app.config import get_settings

settings = get_settings()

# Single engine instance (Singleton)
engine = create_async_engine(
    settings.DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    echo=(settings.ENVIRONMENT == "development"),
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession,
)


class Base(DeclarativeBase):
    pass


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency Injection: yields a database session per request."""
    async with AsyncSessionLocal() as session:
        yield session
