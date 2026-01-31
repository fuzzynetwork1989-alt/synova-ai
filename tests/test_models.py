"""
Tests for the database models.
"""
from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from typing import Any, Dict
from unittest.mock import patch

import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.models.message import Message, MessageTier


class TestMessageModel:
    """Test cases for the Message model."""

    @pytest.fixture
    def test_message(self) -> Message:
        """Fixture providing a test message instance."""
        return Message(
            tier=MessageTier.TERRESTRIAL.value,  # Store as string value
            query="Test query",
            response="Test response",
        )

    @pytest.fixture
    def message_dict(self) -> Dict[str, Any]:
        """Fixture providing a dictionary representation of a message."""
        return {
            "tier": MessageTier.CELESTIAL.value,  # Store as string value
            "query": "Test query from dict",
            "response": "Test response from dict"
        }

    def test_message_creation(self, db_session, test_message):
        """Test creating a new message."""
        # Add to database
        db_session.add(test_message)
        db_session.commit()
        
        # Retrieve the message using modern SQLAlchemy 2.0 style
        stmt = select(Message).where(Message.id == test_message.id)
        db_message = db_session.execute(stmt).scalar_one_or_none()
        
        # Assertions
        assert db_message is not None
        assert db_message.id is not None
        assert db_message.tier == MessageTier.TERRESTRIAL
        assert db_message.query == "Test query"
        assert db_message.response == "Test response"
        assert db_message.created_at is not None
        assert db_message.updated_at is not None
        # Compare with timezone-naive datetime since that's what the model uses
        current_time = datetime.utcnow()
        assert db_message.created_at <= current_time
        assert db_message.updated_at <= current_time
        assert db_message.created_at == db_message.updated_at

    def test_message_creation_with_factory(self, db_session, message_dict):
        """Test creating a message using dictionary unpacking."""
        message = Message(**message_dict)
        db_session.add(message)
        db_session.commit()
        
        assert message.id is not None
        assert message.tier == message_dict["tier"]
        assert message.query == message_dict["query"]
        assert message.response == message_dict["response"]

    def test_message_representation(self, db_session, test_message):
        """Test the string representation of a message."""
        test_timestamp = datetime(2023, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        test_message.id = 1
        test_message.created_at = test_timestamp
        
        # The string representation should include the id, tier, and created_at
        assert "Message(id=1, tier=terrestrial, created_at=2023-01-01 12:00:00" in str(test_message)
        
        # Test with different tier - the string representation should use the enum's string value
        test_message.tier = MessageTier.GALACTIC.value  # Store as string value
        assert "tier=galactic" in str(test_message).lower()  # Case-insensitive check

    @pytest.mark.parametrize("tier,expected_tier_value", [
        ("terrestrial", "terrestrial"),
        ("celestial", "celestial"),
        ("galactic", "galactic"),
        (MessageTier.TERRESTRIAL.value, "terrestrial"),
        (MessageTier.CELESTIAL.value, "celestial"),
        (MessageTier.GALACTIC.value, "galactic"),
    ])
    def test_message_tier_values(self, tier, expected_tier_value, db_session):
        """Test that message tier values are correctly handled."""
        message = Message(tier=tier, query="test")
        db_session.add(message)
        db_session.commit()
        
        # Refresh to get the actual stored value
        db_session.refresh(message)
        assert message.tier == expected_tier_value
        assert isinstance(message.tier, str)

    def test_message_tier_invalid_value(self, db_session):
        """Test that invalid tier values are handled."""
        # Since the tier is just a string column, it will accept any value
        # But we'll test that it doesn't raise an error
        message = Message(tier="invalid_tier", query="test")
        db_session.add(message)
        db_session.commit()
        assert message.tier == "invalid_tier"

    def test_message_update_timestamps(self, db_session, test_message):
        """Test that updated_at changes when message is updated."""
        # Add initial message
        db_session.add(test_message)
        db_session.commit()
        
        # Store initial timestamps
        created_at = test_message.created_at
        original_updated = test_message.updated_at
        
        # Ensure there's a small time difference
        with patch('app.models.message.datetime') as mock_datetime:
            mock_datetime.utcnow.return_value = datetime.utcnow() + timedelta(seconds=10)
            
            # Update the message
            test_message.response = "Updated response"
            db_session.commit()
        
        # Verify timestamps
        assert test_message.created_at == created_at  # Should not change
        assert test_message.updated_at > original_updated  # Should be updated
        assert test_message.updated_at > test_message.created_at  # updated_at should be after created_at

    def test_message_required_fields(self, db_session):
        """Test that required fields are enforced."""
        # Test missing required field (query)
        with pytest.raises(IntegrityError):
            message = Message(tier=MessageTier.TERRESTRIAL)
            db_session.add(message)
            db_session.commit()

    def test_message_default_values(self, db_session):
        """Test default values for message fields."""
        message = Message(query="Test query")
        db_session.add(message)
        db_session.commit()
        
        assert message.tier == MessageTier.TERRESTRIAL.value  # Default tier as string
        assert message.response is None  # Default response
        assert message.created_at is not None  # Auto-generated
        assert message.updated_at is not None  # Auto-generated

    def test_message_json_serialization(self, test_message, db_session):
        """Test that message can be serialized to JSON."""
        # Add to database to get auto-generated values
        db_session.add(test_message)
        db_session.commit()
        db_session.refresh(test_message)
        
        # Convert to dict and then to JSON
        message_dict = test_message.__dict__.copy()
        # Remove SQLAlchemy internal attribute
        message_dict.pop('_sa_instance_state', None)
        
        # Convert to JSON and back
        message_json = json.dumps(message_dict, default=str)
        deserialized = json.loads(message_json)
        
        # Verify the deserialized data matches expected values
        assert deserialized["tier"] == "terrestrial"
        assert deserialized["query"] == "Test query"
        assert deserialized["response"] == "Test response"
        assert "created_at" in deserialized
        assert "updated_at" in deserialized

    def test_message_equality(self, db_session):
        """Test message equality based on ID."""
        # Create and save first message
        message1 = Message(query="Test 1")
        db_session.add(message1)
        db_session.commit()
        
        # Create a second message with the same ID but different content
        message2 = Message(id=message1.id, query="Test 2")
        
        # Create a third message with a different ID
        message3 = Message(query="Test 1")
        db_session.add(message3)
        db_session.commit()
        
        # Test equality - messages with the same ID should be considered equal
        # even if other attributes differ
        assert message1.id == message2.id
        assert message1 != message3  # Different IDs should not be equal
        assert message1 != "not a message"  # Different types should not be equal

    @pytest.mark.parametrize("query_length", [
        10, 100, 1000, 5000
    ])
    def test_message_long_query(self, db_session, query_length):
        """Test that long queries are handled correctly."""
        long_query = "x" * query_length
        message = Message(query=long_query)
        db_session.add(message)
        db_session.commit()
        
        assert len(message.query) == query_length
        
        # Verify retrieval
        db_message = db_session.get(Message, message.id)
        assert db_message.query == long_query
