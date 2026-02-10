from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional

from sqlalchemy import (DateTime, Enum as SAEnum,
                        ForeignKey, Integer, Numeric,
                        String, func, select)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.hybrid import hybrid_property


# ----------Base---------- #
class Base(DeclarativeBase):
    pass


# ---------- Enums ---------- #
class InvoiceStatus(str, Enum):
    draft = "draft"
    issued = "issued"
    paid = "paid"


# ---------- Entities ---------- #
class Customer(Base):
    __tablename__ = "customer"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    email: Mapped[Optional[str]] = mapped_column(String(320))
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )

    invoices: Mapped[list["Invoice"]] = relationship(
        back_populates="customer",
        cascade="all, delete-orphan",
        passive_deletes=True
    )

    def __repr__(self) -> str:
        return f"<Customer id={self.id} name={self.name!r}>"


class Invoice(Base):
    __tablename__ = "invoice"

    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(
        ForeignKey("customer.id", ondelete="CASCADE"),
        nullable=False
    )
    status: Mapped[InvoiceStatus] = mapped_column(
        SAEnum(InvoiceStatus),
        default=InvoiceStatus.draft,
        nullable=False
    )
    issued_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    customer: Mapped[Customer] = relationship(back_populates="invoices")
    line_items: Mapped[list[LineItem]] = relationship(
        back_populates="invoice",
        cascade="all, delete-orphan",
        passive_deletes=True
    )

    @hybrid_property
    def total_amount(self) -> float:
        return float(
            sum(li.quantity * li.unit_price for li in self.line_items)
            )

    @total_amount.expression
    def total_amount(cls):
        return (
            select(
                func.coalesce(
                    func.sum(LineItem.quantity * LineItem.unit_price), 0
                            )
                    )
            .where(LineItem.invoice_id == cls.id)
            .correlate(cls.__tablename__)
            .scalar_subquery()
        )


class LineItem(Base):
    __tablename__ = "line_item"

    id: Mapped[int] = mapped_column(primary_key=True)
    invoice_id: Mapped[int] = mapped_column(
        ForeignKey("invoice.id", ondelete="CASCADE"), nullable=False
    )
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)

    invoice: Mapped[Invoice] = relationship(back_populates="line_items")

    def __repr__(self) -> str:
        return f"<LineItem id = {self.id} qty={self.quantity} price={self.unit_price}>"
