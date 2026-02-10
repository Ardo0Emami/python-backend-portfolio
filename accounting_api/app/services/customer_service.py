from __future__ import annotations

from typing import Optional, List
from sqlalchemy.orm import Session

from accounting_api.app.repositories.customer import CustomerRepository
from accounting_api.app.models.sqlalchemy_models import Customer


class CustomerService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = CustomerRepository(db)

    def create_customer(self, name: str, email: Optional[str]) -> Customer:
        customer = self.repo.add(name=name, email=email)
        return customer

    def get_customer(self, customer_id: int) -> Optional[Customer]:
        return self.repo.get(customer_id)

    def list_customers(self) -> Optional[List[Customer]]:
        return self.repo.list()

    def delete_customer(self, customer_id: int) -> bool:
        deleted = self.repo.delete(customer_id)
        return deleted
