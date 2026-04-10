"""Dish endpoint tests — list, detail, scoring."""

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.routers.auth import _users, _email_index
from app.routers.dishes import _dishes

client = TestClient(app)


def _get_token(email="scorer@forkfox.ai", password="securepass1", name="Scorer"):
    _users.clear()
    _email_index.clear()
    client.post("/api/v1/auth/register", json={"email": email, "password": password, "display_name": name})
    resp = client.post("/api/v1/auth/token", json={"email": email, "password": password})
    return resp.json()["access_token"]


def test_list_dishes():
    resp = client.get("/api/v1/dishes")
    assert resp.status_code == 200
    data = resp.json()
    assert "items" in data
    assert isinstance(data["items"], list)
    assert data["page"] == 1


def test_list_dishes_filter_cuisine():
    resp = client.get("/api/v1/dishes?cuisine=Italian")
    assert resp.status_code == 200
    data = resp.json()
    for item in data["items"]:
        assert item["cuisine_type"] == "Italian"


def test_get_dish():
    resp = client.get("/api/v1/dishes/dish-001")
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == "dish-001"
    assert data["name"] == "Margherita Pizza"


def test_get_dish_not_found():
    resp = client.get("/api/v1/dishes/does-not-exist")
    assert resp.status_code == 404
    body = resp.json()
    assert body["error"]["code"] == "NOT_FOUND"


def test_score_dish_requires_auth():
    resp = client.post(
        "/api/v1/dishes/dish-001/score",
        json={"dish_id": "dish-001", "rating": 4.5},
    )
    assert resp.status_code == 401


def test_score_dish_success():
    token = _get_token()
    initial_ratings = list(_dishes["dish-001"]["ratings"])
    resp = client.post(
        "/api/v1/dishes/dish-001/score",
        json={"dish_id": "dish-001", "rating": 4.0, "notes": "Great crust!"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["dish_id"] == "dish-001"
    assert 0.0 <= data["community_score"] <= 100.0
    assert data["rating_count"] == len(initial_ratings) + 1
    # restore
    _dishes["dish-001"]["ratings"] = initial_ratings


def test_score_dish_id_mismatch():
    token = _get_token()
    resp = client.post(
        "/api/v1/dishes/dish-001/score",
        json={"dish_id": "dish-002", "rating": 3.0},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 400
    assert resp.json()["error"]["code"] == "BAD_REQUEST"


def test_score_dish_invalid_rating():
    token = _get_token()
    resp = client.post(
        "/api/v1/dishes/dish-001/score",
        json={"dish_id": "dish-001", "rating": 99.0},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 422
    assert resp.json()["error"]["code"] == "VALIDATION_ERROR"


def test_response_time_header():
    resp = client.get("/api/v1/dishes")
    assert "x-response-time" in resp.headers


def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"
