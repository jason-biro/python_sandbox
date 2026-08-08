from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

# Creates a physical 'nhl_data.db' SQLite file in your project root folder.
DATABASE_URL = "sqlite+aiosqlite:///nhl_data.db"

# Initializes the Engine
engine = create_async_engine(DATABASE_URL, echo=False)

# Configures the Async DbContext Factory.
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

class Base(DeclarativeBase):
    pass