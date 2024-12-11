import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from db.engine import Base, get_async_db

from main import app

SQLALCHEMY_TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"


@pytest.fixture(scope="session")
async def async_engine():
    """Create an async engine for the test database."""
    engine = create_async_engine(
        SQLALCHEMY_TEST_DATABASE_URL,
        future=True,
        echo=False
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest.fixture(scope="function")
async def async_session(async_engine):
    """Provide an asynchronous database session for tests."""
    Session = sessionmaker(
        bind=async_engine,
        class_=AsyncSession,
        expire_on_commit=False
    )
    async with Session() as session:
        yield session


@pytest.fixture(scope="function")
def override_get_async_db(async_session):
    """"Override the FastAPI dependency for the async database session."""
    async def _override():
        yield async_session
    app.dependency_overrides[get_async_db] = _override
    yield
    app.dependency_overrides.pop(get_async_db)


@pytest.fixture(autouse=True)
async def clean_database(async_session: AsyncSession):
    """Delete all data from the database."""
    for table in reversed(Base.metadata.sorted_tables):
        await async_session.execute(text(f"DELETE FROM {table.name}"))
    await async_session.commit()
