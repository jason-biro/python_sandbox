import pytest
from typing import AsyncGenerator
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from database import Base, AsyncSessionLocal
from main import app

# 1. Setup isolated in-memory test database architecture.
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"
test_engine = create_async_engine(TEST_DATABASE_URL, echo=False)
TestAsyncSessionLocal = async_sessionmaker(bind=test_engine, expire_on_commit=False, class_=AsyncSession)

@pytest.fixture(scope="function", autouse=True)
async def setup_test_db():
    """Builds a fresh database schema for every isolated test lifecycle."""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Provides a transactional session directly inside verification tests."""
    async with TestAsyncSessionLocal() as session:
        yield session

@pytest.fixture(scope="function")
def test_app(monkeypatch) -> FastAPI:
    """Overrides the production database session factory inside main.py."""
    # This points any references to AsyncSessionLocal in main or scraper to the test DB.
    monkeypatch.setattr("main.AsyncSessionLocal", TestAsyncSessionLocal)
    monkeypatch.setattr("scraper.AsyncSessionLocal", TestAsyncSessionLocal)
    return app
