import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class PaymentInfo(BaseModel):
    """Mock payment details — Luhn-validated but never processed."""
    card_number: str
    expiry_month: int
    expiry_year: int
    cvv: str


class RegistrationCreate(BaseModel):
    event_id: uuid.UUID
    ticket_type_id: uuid.UUID
    quantity: int = 1
    payment: Optional[PaymentInfo] = None


class RegistrationEventSummary(BaseModel):
    title: str
    start_at: datetime
    venue_name: Optional[str] = None

    model_config = {"from_attributes": True}


class RegistrationTicketSummary(BaseModel):
    name: str
    price: float

    model_config = {"from_attributes": True}


class RegistrationRead(BaseModel):
    id: uuid.UUID
    qr_token: str
    status: str
    quantity: int
    total_amount: float
    payment_ref: Optional[str] = None
    checked_in_at: Optional[datetime] = None
    created_at: datetime
    event: Optional[RegistrationEventSummary] = None
    ticket_type: Optional[RegistrationTicketSummary] = None

    model_config = {"from_attributes": True}
