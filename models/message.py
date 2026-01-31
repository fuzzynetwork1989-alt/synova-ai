from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from typing import Optional
from database import Base

class Message(Base):
    """
    Message model representing messages in the system.
    
    Attributes:
        id: Primary key
        content: The message content
        created_at: Timestamp when the message was created
    """
    __tablename__ = "messages"
    
    id: int = Column(Integer, primary_key=True, index=True)
    content: str = Column(String(1000), index=True, nullable=False)
    created_at: datetime = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    def __repr__(self) -> str:
        return f"<Message(id={self.id}, created_at={self.created_at})>"
