"""Tests for brief section C (appointments) and the rest of D (jobs and their statuses)."""

from datetime import datetime, timedelta

import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app import database
from app.models import Job


def in_days(days, hour=9):
    """A date and time in the format a datetime-local input sends."""
    day = datetime.now() + timedelta(days=days)
    return day.replace(hour=hour, minute=30).strftime("%Y-%m-%dT%H:%M")


def add_customer(client, name="Anna Lee"):
    body = {"name": name, "phone": "0113 496 0000", "address": "1 High Street, Leeds"}
    return client.post("/api/customers", json=body).json()["id"]


def add_staff(client, name="Sam Patel", is_active=True):
    body = {"name": name, "role": "Fitter", "phone": "0113 496 0001"}
    staff_id = client.post("/api/staff", json=body).json()["id"]
    if not is_active:
        client.put(f"/api/staff/{staff_id}", json={**body, "is_active": False})
    return staff_id


@pytest.fixture
def booking(client):
    """A valid booking request, with a customer and staff member already in the database."""
    return {
        "customer_id": add_customer(client),
        "staff_id": add_staff(client),
        "description": "Fit a new boiler",
        "scheduled_at": in_days(1),
    }


def book_job(client, booking, **changes):
    response = client.post("/api/jobs", json={**booking, **changes})
    assert response.status_code == 201
    return response.json()


def add_past_job(booking, status="Pending"):
    """The API refuses past dates, so a job from the past goes straight into the database."""
    with Session(database.engine) as session:
        job = Job(
            customer_id=booking["customer_id"],
            staff_id=booking["staff_id"],
            description="Old job",
            # Whole minutes, as the API stores them.
            scheduled_at=(datetime.now() - timedelta(days=1)).replace(second=0, microsecond=0),
            status=status,
        )
        session.add(job)
        session.commit()
        return job.id


def field_errors(response):
    assert response.status_code == 422
    return response.json()["errors"]


# Booking


def test_booking_stores_the_job_as_pending(client, booking):
    job = book_job(client, booking)

    assert job["status"] == "Pending"
    assert job["description"] == "Fit a new boiler"
    assert job["customer"]["name"] == "Anna Lee"
    assert job["staff"]["name"] == "Sam Patel"
    assert job["scheduled_at"] == booking["scheduled_at"] + ":00"
    assert client.get(f"/api/jobs/{job['id']}").json() == job


@pytest.mark.parametrize(
    "field, value, message",
    [
        ("customer_id", "", "Choose a customer."),
        ("staff_id", "", "Choose a staff member."),
        ("customer_id", 999, "That customer doesn't exist."),
        ("staff_id", 999, "That staff member doesn't exist."),
        ("description", "", "Description is required."),
        ("description", "   ", "Description is required."),
        ("scheduled_at", "", "Date and time is required."),
    ],
)
def test_booking_rejects_invalid_input_and_saves_nothing(client, booking, field, value, message):
    response = client.post("/api/jobs", json={**booking, field: value})

    assert field_errors(response) == {field: message}
    assert client.get("/api/jobs").json() == []


@pytest.mark.parametrize(
    "value",
    [
        "not a date",
        "2026-13-40T09:30",
        "2030-01-01T09:30:00+01:00",
        # What Chrome sends if you type the date straight through without moving on.
        "202609-11-05T03:00",
        12345,
        None,
    ],
)
def test_booking_rejects_a_bad_date_with_a_plain_message(client, booking, value):
    response = client.post("/api/jobs", json={**booking, "scheduled_at": value})

    assert field_errors(response) == {"scheduled_at": "Enter a valid date and time."}


def test_booking_rejects_a_time_in_the_past(client, booking):
    response = client.post("/api/jobs", json={**booking, "scheduled_at": in_days(-1)})

    assert field_errors(response) == {"scheduled_at": "Choose a date and time in the future."}


