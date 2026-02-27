import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class TicketTypeCreate(BaseModel):
    name: str
    price: float = 0.00
    quantity_total: int
    is_active: bool = True
    sale_ends_at: Optional[datetime] = None


class TicketTypeRead(BaseModel):
    id: uuid.UUID
    event_id: uuid.UUID
    name: str
    price: float
    quantity_total: int
    quantity_sold: int
    quantity_available: int
    is_active: bool
    sale_ends_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class TicketTypeUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    quantity_total: Optional[int] = None
    is_active: Optional[bool] = None
    sale_ends_at: Optional[datetime] = None
