"""Tests for the staff list in brief section D."""

import pytest

VALID_STAFF = {
    "name": "Sam Patel",
    "role": "Fitter",
    "phone": "0113 496 0001",
}


def add_staff(client, **changes):
    response = client.post("/api/staff", json={**VALID_STAFF, **changes})
    assert response.status_code == 201
    return response.json()


def test_add_staff_stores_them_as_active(client):
    created = add_staff(client)

    assert created == {**VALID_STAFF, "id": created["id"], "is_active": True}
    assert client.get(f"/api/staff/{created['id']}").json() == created


@pytest.mark.parametrize("role", ["Fitter", "Maintenance Engineer"])
def test_add_staff_accepts_both_roles(client, role):
    assert add_staff(client, role=role)["role"] == role


@pytest.mark.parametrize(
    "field, value, message",
    [
        ("name", "", "Name is required."),
        ("name", "   ", "Name is required."),
        ("phone", "", "Phone is required."),
        ("phone", "12a34567", "Enter a valid phone number."),
        ("role", "Plumber", "Input should be 'Fitter' or 'Maintenance Engineer'"),
    ],
)
def test_add_staff_rejects_invalid_input_and_saves_nothing(client, field, value, message):
    response = client.post("/api/staff", json={**VALID_STAFF, field: value})

    assert response.status_code == 422
    assert response.json()["errors"] == {field: message}
    assert client.get("/api/staff").json() == []


def test_staff_list_is_empty_at_first(client):
    assert client.get("/api/staff").json() == []


def test_staff_list_is_alphabetical_whatever_the_case(client):
    for name in ["Zed", "anna", "Bob"]:
        add_staff(client, name=name)

    names = [staff["name"] for staff in client.get("/api/staff").json()]

    assert names == ["anna", "Bob", "Zed"]


@pytest.mark.parametrize("staff_id", [999, "abc", 2**63])
def test_unknown_staff_member_returns_404(client, staff_id):
    assert client.get(f"/api/staff/{staff_id}").status_code == 404


def test_edit_staff_changes_their_details(client):
    created = add_staff(client)
    changes = {
        "name": "Sam Khan",
        "role": "Maintenance Engineer",
        "phone": "0113 496 0002",
        "is_active": True,
    }

    response = client.put(f"/api/staff/{created['id']}", json=changes)

    assert response.status_code == 200
    assert client.get(f"/api/staff/{created['id']}").json() == {**changes, "id": created["id"]}


def test_staff_member_can_be_marked_inactive_and_active_again(client):
    created = add_staff(client)
    url = f"/api/staff/{created['id']}"

    client.put(url, json={**VALID_STAFF, "is_active": False})
    assert client.get(url).json()["is_active"] is False

    client.put(url, json={**VALID_STAFF, "is_active": True})
    assert client.get(url).json()["is_active"] is True


def test_inactive_staff_member_stays_in_the_list(client):
    created = add_staff(client)
    client.put(f"/api/staff/{created['id']}", json={**VALID_STAFF, "is_active": False})

    assert [staff["is_active"] for staff in client.get("/api/staff").json()] == [False]


def test_edit_staff_needs_the_active_flag_and_changes_nothing_without_it(client):
    created = add_staff(client)
    client.put(f"/api/staff/{created['id']}", json={**VALID_STAFF, "is_active": False})

    response = client.put(f"/api/staff/{created['id']}", json=VALID_STAFF)

    assert response.status_code == 422
    assert "is_active" in response.json()["errors"]
    assert client.get(f"/api/staff/{created['id']}").json()["is_active"] is False


def test_edit_staff_rejects_invalid_input_and_changes_nothing(client):
    created = add_staff(client)

    response = client.put(
        f"/api/staff/{created['id']}", json={**VALID_STAFF, "is_active": True, "name": ""}
    )

    assert response.json()["errors"] == {"name": "Name is required."}
    assert client.get(f"/api/staff/{created['id']}").json() == created


def test_edit_unknown_staff_member_returns_404(client):
    response = client.put("/api/staff/999", json={**VALID_STAFF, "is_active": True})

    assert response.status_code == 404
