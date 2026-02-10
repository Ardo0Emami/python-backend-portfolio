from __future__ import annotations
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr


# ---------- Base Schemas ---------- #
class CustomerBase(BaseModel):
    name: str
    email: Optional[EmailStr]
    phone: Optional[str] = None
    address: Optional[str] = None


class CustomerCreate(CustomerBase):
    pass


class CustomerRead(CustomerBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
