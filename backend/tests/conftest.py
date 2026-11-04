import pytest
from fastapi.testclient import TestClient

from app import database
from app.main import app


@pytest.fixture
def client(tmp_path, monkeypatch):
    """A test client with its own empty database, new for every test."""
    monkeypatch.setattr(database, "engine", database.make_engine(tmp_path / "test.db"))
    # The "with" block runs the app's startup, which creates the tables.
    with TestClient(app) as test_client:
        yield test_client
