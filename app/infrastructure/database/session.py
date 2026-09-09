from collections.abc import AsyncIterator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from app.infrastructure.config import settings

_connect_args = {"ssl": "require"} if "supabase.com" in settings.database_url else {}
engine = create_async_engine(settings.database_url, echo=settings.debug, connect_args=_connect_args)
_sessionFactory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def criarTabelas() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def getSession() -> AsyncIterator[AsyncSession]:
    async with _sessionFactory() as session:
        yield session
