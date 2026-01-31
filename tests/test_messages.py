"""
Tests for the message endpoints.
"""
import pytest
from fastapi import status

from app.models.message import Message
from app.schemas.message import MessageCreate


def test_create_message(client, db_session):
    """Test creating a new message."""
    # Create test data
    message_data = {
        "tier": "info",
        "query": "Test query",
        "response": "Test response"
    }
    
    # Make the request
    response = client.post("/api/v1/messages/", json=message_data)
    
    # Assert the response
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["tier"] == message_data["tier"]
    assert data["query"] == message_data["query"]
    assert data["response"] == message_data["response"]
    assert "id" in data
    assert "timestamp" in data
    
    # Verify the message was saved to the database
    db_message = db_session.query(Message).filter(Message.id == data["id"]).first()
    assert db_message is not None
    assert db_message.tier == message_data["tier"]


def test_get_message(client, db_session):
    """Test retrieving a message by ID."""
    # Create a test message in the database
    test_message = Message(
        tier="test",
        query="Test query",
        response="Test response"
    )
    db_session.add(test_message)
    db_session.commit()
    db_session.refresh(test_message)
    
    # Make the request
    response = client.get(f"/api/v1/messages/{test_message.id}")
    
    # Assert the response
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == test_message.id
    assert data["tier"] == test_message.tier
    assert data["query"] == test_message.query
    assert data["response"] == test_message.response


def test_list_messages(client, db_session):
    """Test listing messages with pagination."""
    # Create test messages
    messages = [
        Message(tier=f"type_{i}", query=f"Query {i}", response=f"Response {i}")
        for i in range(5)
    ]
    db_session.add_all(messages)
    db_session.commit()
    
    # Make the request
    response = client.get("/api/v1/messages/?skip=1&limit=2")
    
    # Assert the response
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 2  # Should only return 2 items due to pagination
    
    # Verify the messages are ordered by most recent first
    assert data[0]["id"] > data[1]["id"]


def test_create_message_validation(client):
    """Test message creation validation."""
    # Missing required fields
    response = client.post("/api/v1/messages/", json={"tier": "info"})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    # Invalid tier
    response = client.post("/api/v1/messages/", json={
        "tier": "invalid",
        "query": "test",
        "response": "test"
    })
    assert response.status_code == status.HTTP_201_CREATED  # Or 422 if you add validation


def test_get_nonexistent_message(client):
    """Test retrieving a message that doesn't exist."""
    response = client.get("/api/v1/messages/999999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
