"""API routes for jobs. A job is a booked visit, so these also cover appointments."""

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.models import Customer, Job, Staff
from app.schemas import JobDetails, JobOut, JobStatusUpdate

router = APIRouter(prefix="/api/jobs", tags=["Jobs"])

CLASH_MESSAGE = "This staff member already has an open job at that time."


def find_job(db: Session, job_id: int) -> Job:
    job = db.get(Job, job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found.")
    return job


def has_clash(db: Session, staff_id: int, scheduled_at: datetime, job: Job | None = None) -> bool:
    """Is this person on another open job at this exact time?"""
    query = select(Job.id).where(
        Job.staff_id == staff_id,
        Job.scheduled_at == scheduled_at,
        Job.status != "Completed",
    )
    if job is not None:
        query = query.where(Job.id != job.id)
    return db.scalar(query) is not None


def booking_errors(db: Session, details: JobDetails, job: Job | None = None) -> dict:
    """Check the rules that need the database. job is the one being edited, if any.

    An edit can keep a past time or an inactive staff member, so that a job
    already in that state can still have its description corrected.
    """
    errors = {}
    staff_changed = job is None or details.staff_id != job.staff_id
    time_changed = job is None or details.scheduled_at != job.scheduled_at

    if db.get(Customer, details.customer_id) is None:
        errors["customer_id"] = "That customer doesn't exist."

    staff = db.get(Staff, details.staff_id)
    if staff is None:
        errors["staff_id"] = "That staff member doesn't exist."
    elif staff_changed and not staff.is_active:
        errors["staff_id"] = f"{staff.name} is inactive, so can't take new jobs."

    if time_changed and details.scheduled_at < datetime.now():
        errors["scheduled_at"] = "Choose a date and time in the future."
    elif (staff_changed or time_changed) and has_clash(
        db, details.staff_id, details.scheduled_at, job
    ):
        errors["scheduled_at"] = CLASH_MESSAGE

    return errors


@router.get("", response_model=list[JobOut])
def list_jobs(
    upcoming: bool = False,
    customer_id: int | None = None,
    staff_id: int | None = None,
    db: Session = Depends(get_db),
):
    # joinedload fetches each job's customer and staff member in the same query.
    query = (
        select(Job)
        .options(joinedload(Job.customer), joinedload(Job.staff))
        .order_by(Job.scheduled_at)
    )
    if upcoming:
        query = query.where(Job.status != "Completed", Job.scheduled_at >= datetime.now())
    if customer_id is not None:
        query = query.where(Job.customer_id == customer_id)
    if staff_id is not None:
        query = query.where(Job.staff_id == staff_id)
    return db.scalars(query).all()


@router.post("", response_model=JobOut, status_code=201)
def create_job(details: JobDetails, db: Session = Depends(get_db)):
    errors = booking_errors(db, details)
    if errors:
        return JSONResponse(status_code=422, content={"errors": errors})

    job = Job(**details.model_dump(), status="Pending")
    db.add(job)
    db.commit()
    return job


# ":int" works as it does in customers.py: a non-numeric id is a 404.
@router.get("/{job_id:int}", response_model=JobOut)
def get_job(job_id: int, db: Session = Depends(get_db)):
    return find_job(db, job_id)


@router.put("/{job_id:int}", response_model=JobOut)
def update_job(job_id: int, details: JobDetails, db: Session = Depends(get_db)):
    job = find_job(db, job_id)
    errors = booking_errors(db, details, job)
    if errors:
        return JSONResponse(status_code=422, content={"errors": errors})

    for field, value in details.model_dump().items():
        setattr(job, field, value)
    db.commit()
    return job


@router.patch("/{job_id:int}/status", response_model=JobOut)
def update_job_status(job_id: int, update: JobStatusUpdate, db: Session = Depends(get_db)):
    job = find_job(db, job_id)

    # Reopening a completed job could put two open jobs in the same slot.
    reopening = job.status == "Completed" and update.status != "Completed"
    if reopening and has_clash(db, job.staff_id, job.scheduled_at, job):
        raise HTTPException(status_code=409, detail=CLASH_MESSAGE)

    job.status = update.status
    db.commit()
    return job
