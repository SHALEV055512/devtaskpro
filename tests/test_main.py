# =============================================================
# IMPORTS
# =============================================================

import pytest
from fastapi.testclient import TestClient
from backend.main import app
from tests.test_validators import VALID_USER

client = TestClient(app)


# =============================================================
# HELP ENDPOINT TEST
# =============================================================

def test_help_endpoint_returns_ok():
    response = client.get("/help")
    assert response.status_code == 200
    assert response.headers.get("content-type", "").startswith("application/json")
    assert response.json() == {"status": "ok", "message": "Backend is alive!"}


# =============================================================
# REGISTER ENDPOINT TESTS
# =============================================================

@pytest.fixture
def existing_user():
    """Fixture for a user that already exists in the system"""
    data = VALID_USER.copy()
    data["email"] = "duplicate@example.com"
    return data


@pytest.fixture
def valid_user():
    """Fixture for a valid new user"""
    return VALID_USER.copy()


# -------------------------
# REGISTER - EXISTING EMAIL TEST
# -------------------------

def test_register_existing_email(monkeypatch, existing_user):
    """Verify that registering with an existing email returns 400"""
    monkeypatch.setattr("backend.main.get_user_by_email", lambda email: {"email": email})
    monkeypatch.setattr("backend.main.create_user", lambda data: None)

    response = client.post("/api/register", json=existing_user)

    assert response.status_code == 400
    assert response.json() == {"detail": "Email is already registered"}


# -------------------------
# REGISTER - SUCCESSFUL REGISTRATION TEST
# -------------------------

def test_register_success(monkeypatch, valid_user):
    monkeypatch.setattr("backend.main.get_user_by_email", lambda email: None)
    monkeypatch.setattr("backend.main.create_user", lambda data: None)

    response = client.post("/api/register", json=valid_user)

    assert response.status_code == 200
    assert response.json() == {"message": "User created"}


# -------------------------
# LOGGER SECURITY TEST (NO PASSWORD IN LOGS)
# -------------------------

def test_logger_does_not_expose_password(monkeypatch, caplog, valid_user):
    monkeypatch.setattr("backend.main.get_user_by_email", lambda email: None)
    monkeypatch.setattr("backend.main.create_user", lambda data: None)

    with caplog.at_level("INFO"):
        client.post("/api/register", json=valid_user)

    logs = " ".join(caplog.messages)

    # Ensure password is not logged
    assert "Password123" not in logs

    # Ensure other fields appear in logs
    assert "Shalev" in logs
    assert "Harari" in logs
