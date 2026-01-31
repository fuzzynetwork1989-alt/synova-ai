"""
API endpoints for message operations.

This module contains the FastAPI route handlers for message-related operations.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.message import Message
from app.schemas.message import MessageCreate, MessageResponse

router = APIRouter(prefix="/messages", tags=["messages"])


@router.get("/", response_model=List[MessageResponse])
def list_messages(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    """Retrieve a list of messages with pagination."""
    messages = db.query(Message).offset(skip).limit(limit).all()
    return messages


@router.post("/", response_model=MessageResponse, status_code=201)
def create_message(
    message: MessageCreate,
    db: Session = Depends(get_db)
):
    """Create a new message."""
    db_message = Message(**message.model_dump())
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message


@router.get("/{message_id}", response_model=MessageResponse)
def get_message(
    message_id: int, 
    db: Session = Depends(get_db)
):
    """Retrieve a specific message by ID."""
    message = db.query(Message).filter(Message.id == message_id).first()
    if message is None:
        raise HTTPException(status_code=404, detail="Message not found")
    return message
