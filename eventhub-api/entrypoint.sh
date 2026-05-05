#!/bin/sh
set -e

echo "Running migrations..."
alembic upgrade head

echo "Seeding database if empty..."
python - <<'EOF'
import asyncio
from sqlalchemy import text
from app.database import AsyncSessionLocal

async def maybe_seed():
    async with AsyncSessionLocal() as db:
        result = await db.execute(text("SELECT COUNT(*) FROM users"))
        count = result.scalar()
    if count == 0:
        print("Database is empty — running seed...")
        import subprocess, sys
        subprocess.run([sys.executable, "scripts/seed.py"], check=True)
    else:
        print(f"Database already has {count} users — skipping seed.")

asyncio.run(maybe_seed())
EOF

echo "Starting server..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 2
