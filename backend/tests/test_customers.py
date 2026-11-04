"""Tests for brief sections A (customer management) and B (onboarding)."""

import pytest

VALID_CUSTOMER = {
    "name": "Anna Lee",
    "phone": "+44 7700 900123",
    "email": "anna@example.com",
    "address": "1 High Street, Leeds",
}


def add_customer(client, **changes):
    response = client.post("/api/customers", json={**VALID_CUSTOMER, **changes})
    assert response.status_code == 201
    return response.json()


def field_errors(response):
    assert response.status_code == 422
    return response.json()["errors"]


# Adding customers


def test_add_customer_stores_it_with_the_default_status(client):
    created = add_customer(client)

    assert created == {**VALID_CUSTOMER, "id": created["id"], "onboarding_status": "New Enquiry"}
    assert client.get(f"/api/customers/{created['id']}").json() == created


def test_add_customer_without_an_email(client):
    created = add_customer(client, email="")

    assert client.get(f"/api/customers/{created['id']}").json()["email"] == ""


def test_add_customer_removes_spaces_around_values(client):
    created = add_customer(client, name="  Anna Lee  ")

    assert created["name"] == "Anna Lee"


@pytest.mark.parametrize("phone", ["1234567", "123456789012345", "+44 (0)113-496 0000"])
def test_add_customer_accepts_valid_phone_numbers(client, phone):
    assert add_customer(client, phone=phone)["phone"] == phone


@pytest.mark.parametrize(
    "field, value, message",
    [
        ("name", "", "Name is required."),
        ("name", "   ", "Name is required."),
        ("phone", "", "Phone is required."),
        ("phone", "12a34567", "Enter a valid phone number."),
        ("phone", "123456", "Enter a valid phone number."),
        ("phone", "1234567890123456", "Enter a valid phone number."),
        ("email", "not-an-email", "Enter a valid email address."),
        ("email", "a@b", "Enter a valid email address."),
        ("address", "", "Address is required."),
        ("onboarding_status", "Unknown", "Input should be 'New Enquiry', 'In Progress' or 'Active'"),
    ],
)
def test_add_customer_rejects_invalid_input_and_saves_nothing(client, field, value, message):
    response = client.post("/api/customers", json={**VALID_CUSTOMER, field: value})

    assert field_errors(response) == {field: message}
    assert client.get("/api/customers").json() == []


def test_add_customer_reports_every_invalid_field_at_once(client):
    response = client.post("/api/customers", json={"name": "", "phone": "", "address": ""})

    assert field_errors(response) == {
        "name": "Name is required.",
        "phone": "Phone is required.",
        "address": "Address is required.",
    }


# Viewing customers


def test_customer_list_is_empty_at_first(client):
    response = client.get("/api/customers")

    assert response.status_code == 200
    assert response.json() == []


def test_customer_list_is_alphabetical_whatever_the_case(client):
    for name in ["Zed", "anna", "Bob"]:
        add_customer(client, name=name)

    names = [customer["name"] for customer in client.get("/api/customers").json()]

    assert names == ["anna", "Bob", "Zed"]


@pytest.mark.parametrize(
    "customer_id, message",
    [
        (999, "Customer not found."),
        ("abc", "Not Found"),
        (2**63, "Record not found."),
    ],
)
def test_unknown_customer_returns_404(client, customer_id, message):
    response = client.get(f"/api/customers/{customer_id}")

    assert response.status_code == 404
    assert response.json() == {"detail": message}


# Editing customers


def test_edit_customer_changes_the_details_and_keeps_the_status(client):
    created = add_customer(client, onboarding_status="Active")
    changes = {**VALID_CUSTOMER, "name": "Anna Khan", "address": "2 Low Road, York"}

    response = client.put(f"/api/customers/{created['id']}", json=changes)

    assert response.status_code == 200
    stored = client.get(f"/api/customers/{created['id']}").json()
    assert stored == {**changes, "id": created["id"], "onboarding_status": "Active"}


def test_edit_customer_can_clear_the_email(client):
    created = add_customer(client)

    response = client.put(f"/api/customers/{created['id']}", json={**VALID_CUSTOMER, "email": ""})

    assert response.status_code == 200
    assert client.get(f"/api/customers/{created['id']}").json()["email"] == ""


def test_edit_customer_rejects_invalid_input_and_changes_nothing(client):
    created = add_customer(client)

    response = client.put(f"/api/customers/{created['id']}", json={**VALID_CUSTOMER, "name": ""})

    assert field_errors(response) == {"name": "Name is required."}
    assert client.get(f"/api/customers/{created['id']}").json() == created


def test_edit_unknown_customer_returns_404(client):
    response = client.put("/api/customers/999", json=VALID_CUSTOMER)

    assert response.status_code == 404


# Onboarding status


@pytest.mark.parametrize("status", ["New Enquiry", "In Progress", "Active"])
def test_new_customer_can_start_at_any_status(client, status):
    assert add_customer(client, onboarding_status=status)["onboarding_status"] == status


@pytest.mark.parametrize("status", ["New Enquiry", "In Progress", "Active"])
def test_update_onboarding_status_stores_it(client, status):
    created = add_customer(client)

    response = client.patch(
        f"/api/customers/{created['id']}/status", json={"onboarding_status": status}
    )

    assert response.status_code == 200
    assert client.get(f"/api/customers/{created['id']}").json() == {
        **created,
        "onboarding_status": status,
    }


def test_update_onboarding_status_rejects_an_unknown_status(client):
    created = add_customer(client)

    response = client.patch(
        f"/api/customers/{created['id']}/status", json={"onboarding_status": "Unknown"}
    )

    assert "onboarding_status" in field_errors(response)
    assert client.get(f"/api/customers/{created['id']}").json() == created


def test_update_onboarding_status_of_unknown_customer_returns_404(client):
    response = client.patch("/api/customers/999/status", json={"onboarding_status": "Active"})

    assert response.status_code == 404
