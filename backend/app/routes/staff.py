"""API routes for the list of fitters and maintenance engineers."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Staff
from app.schemas import StaffCreate, StaffDetails, StaffOut

router = APIRouter(prefix="/api/staff", tags=["Staff"])


def find_staff(db: Session, staff_id: int) -> Staff:
    staff = db.get(Staff, staff_id)
    if staff is None:
        raise HTTPException(status_code=404, detail="Staff member not found.")
    return staff


@router.get("", response_model=list[StaffOut])
def list_staff(db: Session = Depends(get_db)):
    return db.scalars(select(Staff).order_by(func.lower(Staff.name))).all()


@router.post("", response_model=StaffOut, status_code=201)
def create_staff(new_staff: StaffCreate, db: Session = Depends(get_db)):
    staff = Staff(**new_staff.model_dump(), is_active=True)
    db.add(staff)
    db.commit()
    return staff


# ":int" works as it does in customers.py: a non-numeric id is a 404.
@router.get("/{staff_id:int}", response_model=StaffOut)
def get_staff(staff_id: int, db: Session = Depends(get_db)):
    return find_staff(db, staff_id)


@router.put("/{staff_id:int}", response_model=StaffOut)
def update_staff(staff_id: int, details: StaffDetails, db: Session = Depends(get_db)):
    staff = find_staff(db, staff_id)
    for field, value in details.model_dump().items():
        setattr(staff, field, value)
    db.commit()
    return staff
