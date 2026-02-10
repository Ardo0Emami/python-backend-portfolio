"""
One-off data seeding script.

This script demonstrates the intended usage of `session_scope`,
which provides explicit transaction control outside the HTTP
request lifecycle.

Run with:
    python -m accounting_api.scripts.seed_demo_data
"""

from accounting_api.app.core.db_adapter import SessionLocal
from accounting_api.app.core.db_infrastructure import session_scope
from accounting_api.app.models.sqlalchemy_models import (
    Customer,
    Invoice,
    LineItem
)
from accounting_api.app.models.sqlalchemy_models import InvoiceStatus


def seed_demo_data() -> None:
    """
    Seed a small set of demo data into the database.

    This function intentionally uses `session_scope` instead of FastAPI's
    `get_db` dependency, because:
    - It runs outside the web application
    - There is no request lifecycle
    - We want explicit, script-level transaction control
    """
    with session_scope(SessionLocal) as db:
        customer = Customer(
            name="Demo Customer",
            email="demo@example.com",
        )
        db.add(customer)
        db.flush()  # ensure customer.id is available

        invoice = Invoice(
            customer_id=customer.id,
            status=InvoiceStatus.issued,
        )
        db.add(invoice)
        db.flush()

        items = [
            LineItem(
                invoice_id=invoice.id,
                description="Consulting services",
                quantity=10,
                unit_price=150.00,
            ),
            LineItem(
                invoice_id=invoice.id,
                description="Support services",
                quantity=5,
                unit_price=80.00,
            ),
        ]

        db.add_all(items)

        # No explicit commit needed here:
        # `session_scope` will commit if no exception is raised.


def main() -> None:
    seed_demo_data()
    print("Demo data successfully seeded.")


if __name__ == "__main__":
    main()
