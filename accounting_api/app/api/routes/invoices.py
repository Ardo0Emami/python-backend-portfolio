from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from accounting_api.app.api.dependencies.auth import get_api_key
from accounting_api.app.core.db_adapter import get_db
from accounting_api.app.models.schemas.invoice import (
    InvoiceCreate,
    InvoiceRead,
    LineItemCreate,
    LineItemRead,
)
from accounting_api.app.services.invoice_service import InvoiceService

router = APIRouter(prefix="/invoices", tags=["invoices"])


@router.post(
        "/",
        response_model=InvoiceRead,
        status_code=status.HTTP_201_CREATED,
        dependencies=[Depends(get_api_key)]
)
def create_invoice(
    payload: InvoiceCreate,
    db: Session = Depends(get_db),
):
    return InvoiceService(db).create_invoice(payload.customer_id)


@router.get("/{invoice_id}", response_model=InvoiceRead)
def get_invoice(
    invoice_id: int,
    db: Session = Depends(get_db),
):
    return InvoiceService(db).get_invoice(invoice_id)


@router.delete("/{invoice_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_invoice(
    invoice_id: int,
    db: Session = Depends(get_db),
):
    return InvoiceService(db).delete_invoice(invoice_id)


@router.post(
    "/{invoice_id}/items",
    response_model=LineItemRead,
    status_code=status.HTTP_201_CREATED,
)
def add_line_item(
    invoice_id: int,
    payload: LineItemCreate,
    db: Session = Depends(get_db),
):
    service = InvoiceService(db)
    return service.add_line_item(
        invoice_id=invoice_id,
        description=payload.description,
        quantity=payload.quantity,
        unit_price=payload.unit_price,
    )
