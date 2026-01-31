"""
Test cases for the main FastAPI application.

This module contains test cases for the FastAPI application endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.config import settings
from app.models.message import MessageTier

# Create test client
client = TestClient(app)

# Test data
TEST_QUERY = "Hello, world!"
TEST_TIERS = [tier.value for tier in MessageTier]  # Use actual enum values
INVALID_TIERS = ["space", "ocean", "", None, 123, "aerial"]  # Add invalid tiers

# Test root endpoint
def test_read_root():
    """Test the root endpoint returns the correct welcome message."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert settings.PROJECT_NAME in data["message"]

# Test API version prefix
def test_api_prefix():
    """Test that the API routes are properly prefixed."""
    response = client.get("/" + settings.API_V1_STR)
    # Should return 404 if the prefix is correct but no matching route
    assert response.status_code == 404

# Test CORS headers
def test_cors_headers():
    """Test that CORS headers are properly set."""
    response = client.options(
        "/",
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "GET",
            "Access-Control-Request-Headers": "Content-Type",
        },
    )
    assert response.status_code == 200
    assert "access-control-allow-origin" in response.headers
    assert "access-control-allow-methods" in response.headers
    assert "access-control-allow-headers" in response.headers

# Test API version endpoint
def test_api_version():
    """Test the API version endpoint."""
    response = client.get(f"{settings.API_V1_STR}/version")
    assert response.status_code == 200
    data = response.json()
    assert "version" in data
    assert isinstance(data["version"], str)

# Test message creation endpoint
@pytest.mark.parametrize("tier", TEST_TIERS)
def test_create_message(tier):
    """Test creating a message with valid tiers."""
    response = client.post(
        f"{settings.API_V1_STR}/messages/",
        json={"tier": tier, "query": TEST_QUERY}
    )
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["tier"] == tier
    assert data["query"] == TEST_QUERY
    assert "created_at" in data

# Test message creation with invalid tiers
@pytest.mark.parametrize("tier", INVALID_TIERS)
def test_create_message_invalid_tier(tier):
    """Test creating a message with invalid tiers."""
    response = client.post(
        f"{settings.API_V1_STR}/messages/",
        json={"tier": tier, "query": TEST_QUERY}
    )
    assert response.status_code in [400, 422]  # 400 for empty string, 422 for validation error

# Test message creation with empty query
def test_create_message_empty_query():
    """Test creating a message with an empty query."""
    response = client.post(
        f"{settings.API_V1_STR}/messages/",
        json={"tier": MessageTier.TERRESTRIAL.value, "query": ""}
    )
    assert response.status_code == 422  # Validation error
    data = response.json()
    assert "detail" in data

# Test message creation with missing fields
def test_create_message_missing_fields():
    """Test creating a message with missing required fields."""
    # Missing query
    response = client.post(
        f"{settings.API_V1_STR}/messages/",
        json={"tier": MessageTier.TERRESTRIAL.value}
    )
    assert response.status_code == 422  # Validation error

    # Missing tier
    response = client.post(
        f"{settings.API_V1_STR}/messages/",
        json={"query": TEST_QUERY}
    )
    assert response.status_code == 422  # Validation error

# Test 404 for non-existent routes
def test_nonexistent_route():
    """Test that a non-existent route returns a 404 status code."""
    response = client.get("/nonexistent/route")
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
