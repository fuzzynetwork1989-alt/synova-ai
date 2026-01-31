"""
Main FastAPI application module.

This module creates and configures the FastAPI application instance.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api import router as api_router
from app.database import Base, engine

# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Synova AI API",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables on startup
@app.on_event("startup")
def startup_event():
    """Initialize database tables on app startup."""
    Base.metadata.create_all(bind=engine)

# Include API routers
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/")
async def root():
    """Root endpoint that returns a welcome message."""
    return {"message": f"Welcome to {settings.PROJECT_NAME} API"}
