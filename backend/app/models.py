"""The database tables, as SQLAlchemy classes."""

from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Parent of every table class. It keeps the list of tables to create."""


class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    phone: Mapped[str]
    email: Mapped[str]  # Blank when the customer has no email address.
    address: Mapped[str]
    onboarding_status: Mapped[str]  # schemas.py lists the allowed values.


class Staff(Base):
    __tablename__ = "staff"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    role: Mapped[str]  # schemas.py lists the allowed values.
    phone: Mapped[str]
    # Someone who leaves is marked inactive, so their past jobs keep their name.
    is_active: Mapped[bool]


class Job(Base):
    """A booked visit. One record is both the appointment and the work."""

    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"))
    staff_id: Mapped[int] = mapped_column(ForeignKey("staff.id"))
    description: Mapped[str]
    scheduled_at: Mapped[datetime]
    status: Mapped[str]  # schemas.py lists the allowed values.

    customer: Mapped[Customer] = relationship()
    staff: Mapped[Staff] = relationship()

    @property
    def is_overdue(self) -> bool:
        """Its time has passed and nobody has started it."""
        return self.status == "Pending" and self.scheduled_at < datetime.now()
