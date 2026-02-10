
import pytest
from sqlalchemy.orm import Session
from accounting_api.app.repositories.customer import CustomerRepository
from accounting_api.app.repositories.invoice import InvoiceRepository


def test_customer_and_invoice_repositories(test_db_session: Session):
    customers = CustomerRepository(test_db_session)
    invoices = InvoiceRepository(test_db_session)

    c = customers.add("ardo0", "it.arghavanemami@gmail.com")
    assert c.id is not None

    inv = invoices.create(c.id)
    invoices.add_line_item(inv.id, "a", 2, float(10))
    invoices.add_line_item(inv.id, "b", 1, float(15))

    assert inv.total_amount == pytest.approx(35)
    assert len(invoices.list_by_customer(c.id)) == 1

    invoices.delete(inv.id)
    assert invoices.get(inv.id) is None
    customers.delete(c.id)
    assert customers.get(c.id) is None
