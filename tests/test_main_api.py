"""Test suite for Synova AI main API endpoints."""
import importlib
import os
import sqlite3

import pytest
from fastapi.testclient import TestClient  # type: ignore


@pytest.fixture()
def temp_db_path(tmp_path):
    return str(tmp_path / "test_synova.db")


@pytest.fixture()
def patched_sqlite(monkeypatch, temp_db_path):
    original_connect = sqlite3.connect

    def _connect(db_path, *args, **kwargs):
        # redirect all DB connections to a temp file for test isolation
        return original_connect(temp_db_path, *args, **kwargs)

    monkeypatch.setattr(sqlite3, "connect", _connect)
    yield
    # cleanup (optional): remove file if created
    if os.path.exists(temp_db_path):
        try:
            os.remove(temp_db_path)
        except OSError:
            pass


@pytest.fixture()
def patched_sleep(monkeypatch):
    import time

    monkeypatch.setattr(time, "sleep", lambda *_args, **_kwargs: None)


@pytest.fixture()
def app_and_module(patched_sqlite, patched_sleep):
    # Import inside the fixture after monkeypatch is applied
    # so module init uses the patched sqlite
    main = importlib.import_module("main")
    importlib.reload(main)
    return main.app, main


def test_root_health_and_stats_endpoints(app_and_module):
    app, main = app_and_module
    client = TestClient(app)

    # Root
    r = client.get("/")
    assert r.status_code == 200
    assert r.json()["status"] == "active"

    # Health
    r = client.get("/api/health")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data

    # Stats (empty DB at start)
    r = client.get("/api/stats")
    assert r.status_code == 200
    stats = r.json()
    assert isinstance(stats.get("users_by_tier", {}), dict)
    assert isinstance(stats.get("total_messages", 0), int)


def test_register_login_and_query_flow(app_and_module):
    app, main = app_and_module
    client = TestClient(app)

    # Register
    email = "test@example.com"
    password = "secret123"
    r = client.post(
        "/api/register",
        json={"email": email, "password": password}
    )
    assert r.status_code == 200
    user_id = r.json()["user_id"]

    # Duplicate register should fail
    r_dup = client.post(
        "/api/register", json={"email": email, "password": password}
    )
    assert r_dup.status_code == 400

    # Login
    r = client.post("/api/login", json={"email": email, "password": password})
    assert r.status_code == 200
    login_data = r.json()
    assert login_data["user_id"] == user_id
    assert login_data["tier"] == "terrestrial"

    # Query ok
    r = client.post(
        "/api/query",
        json={"query": "hello there", "tier": "terrestrial", "user_id": user_id},
    )
    assert r.status_code == 200
    payload = r.json()
    assert payload["success"] is True
    assert payload["data"]["tier"] == "terrestrial"
    assert isinstance(
        payload.get("data", {}).get("confidence", 0.0), float
    )

    # Query too long for tier
    long_query = "x" * 201
    r = client.post(
        "/api/query",
        json={"query": long_query, "tier": "terrestrial", "user_id": user_id},
    )
    assert r.status_code == 400


def test_hash_password_deterministic(app_and_module):
    _app, main = app_and_module
    h1 = main.hash_password("abc123")
    h2 = main.hash_password("abc123")
    h3 = main.hash_password("different")
    assert h1 == h2
    assert h1 != h3
