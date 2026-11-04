"""Tests for the sample data."""

from app.seed import seed


def test_seed_adds_sample_data_with_something_in_every_list(client):
    seed()

    assert len(client.get("/api/customers").json()) == 4
    assert len(client.get("/api/staff").json()) == 4

    jobs = client.get("/api/jobs").json()
    assert len(jobs) == 7
    assert {job["status"] for job in jobs} == {"Pending", "In Progress", "Completed"}
    assert any(job["is_overdue"] for job in jobs)

    assert len(client.get("/api/jobs?upcoming=true").json()) == 4


def test_seed_adds_nothing_if_the_database_already_has_customers(client):
    seed()
    seed()

    assert len(client.get("/api/customers").json()) == 4
    assert len(client.get("/api/jobs").json()) == 7