def test_booking_rejects_inactive_staff(client, booking):
    leaver = add_staff(client, name="Lee Hall", is_active=False)

    response = client.post("/api/jobs", json={**booking, "staff_id": leaver})

    assert field_errors(response) == {"staff_id": "Lee Hall is inactive, so can't take new jobs."}


def test_booking_reports_every_problem_at_once(client):
    response = client.post(
        "/api/jobs", json={"customer_id": "", "staff_id": "", "description": "", "scheduled_at": ""}
    )

    assert set(field_errors(response)) == {"customer_id", "staff_id", "description", "scheduled_at"}


def test_database_refuses_a_job_for_a_customer_that_does_not_exist(booking):
    # This test doesn't call the API. It proves SQLite is enforcing foreign keys.
    with Session(database.engine) as session:
        session.add(
            Job(
                customer_id=999,
                staff_id=booking["staff_id"],
                description="Job",
                scheduled_at=datetime.now(),
                status="Pending",
            )
        )
        with pytest.raises(IntegrityError):
            session.commit()


# Double booking


@pytest.mark.parametrize("first_job_status", ["Pending", "In Progress"])
def test_booking_rejects_a_second_open_job_for_one_person_at_the_same_time(
    client, booking, first_job_status
):
    first = book_job(client, booking)
    client.patch(f"/api/jobs/{first['id']}/status", json={"status": first_job_status})

    response = client.post("/api/jobs", json=booking)

    assert field_errors(response) == {
        "scheduled_at": "This staff member already has an open job at that time."
    }


@pytest.mark.parametrize("extra", [":59", ":00.5"])
def test_seconds_do_not_get_around_the_double_booking_rule(client, booking, extra):
    book_job(client, booking)

    response = client.post(
        "/api/jobs", json={**booking, "scheduled_at": booking["scheduled_at"] + extra}
    )

    assert "scheduled_at" in field_errors(response)


def test_two_people_can_have_jobs_at_the_same_time(client, booking):
    book_job(client, booking)

    book_job(client, booking, staff_id=add_staff(client, name="Priya Shah"))


def test_one_person_can_have_jobs_at_different_times(client, booking):
    book_job(client, booking)

    book_job(client, booking, scheduled_at=in_days(1, hour=14))


def test_a_completed_job_does_not_block_its_time(client, booking):
    job = book_job(client, booking)
    client.patch(f"/api/jobs/{job['id']}/status", json={"status": "Completed"})

    book_job(client, booking)


@pytest.mark.parametrize("new_status", ["Pending", "In Progress"])
def test_reopening_a_completed_job_is_refused_if_its_time_is_taken(client, booking, new_status):
    first = book_job(client, booking)
    client.patch(f"/api/jobs/{first['id']}/status", json={"status": "Completed"})
    book_job(client, booking)

    response = client.patch(f"/api/jobs/{first['id']}/status", json={"status": new_status})

    assert response.status_code == 409
    assert response.json() == {"detail": "This staff member already has an open job at that time."}
    assert client.get(f"/api/jobs/{first['id']}").json()["status"] == "Completed"


def test_reopening_a_completed_job_is_allowed_if_its_time_is_free(client, booking):
    job = book_job(client, booking)
    client.patch(f"/api/jobs/{job['id']}/status", json={"status": "Completed"})

    response = client.patch(f"/api/jobs/{job['id']}/status", json={"status": "In Progress"})

    assert response.status_code == 200
    assert client.get(f"/api/jobs/{job['id']}").json()["status"] == "In Progress"


# Listing and upcoming appointments


def test_job_lists_are_empty_at_first(client):
    assert client.get("/api/jobs").json() == []
    assert client.get("/api/jobs?upcoming=true").json() == []


