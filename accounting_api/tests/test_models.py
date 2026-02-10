from __future__ import annotations

import math
# from typing import Any, Generator
# import pytest
from sqlalchemy.orm import Session

from accounting_api.app.models.sqlalchemy_models import (
    # Base,
    Customer,
    Invoice,
    LineItem,
    InvoiceStatus,
)


def test_create_customer(test_db_session: Session):
    c = Customer(name="Alice", email="alice@example.com")
    test_db_session.add(c)
    test_db_session.flush()

    assert c.id is not None
    assert isinstance(c.created_at, type(c.created_at))
    assert test_db_session.query(Customer).count() == 1


def test_invoice_line_items_relationship(test_db_session: Session):
    # Create Customer
    c = Customer(name="Bob", email="bob@example.com")
    test_db_session.add(c)
    test_db_session.flush()

    # Create Invoice
    inv = Invoice(customer_id=c.id, status=InvoiceStatus.draft)
    test_db_session.add(inv)
    test_db_session.flush()

    # Add LineItems
    li1 = LineItem(
        invoice_id=inv.id,
        description="Apples",
        quantity=2,
        unit_price=3.50
        )
    li2 = LineItem(
        invoice_id=inv.id,
        description="Oranges",
        quantity=3,
        unit_price=4.00
        )
    test_db_session.add_all([li1, li2])
    test_db_session.flush()

    # Validate relationships
    assert len(inv.line_items) == 2
    assert inv.customer.id == c.id
    assert math.isclose(inv.total_amount, 2 * 3.5 + 3 * 4.0, rel_tol=1e-9)

    # Ensure bidirectional relationship works
    assert li1.invoice == inv


def test_cascade_delete_invoice_removes_line_items(test_db_session: Session):
    c = Customer(name="Carol", email="carol@example.com")
    inv = Invoice(customer=c)
    inv.line_items = [
        LineItem(description="A", quantity=1, unit_price=10),
        LineItem(description="B", quantity=2, unit_price=5),
    ]
    test_db_session.add(inv)
    test_db_session.flush()

    # delete invoice, should cascade to line_items
    test_db_session.delete(inv)
    test_db_session.flush()

    assert test_db_session.query(LineItem).count() == 0


def test_cascade_delete_customer_removes_invoices(test_db_session: Session):
    c = Customer(name="Dave", email="dave@example.com")
    inv = Invoice(customer=c)
    test_db_session.add(inv)
    test_db_session.flush()

    # delete customer, should cascade to invoice
    test_db_session.delete(c)
    test_db_session.flush()

    assert test_db_session.query(Invoice).count() == 0
