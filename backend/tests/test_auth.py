"""Auth endpoint tests — register, login, token validation."""

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.routers.auth import _users, _email_index

client = TestClient(app)


def _cleanup():
    _users.clear()
    _email_index.clear()


def test_register_success():
    _cleanup()
    resp = client.post(
        "/api/v1/auth/register",
        json={"email": "ali@forkfox.ai", "password": "securepass1", "display_name": "Ali"},
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["email"] == "ali@forkfox.ai"
    assert "id" in data
    assert "hashed_password" not in data


def test_register_duplicate_email():
    _cleanup()
    payload = {"email": "dup@forkfox.ai", "password": "securepass1", "display_name": "Dup"}
    client.post("/api/v1/auth/register", json=payload)
    resp = client.post("/api/v1/auth/register", json=payload)
    assert resp.status_code == 409
    assert resp.json()["error"]["code"] == "CONFLICT"


def test_login_success():
    _cleanup()
    client.post(
        "/api/v1/auth/register",
        json={"email": "user@forkfox.ai", "password": "securepass1", "display_name": "User"},
    )
    resp = client.post(
        "/api/v1/auth/token",
        json={"email": "user@forkfox.ai", "password": "securepass1"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["expires_in"] > 0


def test_login_wrong_password():
    _cleanup()
    client.post(
        "/api/v1/auth/register",
        json={"email": "u2@forkfox.ai", "password": "securepass1", "display_name": "U2"},
    )
    resp = client.post(
        "/api/v1/auth/token",
        json={"email": "u2@forkfox.ai", "password": "wrongpassword"},
    )
    assert resp.status_code == 401
    assert resp.json()["error"]["code"] == "UNAUTHORIZED"


def test_login_unknown_email():
    _cleanup()
    resp = client.post(
        "/api/v1/auth/token",
        json={"email": "ghost@forkfox.ai", "password": "securepass1"},
    )
    assert resp.status_code == 401


def test_error_shape_consistent():
    """All errors must have error.code and error.message."""
    resp = client.get("/api/v1/dishes/nonexistent-dish")
    body = resp.json()
    assert "error" in body
    assert "code" in body["error"]
    assert "message" in body["error"]
