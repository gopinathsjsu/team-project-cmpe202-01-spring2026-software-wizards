"""
Calendar service — generates .ics files and Google/Outlook calendar links.
"""
from datetime import timezone as _utc
from urllib.parse import urlencode
from app.models.event import Event


def _as_utc(dt):
    """Return dt as UTC, handling both naive (assumed UTC) and aware datetimes."""
    if dt.tzinfo is None:
        return dt.replace(tzinfo=_utc.utc)
    return dt.astimezone(_utc.utc)


def build_google_link(event: Event) -> str:
    """Build a Google Calendar 'Add to Calendar' URL."""
    fmt = "%Y%m%dT%H%M%SZ"
    start = _as_utc(event.start_at).strftime(fmt)
    end = _as_utc(event.end_at).strftime(fmt)
    params = {
        "action": "TEMPLATE",
        "text": event.title,
        "dates": f"{start}/{end}",
        "details": (event.description or "")[:500],
        "location": event.address or event.venue_name or "",
    }
    return "https://calendar.google.com/calendar/render?" + urlencode(params)


def build_outlook_link(event: Event) -> str:
    """Build an Outlook Web 'Add to Calendar' URL."""
    params = {
        "subject": event.title,
        "startdt": _as_utc(event.start_at).isoformat(),
        "enddt": _as_utc(event.end_at).isoformat(),
        "body": (event.description or "")[:500],
        "location": event.address or event.venue_name or "",
    }
    return "https://outlook.live.com/calendar/0/deeplink/compose?" + urlencode(params)


def build_ics(event: Event) -> bytes:
    """Build an iCalendar .ics file for the event."""
    from icalendar import Calendar, Event as ICSEvent
    import uuid as uuidlib

    cal = Calendar()
    cal.add("prodid", "-//EventHub//EN")
    cal.add("version", "2.0")

    ics_event = ICSEvent()
    ics_event.add("uid", str(event.id))
    ics_event.add("summary", event.title)
    ics_event.add("description", event.description or "")
    ics_event.add("dtstart", event.start_at)
    ics_event.add("dtend", event.end_at)

    location_parts = [p for p in [event.venue_name, event.address] if p]
    ics_event.add("location", ", ".join(location_parts))

    cal.add_component(ics_event)
    return cal.to_ical()