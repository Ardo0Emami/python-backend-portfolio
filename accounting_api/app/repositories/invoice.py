from __future__ import annotations
from decimal import Decimal
from typing import List, Optional
from sqlalchemy.orm import Session

from accounting_api.app.models.sqlalchemy_models import (
    Invoice,
    LineItem,
    InvoiceStatus
)


class InvoiceRepository:
    """Repository for Invoice and LineItem operations."""

    def __init__(self, db: Session):
        self.db = db

    # --- CREATE ---
    def create(self,
               customer_id: int,
               status: InvoiceStatus = InvoiceStatus.draft
               ) -> Invoice:
        invoice = Invoice(customer_id=customer_id, status=status)
        self.db.add(invoice)
        self.db.flush()
        return invoice

    # --- READ ---
    def get(self, invoice_id: int) -> Optional[Invoice]:
        return self.db.get(Invoice, invoice_id)

    def list_by_customer(self, customer_id: int) -> List[Invoice]:
        return list(
            self.db.query(Invoice)
            .filter(Invoice.customer_id == customer_id)
            .order_by(Invoice.id.asc())
        )

    # --- UPDATE ---
    def update_status(self, invoice_id: int, status: InvoiceStatus) -> bool:
        invoice = self.get(invoice_id)
        if not invoice:
            return False
        invoice.status = status
        self.db.flush()
        return True

    # --- DELETE ---
    def delete(self, invoice_id: int) -> bool:
        invoice = self.get(invoice_id)
        if not invoice:
            return False
        self.db.delete(invoice)
        self.db.flush()
        return True

    # --- LINE ITEMS ---
    def add_line_item(
        self,
        invoice_id: int,
        description: str,
        quantity: int,
        unit_price: float | Decimal
    ) -> LineItem:
        line = LineItem(
            invoice_id=invoice_id,
            description=description,
            quantity=quantity,
            unit_price=unit_price,
        )
        self.db.add(line)
        self.db.flush()
        return line

    def list_line_items(self, invoice_id: int) -> List[LineItem]:
        return list(
            self.db.query(LineItem)
            .filter(LineItem.invoice_id == invoice_id)
            .order_by(LineItem.id.asc())
        )

    def delete_line_item(self, line_item_id: int) -> bool:
        line = self.db.get(LineItem, line_item_id)
        if not line:
            return False
        self.db.delete(line)
        self.db.flush()
        return True
