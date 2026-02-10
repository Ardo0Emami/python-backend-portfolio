from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from accounting_api.app.api.dependencies.auth import get_api_key
from accounting_api.app.core.db_adapter import get_db
from accounting_api.app.services.customer_service import CustomerService
from accounting_api.app.models.schemas.customer import (
    CustomerCreate,
    CustomerRead,
)

router = APIRouter(prefix="/customers", tags=["customers"])


# ---- Routes ---- #
@router.post(
    "/",
    response_model=CustomerRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_api_key)]
)
def create_customer(
    payload: CustomerCreate,
    db: Session = Depends(get_db),
):
    return CustomerService(db).create_customer(
        name=payload.name,
        email=payload.email,
    )


@router.get("/{customer_id}", response_model=CustomerRead)
def read_customer(
    customer_id: int,
    db: Session = Depends(get_db),
):
    customer = CustomerService(db).get_customer(customer_id)
    if customer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found",
        )
    return customer


@router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_customer(
    customer_id: int,
    db: Session = Depends(get_db),
):
    deleted = CustomerService(db).delete_customer(customer_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found",
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/", response_model=list[CustomerRead])
def list_customers(
    db: Session = Depends(get_db),
):
    return CustomerService(db).list_customers()
