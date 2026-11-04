"""The database connection, and one session for each request."""

import os
from pathlib import Path

from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session
from sqlalchemy.pool import NullPool

# Built from this file's location, so the app opens the same database
# whichever folder it starts from.
DATABASE_PATH = Path(__file__).resolve().parent.parent / "crm.db"


def make_engine(path):
    engine = create_engine(
        f"sqlite:///{path}",
        # Close each connection after use. A pool would keep the file open,
        # and Windows then can't delete a test database.
        poolclass=NullPool,
        # The ORM writes the SQL for us. Run with CRM_ECHO_SQL=1 to see it in the terminal.
        echo=os.environ.get("CRM_ECHO_SQL") == "1",
    )

    # SQLite ignores foreign keys unless each new connection turns them on.
    @event.listens_for(engine, "connect")
    def turn_on_foreign_keys(connection, _record):
        connection.execute("PRAGMA foreign_keys = ON")

    return engine


engine = make_engine(DATABASE_PATH)


def get_db():
    """Give a route a session, and close it when the request ends."""
    with Session(engine) as session:
        yield session
