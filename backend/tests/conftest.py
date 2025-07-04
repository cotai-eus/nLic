import asyncio
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import NullPool

from app.main import app
from app.core.config import settings
from app.db.base_class import Base
from app.db.session import get_async_session

# Use a separate test database URL if provided, otherwise append _test to the main DB URL
TEST_DATABASE_URL = settings.TEST_DATABASE_URL or f"{settings.DATABASE_URL}_test"

# Create an async engine for the test database
test_engine = create_async_engine(TEST_DATABASE_URL, poolclass=NullPool)
TestSessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=test_engine, class_=AsyncSession)

@pytest.fixture(scope="session")
async def db_session():
    """Fixture that provides a clean database for each test session."""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with TestSessionLocal() as session:
        yield session

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture(scope="function")
async def session_override(db_session: AsyncSession):
    """Override the get_async_session dependency for tests."""
    app.dependency_overrides[get_async_session] = lambda: db_session
    yield
    app.dependency_overrides.clear()

@pytest.fixture(scope="session")
async def client():
    """Fixture that provides an asynchronous test client for the FastAPI application."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.fixture(scope="session")
def event_loop():
    """Fixture that provides the default event loop for pytest-asyncio."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
