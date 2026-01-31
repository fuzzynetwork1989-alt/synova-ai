"""
Message-related Pydantic models.

This module contains Pydantic models for message-related operations.
"""
from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class MessageTier(str, Enum):
    TERRESTRIAL = "terrestrial"
    CELESTIAL = "celestial"
    GALACTIC = "galactic"


class MessageBase(BaseModel):
    """Base model for message with common attributes."""
    model_config = ConfigDict(from_attributes=True)

    tier: MessageTier = MessageTier.TERRESTRIAL
    query: str = Field(..., description="The user's input query")


class MessageCreate(MessageBase):
    """Model for creating a new message."""
    pass


class MessageUpdate(BaseModel):
    """Model for updating a message."""
    response: str


class MessageResponse(MessageBase):
    """Model for message response."""
    id: int
    response: Optional[str] = None
    created_at: datetime
    updated_at: datetime
