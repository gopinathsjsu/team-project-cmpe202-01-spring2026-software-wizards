import uuid
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

from app.schemas.category import CategoryRead
from app.schemas.ticket import TicketTypeRead
from app.schemas.user import UserPublic


class EventCreate(BaseModel):
    title: str
    description: str
    category_id: Optional[uuid.UUID] = None
    start_at: datetime
    end_at: datetime
    timezone: str = "UTC"
    venue_name: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    capacity: int = 100
    is_virtual: bool = False
    banner_url: Optional[str] = None
    tags: Optional[List[str]] = None


class EventUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category_id: Optional[uuid.UUID] = None
    start_at: Optional[datetime] = None
    end_at: Optional[datetime] = None
    timezone: Optional[str] = None
    venue_name: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    capacity: Optional[int] = None
    is_virtual: Optional[bool] = None
    banner_url: Optional[str] = None
    tags: Optional[List[str]] = None


class EventListItem(BaseModel):
    """Compact shape used in paginated event lists."""
    id: uuid.UUID
    title: str
    start_at: datetime
    city: Optional[str] = None
    banner_url: Optional[str] = None
    is_virtual: bool
    min_price: float = 0.0
    registration_count: int = 0
    category: Optional[CategoryRead] = None
    status: str

    model_config = {"from_attributes": True}


class EventRead(BaseModel):
    """Full event detail — includes nested organizer, tickets, and stats."""
    id: uuid.UUID
    title: str
    description: str
    status: str
    start_at: datetime
    end_at: datetime
    timezone: str
    venue_name: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    capacity: int
    is_virtual: bool
    banner_url: Optional[str] = None
    tags: Optional[List[str]] = None
    rejection_reason: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    organizer: Optional[UserPublic] = None
    category: Optional[CategoryRead] = None
    ticket_types: List[TicketTypeRead] = []
    registration_count: int = 0

    model_config = {"from_attributes": True}


class AttendeeRecord(BaseModel):
    """Row returned by GET /events/{id}/attendees."""
    attendee_id: uuid.UUID
    first_name: str
    last_name: str
    email: str
    ticket_name: str
    quantity: int
    total_amount: float
    status: str
    checked_in_at: Optional[datetime] = None
    registered_at: datetime

    model_config = {"from_attributes": True}


class EventSubmitResponse(BaseModel):
    id: uuid.UUID
    status: str
    message: str