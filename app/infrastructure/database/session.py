from collections.abc import AsyncIterator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from app.infrastructure.config import settings

engine = create_async_engine(settings.database_url, echo=settings.debug)
_session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def criar_tabelas() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncIterator[AsyncSession]:
    async with _session_factory() as session:
        yield session
