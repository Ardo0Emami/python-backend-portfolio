from sqlalchemy.orm import Session
from typing import Optional
from accounting_api.app.models.sqlalchemy_models import Customer


class CustomerRepository:
    """Repository for basic Customer CRUD operations."""

    def __init__(self, db: Session):
        self.db = db

    def add(self, name: str, email: Optional[str]) -> Customer:
        customer = Customer(name=name, email=email)
        self.db.add(customer)
        self.db.flush()
        return customer

    def get(self, customer_id: Optional[int]) -> Optional[Customer]:
        return self.db.get(Customer, customer_id)

    def delete(self, customer_id: Optional[int]) -> bool:
        customer = self.get(customer_id)
        if not customer:
            return False
        self.db.delete(customer)
        self.db.flush()
        return True

    def list(self) -> Optional[list[Customer]]:
        return list(self.db.query(Customer).order_by(Customer.id.asc()))
