"""
Pytest configuration and fixtures for database testing.
"""
from __future__ import annotations

import contextlib
import os
import tempfile
from typing import AsyncGenerator, Generator

import pytest
from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import Session, sessionmaker

from app.database import Base, get_db
from app.models.message import Message

# Test database configuration
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"
TEST_SYNC_DATABASE_URL = "sqlite:///:memory:"

# Enable SQLAlchemy statement logging for debugging
# import logging
# logging.basicConfig()
# logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

# Helper function to create test database tables

def create_tables(engine: Engine) -> None:
    """Create all database tables."""
    Base.metadata.create_all(bind=engine)


def drop_tables(engine: Engine) -> None:
    """Drop all database tables."""
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="session")
def engine():
    """Create a synchronous database engine for testing."""
    engine = create_engine(
        TEST_SYNC_DATABASE_URL,
        connect_args={"check_same_thread": False},
        echo=False,
        future=True
    )
    return engine


@pytest.fixture(scope="session")
def async_engine():
    """Create an async database engine for testing."""
    return create_async_engine(
        TEST_DATABASE_URL,
        echo=False,
        future=True
    )


@pytest.fixture(scope="session")
def setup_database(engine):
    """Set up the test database with all tables."""
    create_tables(engine)
    yield
    drop_tables(engine)


@pytest.fixture
def db_session(engine, setup_database) -> Generator[Session, None, None]:
    """
    Create a new database session with a rollback at the end of the test.
    
    This fixture provides a transaction that's rolled back after each test,
    ensuring test isolation.
    """
    connection = engine.connect()
    transaction = connection.begin()
    
    # Create a session with the connection
    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=connection,
        future=True
    )
    
    # Create a scoped session
    session = TestingSessionLocal()
    
    # Override the get_db dependency
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    
    # Apply the override
    import app.main
    app.main.app.dependency_overrides[get_db] = override_get_db
    
    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()
        # Clear overrides
        app.main.app.dependency_overrides.clear()


@pytest.fixture
async def async_db(async_engine, setup_database) -> AsyncGenerator[AsyncSession, None]:
    """Async database session fixture for testing async code."""
    async with async_engine.connect() as conn:
        await conn.begin()
        await conn.begin_nested()
        
        async_session = sessionmaker(
            bind=conn,
            class_=AsyncSession,
            expire_on_commit=False,
            future=True
        )
        
        session = async_session()
        
        @event.listens_for(session.sync_session, 'after_transaction_end')
        def end_savepoint(session, transaction):
            if conn.closed:
                return
            if not conn.in_nested_transaction():
                conn.sync_connection.begin_nested()
        
        try:
            yield session
        finally:
            await session.close()
            await conn.rollback()


# Add a test client fixture if you're using FastAPI
@pytest.fixture
def test_client():
    """Create a test client for FastAPI application."""
    from fastapi.testclient import TestClient
    from app.main import app
    
    with TestClient(app) as client:
        yield client
