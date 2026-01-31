from sqlalchemy import Column, Integer, String, DateTime, Text
from database import Base
from datetime import datetime
from typing import Optional


class Message(Base):
    """Represents a message in the Synova AI system.
    
    This model stores both user queries and system responses, along with metadata
    like the message tier and timestamp.
    
    Attributes:
        id: Primary key for the message record
        tier: Category or classification of the message (e.g., 'info', 'warning', 'error')
        query: The user's input or question
        response: The system's generated response
        timestamp: When the message was created (automatically set to UTC now)
    """
    __tablename__ = "messages"

    id: int = Column(Integer, primary_key=True, index=True)
    tier: str = Column(String, index=True, nullable=False, doc="Message category/classification")
    query: str = Column(Text, nullable=False, doc="The user's input query")
    response: Optional[str] = Column(Text, nullable=True, doc="System's response to the query")
    timestamp: datetime = Column(DateTime, default=datetime.utcnow, 
                              doc="When the message was created (UTC)")

    def __repr__(self) -> str:
        """Return a string representation of the Message instance.
        
        Returns:
            str: A string containing the message ID, tier, and timestamp
        """
        return f"<Message(id={self.id}, tier='{self.tier}', timestamp='{self.timestamp}')>"