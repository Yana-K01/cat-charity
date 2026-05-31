from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.base import Base
from app.core.config import settings
import app.models  # noqa: F401, E402


__all__ = (
    'Base',
    'AsyncSessionLocal',
    'engine',
    'get_async_session',
)

engine = create_async_engine(settings.database_url, future=True)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
