"""The database tables, as SQLAlchemy classes."""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Parent of every table class. It keeps the list of tables to create."""
