import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.models import Base
from src.service import EventService

# Use SQLite in-memory database for testing
TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(TEST_DATABASE_URL)

# Create a new session factory for tests
TestingSessionLocal = sessionmaker(bind=engine, expire_on_commit=False)


@pytest.fixture(scope="function")
def db_session():
    """Fixture to provide a temporary database session for tests."""
    # Create all tables in the test database
    Base.metadata.create_all(engine)

    session = TestingSessionLocal()
    yield session  # Provide the session to the test

    # Rollback and remove all data after test
    session.rollback()
    session.close()
    Base.metadata.drop_all(engine)  # Cleanup after test


@pytest.fixture
def event_service(db_session):
    """Provides an instance of EventService."""
    return EventService(db_session)

