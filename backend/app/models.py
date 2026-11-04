"""The database tables, as SQLAlchemy classes."""

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


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