def test_upcoming_lists_future_open_jobs_with_the_soonest_first(client, booking):
    later = book_job(client, booking, scheduled_at=in_days(3))
    sooner = book_job(client, booking, scheduled_at=in_days(1))
    started = book_job(client, booking, scheduled_at=in_days(2))
    client.patch(f"/api/jobs/{started['id']}/status", json={"status": "In Progress"})

    ids = [job["id"] for job in client.get("/api/jobs?upcoming=true").json()]

    assert ids == [sooner["id"], started["id"], later["id"]]


def test_upcoming_leaves_out_completed_and_past_jobs(client, booking):
    completed = book_job(client, booking, scheduled_at=in_days(1))
    client.patch(f"/api/jobs/{completed['id']}/status", json={"status": "Completed"})
    past = add_past_job(booking)

    assert client.get("/api/jobs?upcoming=true").json() == []

    all_ids = [job["id"] for job in client.get("/api/jobs").json()]
    assert all_ids == [past, completed["id"]]


def test_jobs_can_be_listed_for_one_customer(client, booking):
    other_customer = add_customer(client, name="Bob Brown")
    theirs = book_job(client, booking, customer_id=other_customer)
    book_job(client, booking, scheduled_at=in_days(2))

    jobs = client.get(f"/api/jobs?customer_id={other_customer}").json()

    assert [job["id"] for job in jobs] == [theirs["id"]]


def test_jobs_can_be_listed_for_one_staff_member(client, booking):
    other_staff = add_staff(client, name="Priya Shah")
    theirs = book_job(client, booking, staff_id=other_staff)
    book_job(client, booking, scheduled_at=in_days(2))

    jobs = client.get(f"/api/jobs?staff_id={other_staff}").json()

    assert [job["id"] for job in jobs] == [theirs["id"]]


@pytest.mark.parametrize("job_id", [999, "abc", 2**63])
def test_unknown_job_returns_404(client, job_id):
    assert client.get(f"/api/jobs/{job_id}").status_code == 404


# Overdue label


@pytest.mark.parametrize(
    "status, expected",
    [("Pending", True), ("In Progress", False), ("Completed", False)],
)
def test_only_a_past_pending_job_is_overdue(client, booking, status, expected):
    job_id = add_past_job(booking, status=status)

    assert client.get(f"/api/jobs/{job_id}").json()["is_overdue"] is expected


def test_a_future_job_is_not_overdue(client, booking):
    assert book_job(client, booking)["is_overdue"] is False


# Editing


def test_edit_job_can_change_everything_except_the_status(client, booking):
    job = book_job(client, booking)
    client.patch(f"/api/jobs/{job['id']}/status", json={"status": "In Progress"})
    changes = {
        "customer_id": add_customer(client, name="Bob Brown"),
        "staff_id": add_staff(client, name="Priya Shah"),
        "description": "Service the boiler",
        "scheduled_at": in_days(5),
    }

    response = client.put(f"/api/jobs/{job['id']}", json=changes)

    assert response.status_code == 200
    stored = client.get(f"/api/jobs/{job['id']}").json()
    assert stored["customer"]["name"] == "Bob Brown"
    assert stored["staff"]["name"] == "Priya Shah"
    assert stored["description"] == "Service the boiler"
    assert stored["scheduled_at"] == changes["scheduled_at"] + ":00"
    assert stored["status"] == "In Progress"


def test_edit_job_can_keep_its_own_time(client, booking):
    job = book_job(client, booking)

    response = client.put(f"/api/jobs/{job['id']}", json={**booking, "description": "Changed"})

    assert response.status_code == 200


def test_edit_job_can_correct_a_past_job_without_changing_its_time(client, booking):
    job_id = add_past_job(booking)
    stored = client.get(f"/api/jobs/{job_id}").json()

    response = client.put(
        f"/api/jobs/{job_id}",
        json={**booking, "description": "Corrected", "scheduled_at": stored["scheduled_at"]},
    )

    assert response.status_code == 200
    assert client.get(f"/api/jobs/{job_id}").json()["description"] == "Corrected"


