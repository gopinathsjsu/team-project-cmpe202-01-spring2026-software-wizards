"""
EventHub API — main application factory.

Patterns active here:
- Singleton: settings and engine created once
- Observer: event_subject subscribers registered at startup
- Dependency Injection: all routers use FastAPI Depends()
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.services.event_service import (
    event_subject,
    AttendeeNotificationObserver,
    OrganizerNotificationObserver,
    send_reminders,
)

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # ── Startup ───────────────────────────────────────────────
    # Observer Pattern: register subscribers
    event_subject.subscribe(AttendeeNotificationObserver())
    event_subject.subscribe(OrganizerNotificationObserver())

    # APScheduler: send 48h reminder emails every 5 minutes
    from apscheduler.schedulers.asyncio import AsyncIOScheduler
    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_reminders, "interval", minutes=5, id="send_reminders")
    scheduler.start()

    yield

    # ── Shutdown ──────────────────────────────────────────────
    scheduler.shutdown(wait=False)


def create_app() -> FastAPI:
    app = FastAPI(
        title="EventHub API",
        description="Eventbrite-like event management & ticketing platform",
        version="1.0.0",
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # CORS — allow local React dev server
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:5173",
            "http://localhost:3000",
            settings.FRONTEND_URL,
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Mount all routers under /api/v1
    from app.routers import auth, users, events, categories, tickets, registrations, admin

    prefix = "/api/v1"
    app.include_router(auth.router, prefix=prefix)
    app.include_router(users.router, prefix=prefix)
    app.include_router(events.router, prefix=prefix)
    app.include_router(categories.router, prefix=prefix)
    app.include_router(tickets.router, prefix=prefix)
    app.include_router(registrations.router, prefix=prefix)
    app.include_router(admin.router, prefix=prefix)

    # Health check also at root level for convenience
    @app.get("/api/v1/health", include_in_schema=False)
    async def health():
        from datetime import datetime, timezone
        return {"status": "ok", "timestamp": datetime.now(timezone.utc).isoformat()}

    return app


app = create_app()
