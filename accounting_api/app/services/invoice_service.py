from sqlalchemy.orm import Session

from accounting_api.app.services.errors import (
    InvalidOperationError,
    NotFoundError
)
from accounting_api.app.models.sqlalchemy_models import InvoiceStatus
from accounting_api.app.repositories.invoice import InvoiceRepository


class InvoiceService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = InvoiceRepository(db)

    def create_invoice(self, customer_id: int):
        invoice = self.repo.create(customer_id)
        return invoice

    def get_invoice(self, invoice_id: int):
        invoice = self.repo.get(invoice_id)
        if not invoice:
            raise NotFoundError(f"Invoice with ID {invoice_id} not found.")
        return invoice

    def delete_invoice(self, invoice_id: int) -> bool:
        deleted = self.repo.delete(invoice_id)
        return deleted

    def add_line_item(
        self,
        invoice_id: int,
        description: str,
        quantity: int,
        unit_price: float,
    ):
        lineItem = self.repo.add_line_item(
            invoice_id=invoice_id,
            description=description,
            quantity=quantity,
            unit_price=unit_price,
        )
        return lineItem

    def issue_invoice(self, invoice_id: int):
        invoice = self.get_invoice(invoice_id)
        if invoice.status != InvoiceStatus.draft:
            raise InvalidOperationError(
                f"Cannot issue invoice with status {invoice.status}."
            )
        invoice.status = InvoiceStatus.issued
        return invoice