def test_edit_job_rejects_moving_it_into_the_past(client, booking):
    job = book_job(client, booking)

    response = client.put(f"/api/jobs/{job['id']}", json={**booking, "scheduled_at": in_days(-1)})

    assert field_errors(response) == {"scheduled_at": "Choose a date and time in the future."}
    assert client.get(f"/api/jobs/{job['id']}").json() == job


def test_edit_job_rejects_moving_it_onto_a_taken_time(client, booking):
    book_job(client, booking)
    other = book_job(client, booking, scheduled_at=in_days(2))

    response = client.put(f"/api/jobs/{other['id']}", json=booking)

    assert "scheduled_at" in field_errors(response)


def test_edit_job_rejects_giving_it_to_someone_already_booked_then(client, booking):
    priya = add_staff(client, name="Priya Shah")
    book_job(client, booking, staff_id=priya)
    job = book_job(client, booking)

    response = client.put(f"/api/jobs/{job['id']}", json={**booking, "staff_id": priya})

    assert "scheduled_at" in field_errors(response)


def test_edit_job_can_keep_a_staff_member_who_has_since_left(client, booking):
    job = book_job(client, booking)
    client.put(
        f"/api/staff/{booking['staff_id']}",
        json={"name": "Sam Patel", "role": "Fitter", "phone": "0113 496 0001", "is_active": False},
    )

    response = client.put(f"/api/jobs/{job['id']}", json={**booking, "description": "Changed"})

    assert response.status_code == 200


def test_edit_job_rejects_changing_to_an_inactive_staff_member(client, booking):
    job = book_job(client, booking)
    leaver = add_staff(client, name="Lee Hall", is_active=False)

    response = client.put(f"/api/jobs/{job['id']}", json={**booking, "staff_id": leaver})

    assert "staff_id" in field_errors(response)


def test_edit_unknown_job_returns_404(client, booking):
    assert client.put("/api/jobs/999", json=booking).status_code == 404


# Job status


@pytest.mark.parametrize("status", ["Pending", "In Progress", "Completed"])
def test_update_job_status_stores_it(client, booking, status):
    job = book_job(client, booking)

    response = client.patch(f"/api/jobs/{job['id']}/status", json={"status": status})

    assert response.status_code == 200
    assert client.get(f"/api/jobs/{job['id']}").json()["status"] == status


def test_update_job_status_works_on_a_past_job(client, booking):
    job_id = add_past_job(booking)

    response = client.patch(f"/api/jobs/{job_id}/status", json={"status": "Completed"})

    assert response.status_code == 200


def test_update_job_status_rejects_an_unknown_status(client, booking):
    job = book_job(client, booking)

    response = client.patch(f"/api/jobs/{job['id']}/status", json={"status": "Cancelled"})

    assert "status" in field_errors(response)
    assert client.get(f"/api/jobs/{job['id']}").json()["status"] == "Pending"


def test_update_status_of_unknown_job_returns_404(client):
    response = client.patch("/api/jobs/999/status", json={"status": "Completed"})

    assert response.status_code == 404


# Onboarding moves with the jobs


def onboarding_status(client, customer_id):
    return client.get(f"/api/customers/{customer_id}").json()["onboarding_status"]


def set_onboarding_status(client, customer_id, status):
    client.patch(f"/api/customers/{customer_id}/status", json={"onboarding_status": status})


def test_booking_a_job_moves_a_new_enquiry_to_in_progress(client, booking):
    assert onboarding_status(client, booking["customer_id"]) == "New Enquiry"

    book_job(client, booking)

    assert onboarding_status(client, booking["customer_id"]) == "In Progress"


@pytest.mark.parametrize("status", ["In Progress", "Active"])
def test_booking_a_job_leaves_a_customer_past_new_enquiry_alone(client, booking, status):
    set_onboarding_status(client, booking["customer_id"], status)

    book_job(client, booking)

    assert onboarding_status(client, booking["customer_id"]) == status


