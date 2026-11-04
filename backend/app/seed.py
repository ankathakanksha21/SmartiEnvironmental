"""Adds sample data, so the app has something to show on a first run.

Run it from the backend folder: python -m app.seed
"""

from datetime import datetime, timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from app import database
from app.models import Base, Customer, Job, Staff


def days_from_now(days, hour, minute=0):
    """A time relative to today, so the sample jobs never go out of date."""
    day = datetime.now() + timedelta(days=days)
    return day.replace(hour=hour, minute=minute, second=0, microsecond=0)


def seed():
    Base.metadata.create_all(database.engine)

    with Session(database.engine) as session:
        if session.scalar(select(Customer.id)) is not None:
            print("The database already has customers, so nothing was added.")
            print("To start again, stop the backend, delete backend/crm.db and run this again.")
            return

        anna = Customer(
            name="Anna Lee",
            phone="0113 496 0101",
            email="anna.lee@example.com",
            address="1 High Street, Leeds, LS1 1AA",
            onboarding_status="Active",
        )
        bilal = Customer(
            name="Bilal Khan",
            phone="0113 496 0102",
            email="",
            address="22 Park Road, York, YO1 2BB",
            onboarding_status="In Progress",
        )
        chloe = Customer(
            name="Chloe Evans",
            phone="0113 496 0103",
            email="chloe.evans@example.com",
            address="5 Mill Lane, Harrogate, HG1 3CC",
            onboarding_status="New Enquiry",
        )
        dev = Customer(
            name="Dev Sharma",
            phone="0113 496 0104",
            email="dev.sharma@example.com",
            address="9 Station Road, Wakefield, WF1 4DD",
            onboarding_status="Active",
        )

        sam = Staff(name="Sam Patel", role="Fitter", phone="0113 496 0201", is_active=True)
        priya = Staff(
            name="Priya Shah", role="Maintenance Engineer", phone="0113 496 0202", is_active=True
        )
        tom = Staff(name="Tom Reed", role="Fitter", phone="0113 496 0203", is_active=True)
        lena = Staff(
            name="Lena Fox", role="Maintenance Engineer", phone="0113 496 0204", is_active=False
        )

        jobs = [
            Job(
                customer=anna,
                staff=sam,
                description="Fit the new unit",
                scheduled_at=days_from_now(1, 9, 30),
                status="Pending",
            ),
            Job(
                customer=bilal,
                staff=priya,
                description="Annual maintenance visit",
                scheduled_at=days_from_now(1, 14),
                status="Pending",
            ),
            Job(
                customer=dev,
                staff=tom,
                description="Replace the faulty part",
                scheduled_at=days_from_now(3, 11),
                status="In Progress",
            ),
            Job(
                customer=anna,
                staff=priya,
                description="First service after fitting",
                scheduled_at=days_from_now(10, 10),
                status="Pending",
            ),
            Job(
                customer=dev,
                staff=sam,
                description="Fit the replacement unit",
                scheduled_at=days_from_now(-7, 9),
                status="Completed",
            ),
            # This one shows the Overdue label under All jobs.
            Job(
                customer=bilal,
                staff=tom,
                description="Survey the site",
                scheduled_at=days_from_now(-2, 15),
                status="Pending",
            ),
            # An old job keeps the name of someone who has since left.
            Job(
                customer=anna,
                staff=lena,
                description="Check the existing system",
                scheduled_at=days_from_now(-30, 10),
                status="Completed",
            ),
        ]

        session.add_all([anna, bilal, chloe, dev, sam, priya, tom, lena, *jobs])
        session.commit()
        print("Added 4 customers, 4 staff members and 7 jobs.")


if __name__ == "__main__":
    seed()
