"""Drop all tables and re-seed. Run: python scripts/reset_db.py"""
import asyncio
import sys
sys.path.insert(0, ".")


async def reset():
    from app.database import engine, Base
    from app.models import *  # noqa

    print("Dropping all tables...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    print("Recreating tables...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Re-seeding...")

    from scripts.seed import seed
    await seed()


if __name__ == "__main__":
    asyncio.run(reset())
