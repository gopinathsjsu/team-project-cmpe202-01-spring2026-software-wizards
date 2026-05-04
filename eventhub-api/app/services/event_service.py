"""
Strategy Pattern — EventSortStrategy defines interchangeable sort algorithms.
Observer Pattern — EventStatusSubject notifies observers on status changes.
"""
import asyncio
from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.event import Event
from app.models.registration import Registration


# Strategy Pattern: Sort strategies for event listing

class EventSortStrategy(ABC):
    """Abstract sort strategy interface."""
    @abstractmethod
    def apply(self, query) -> any: ...


class SortByDate(EventSortStrategy):
    """Sort events by start date ascending (soonest first)."""
    def apply(self, query):
        return query.order_by(Event.start_at.asc())


class SortByPopularity(EventSortStrategy):
    """Sort events by confirmed registration count descending."""
    def apply(self, query):
        subq = (
            select(func.count(Registration.id))
            .where(
                Registration.event_id == Event.id,
                Registration.status == "confirmed",
            )
            .scalar_subquery()
        )
        return query.order_by(subq.desc())


class SortByRecent(EventSortStrategy):
    """Sort events by creation date descending (newest listings first)."""
    def apply(self, query):
        return query.order_by(Event.created_at.desc())


# Registry of available sort strategies (used by EventCRUD)
SORT_STRATEGIES: Dict[str, EventSortStrategy] = {
    "date":       SortByDate(),
    "popularity": SortByPopularity(),
    "recent":     SortByRecent(),
}


# Observer Pattern: Event status change notifications

class EventStatusObserver(ABC):
    """Abstract observer that reacts to event status changes."""
    @abstractmethod
    async def on_status_change(self, event: Event, old_status: str, new_status: str): ...


class AttendeeNotificationObserver(EventStatusObserver):
    """Emails all confirmed registrants when an event is cancelled."""
    async def on_status_change(self, event: Event, old_status: str, new_status: str):
        if new_status == "cancelled":
            from app.crud.registration_crud import registration_crud
            from app.services.notification_service import NotificationFactory, NotificationType
            from app.services.email_service import email_service
            from app.database import AsyncSessionLocal

            async with AsyncSessionLocal() as db:
                registrations = await registration_crud.get_confirmed(db, event.id)
                for reg in registrations:
                    if reg.attendee:
                        notif = NotificationFactory.create(
                            NotificationType.EVENT_CANCELLATION,
                            user=reg.attendee,
                            event=event,
                        )
                        await email_service.send(notif)


class OrganizerNotificationObserver(EventStatusObserver):
    """Emails the organizer when their event is approved or rejected."""
    async def on_status_change(self, event: Event, old_status: str, new_status: str):
        if new_status in ("published", "rejected"):
            from app.services.notification_service import NotificationFactory, NotificationType
            from app.services.email_service import email_service

            ntype = (
                NotificationType.EVENT_APPROVED
                if new_status == "published"
                else NotificationType.EVENT_REJECTED
            )
            kwargs = {"user": event.organizer, "event": event}
            if new_status == "rejected":
                kwargs["reason"] = event.rejection_reason or ""
            notif = NotificationFactory.create(ntype, **kwargs)
            asyncio.create_task(email_service.send(notif))


class EventStatusSubject:
    """
    Observer Pattern subject — maintains a list of observers.
    Called by update_event_status() whenever the status changes.
    """
    def __init__(self):
        self._observers: List[EventStatusObserver] = []

    def subscribe(self, obs: EventStatusObserver):
        self._observers.append(obs)

    async def notify(self, event: Event, old_status: str, new_status: str):
        for obs in self._observers:
            await obs.on_status_change(event, old_status, new_status)


# Module-level subject instance (initialized in main.py lifespan)
event_subject = EventStatusSubject()


# Geocoding (address → lat/lng via Nominatim)

async def geocode_address(address: str) -> Optional[tuple[float, float]]:
    """Call Nominatim to convert address to coordinates. Returns (lat, lon) or None."""
    import httpx
    url = "https://nominatim.openstreetmap.org/search"
    params = {"q": address, "format": "json", "limit": 1}
    headers = {"User-Agent": "eventhub/1.0"}
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.get(url, params=params, headers=headers)
            data = resp.json()
        if data:
            return float(data[0]["lat"]), float(data[0]["lon"])
    except Exception:
        pass
    return None

# APScheduler job: send 48h reminders

async def send_reminders():
    """
    Called every 5 minutes by APScheduler.
    Finds events starting in 47–49 hours and sends reminder emails to confirmed attendees.
    """
    from app.crud.event_crud import event_crud
    from app.crud.registration_crud import registration_crud
    from app.services.notification_service import NotificationFactory, NotificationType
    from app.services.email_service import email_service
    from app.database import AsyncSessionLocal

    async with AsyncSessionLocal() as db:
        events = await event_crud.get_upcoming_for_reminder(db)
        for event in events:
            registrations = await registration_crud.get_unreminded(db, event.id)
            for reg in registrations:
                if reg.attendee:
                    notif = NotificationFactory.create(
                        NotificationType.EVENT_REMINDER,
                        user=reg.attendee,
                        event=event,
                    )
                    asyncio.create_task(email_service.send(notif))
                    reg.reminder_sent = True
                    db.add(reg)
            await db.commit()