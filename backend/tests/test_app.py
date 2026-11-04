"""Tests for the parts every feature relies on."""

from fastapi.testclient import TestClient
from sqlalchemy import text

from app import database
from app.main import app


def test_health_check_reaches_the_database(client):
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_unknown_url_returns_404(client):
    response = client.get("/api/no-such-page")

    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}


def test_unexpected_error_returns_a_clean_500(client):
    def broken_database():
        raise RuntimeError("secret details")

    app.dependency_overrides[database.get_db] = broken_database
    try:
        # By default the test client re-raises server errors instead of returning them.
        with TestClient(app, raise_server_exceptions=False) as test_client:
            response = test_client.get("/api/health")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 500
    assert response.json() == {"detail": "Something went wrong on the server."}
    assert "secret details" not in response.text


def test_foreign_keys_are_turned_on(tmp_path):
    engine = database.make_engine(tmp_path / "test.db")

    with engine.connect() as connection:
        assert connection.execute(text("PRAGMA foreign_keys")).scalar() == 1


def test_default_database_path_does_not_depend_on_the_current_folder():
    assert database.DEFAULT_DATABASE.is_absolute()
    assert database.DEFAULT_DATABASE.parent.name == "backend"
