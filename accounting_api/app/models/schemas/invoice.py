from __future__ import annotations

from datetime import datetime
from typing import Annotated, List, Optional

from pydantic import BaseModel, ConfigDict, Field

from accounting_api.app.models.sqlalchemy_models import InvoiceStatus


# ---------- LineItem Schemas ---------- #
class LineItemCreate(BaseModel):
    description: str
    quantity: Annotated[int, Field(gt=0)]
    unit_price: Annotated[float, Field(gt=0)]


class LineItemRead(BaseModel):
    id: int
    description: str
    quantity: int
    unit_price: float

    model_config = ConfigDict(from_attributes=True)


# ---------- Invoice Schemas ---------- #
class InvoiceCreate(BaseModel):
    customer_id: int


class InvoiceRead(BaseModel):
    id: int
    customer_id: int
    status: InvoiceStatus
    issued_at: Optional[datetime] = None

    # Derived field from ORM hybrid_property
    total_amount: float

    # Nested relationship from ORM
    line_items: List[LineItemRead] = []

    model_config = ConfigDict(from_attributes=True)