@pytest.mark.parametrize(
    "changes", [{"description": ""}, {"scheduled_at": in_days(-1)}, {"staff_id": 999}]
)
def test_a_refused_booking_does_not_move_the_customer(client, booking, changes):
    response = client.post("/api/jobs", json={**booking, **changes})

    assert response.status_code == 422
    assert onboarding_status(client, booking["customer_id"]) == "New Enquiry"


def test_moving_a_job_to_a_new_enquiry_customer_moves_that_customer(client, booking):
    job = book_job(client, booking)
    other_customer = add_customer(client, name="Bob Brown")

    client.put(f"/api/jobs/{job['id']}", json={**booking, "customer_id": other_customer})

    assert onboarding_status(client, other_customer) == "In Progress"


def test_moving_a_job_to_an_active_customer_leaves_them_active(client, booking):
    job = book_job(client, booking)
    other_customer = add_customer(client, name="Bob Brown")
    set_onboarding_status(client, other_customer, "Active")

    client.put(f"/api/jobs/{job['id']}", json={**booking, "customer_id": other_customer})

    assert onboarding_status(client, other_customer) == "Active"


@pytest.mark.parametrize("status", ["New Enquiry", "Active"])
def test_editing_a_job_leaves_a_status_set_by_hand_alone(client, booking, status):
    job = book_job(client, booking)
    set_onboarding_status(client, booking["customer_id"], status)

    response = client.put(f"/api/jobs/{job['id']}", json={**booking, "description": "Changed"})

    assert response.status_code == 200
    assert onboarding_status(client, booking["customer_id"]) == status


@pytest.mark.parametrize(
    "changes", [{"description": ""}, {"scheduled_at": in_days(-1)}, {"staff_id": 999}]
)
def test_a_refused_edit_does_not_move_the_customer(client, booking, changes):
    job = book_job(client, booking)
    other_customer = add_customer(client, name="Bob Brown")

    response = client.put(
        f"/api/jobs/{job['id']}",
        json={**booking, "customer_id": other_customer, **changes},
    )

    assert response.status_code == 422
    assert onboarding_status(client, other_customer) == "New Enquiry"


def test_completing_a_job_makes_the_customer_active(client, booking):
    job = book_job(client, booking)

    response = client.patch(f"/api/jobs/{job['id']}/status", json={"status": "Completed"})

    assert response.json()["customer"]["onboarding_status"] == "Active"
    assert onboarding_status(client, booking["customer_id"]) == "Active"


def test_completing_a_job_makes_a_new_enquiry_customer_active(client, booking):
    job = book_job(client, booking)
    set_onboarding_status(client, booking["customer_id"], "New Enquiry")

    client.patch(f"/api/jobs/{job['id']}/status", json={"status": "Completed"})

    assert onboarding_status(client, booking["customer_id"]) == "Active"


@pytest.mark.parametrize("status", ["Pending", "In Progress"])
def test_other_job_statuses_do_not_make_the_customer_active(client, booking, status):
    job = book_job(client, booking)

    client.patch(f"/api/jobs/{job['id']}/status", json={"status": status})

    assert onboarding_status(client, booking["customer_id"]) == "In Progress"


def test_a_refused_reopen_leaves_the_customer_active(client, booking):
    first = book_job(client, booking)
    client.patch(f"/api/jobs/{first['id']}/status", json={"status": "Completed"})
    book_job(client, booking)

    response = client.patch(f"/api/jobs/{first['id']}/status", json={"status": "Pending"})

    assert response.status_code == 409
    assert onboarding_status(client, booking["customer_id"]) == "Active"


def test_reopening_a_completed_job_leaves_the_customer_active(client, booking):
    job = book_job(client, booking)
    client.patch(f"/api/jobs/{job['id']}/status", json={"status": "Completed"})

    client.patch(f"/api/jobs/{job['id']}/status", json={"status": "In Progress"})

    assert onboarding_status(client, booking["customer_id"]) == "Active"
