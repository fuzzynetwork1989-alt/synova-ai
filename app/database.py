"""
Database configuration and session management.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base

# Create the SQLAlchemy engine
SQLALCHEMY_DATABASE_URL = "sqlite:///./synova.db"

# Create a new engine with future=True for SQLAlchemy 2.0
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    future=True
)

# Create a scoped session factory with future=True
SessionLocal = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)
)

# Base class for models
Base = declarative_base()

# Dependency to get DB session
def get_db():
    """Get a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
