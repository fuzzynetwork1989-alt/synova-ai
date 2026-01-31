"""
API endpoints for the Synova AI application.

This package contains all the API route handlers and request/response models.
"""
from fastapi import APIRouter

# Import all endpoint modules here
from .endpoints import messages

# Create main API router
router = APIRouter()

# Include all endpoint routers
router.include_router(messages.router)

__all__ = ['router']
