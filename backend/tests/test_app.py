"""Tests for the parts every feature relies on."""

from pathlib import Path

from fastapi.testclient import TestClient
from sqlalchemy import text

from app import database
from app.main import app


def client_that_returns_server_errors():
    # By default the test client re-raises server errors instead of returning them.
    return TestClient(app, raise_server_exceptions=False)


def test_health_check_succeeds_with_a_working_database(client):
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_health_check_fails_when_the_database_cannot_be_opened(tmp_path, monkeypatch):
    # A folder can't be opened as a database file.
    monkeypatch.setattr(database, "engine", database.make_engine(tmp_path))

    response = client_that_returns_server_errors().get("/api/health")

    assert response.status_code == 500


def test_unknown_url_returns_404(client):
    response = client.get("/api/no-such-page")

    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}


def test_unexpected_error_returns_a_json_message(monkeypatch):
    def broken_database():
        raise RuntimeError("secret details")

    monkeypatch.setitem(app.dependency_overrides, database.get_db, broken_database)

    response = client_that_returns_server_errors().get("/api/health")

    assert response.status_code == 500
    assert response.json() == {"detail": "Something went wrong on the server."}


def test_foreign_keys_are_turned_on(tmp_path):
    engine = database.make_engine(tmp_path / "test.db")

    with engine.connect() as connection:
        assert connection.execute(text("PRAGMA foreign_keys")).scalar() == 1


def test_database_path_does_not_depend_on_the_current_folder():
    assert Path(database.engine.url.database).is_absolute()
