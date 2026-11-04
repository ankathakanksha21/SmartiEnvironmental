"""API routes for customers and their onboarding status."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Customer
from app.schemas import CustomerCreate, CustomerDetails, CustomerOut, CustomerStatusUpdate

router = APIRouter(prefix="/api/customers", tags=["Customers"])


def find_customer(db: Session, customer_id: int) -> Customer:
    customer = db.get(Customer, customer_id)
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found.")
    return customer


@router.get("", response_model=list[CustomerOut])
def list_customers(db: Session = Depends(get_db)):
    return db.scalars(select(Customer).order_by(func.lower(Customer.name))).all()


@router.post("", response_model=CustomerOut, status_code=201)
def create_customer(new_customer: CustomerCreate, db: Session = Depends(get_db)):
    customer = Customer(**new_customer.model_dump())
    db.add(customer)
    db.commit()
    return customer


# ":int" makes a non-numeric id a 404. Without it FastAPI returns a 422,
# and the page would ask the user to fix a form it doesn't have.
@router.get("/{customer_id:int}", response_model=CustomerOut)
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    return find_customer(db, customer_id)


@router.put("/{customer_id:int}", response_model=CustomerOut)
def update_customer(
    customer_id: int, details: CustomerDetails, db: Session = Depends(get_db)
):
    customer = find_customer(db, customer_id)
    for field, value in details.model_dump().items():
        setattr(customer, field, value)
    db.commit()
    return customer


@router.patch("/{customer_id:int}/status", response_model=CustomerOut)
def update_onboarding_status(
    customer_id: int, update: CustomerStatusUpdate, db: Session = Depends(get_db)
):
    customer = find_customer(db, customer_id)
    customer.onboarding_status = update.onboarding_status
    db.commit()
    return customer
