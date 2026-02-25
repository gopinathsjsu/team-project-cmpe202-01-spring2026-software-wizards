import uuid
from typing import Optional
from pydantic import BaseModel


class CategoryCreate(BaseModel):
    name: str
    slug: str
    icon: Optional[str] = None


class CategoryRead(BaseModel):
    id: uuid.UUID
    name: str
    slug: str
    icon: Optional[str] = None

    model_config = {"from_attributes": True}