from collections.abc import AsyncIterator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlmodel import SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.infrastructure.config import settings

engine = create_async_engine(settings.database_url, echo=settings.debug)
_session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def criar_tabelas() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def seed_tipos_usuario() -> None:
    from app.infrastructure.database.models.usuario_model import TipoUsuarioModel

    tipos = ["admin", "usuario", "funcionario"]
    async with _session_factory() as session:
        for nome in tipos:
            result = await session.exec(
                select(TipoUsuarioModel).where(TipoUsuarioModel.nome == nome)
            )
            if not result.first():
                session.add(TipoUsuarioModel(nome=nome))
        await session.commit()


async def get_session() -> AsyncIterator[AsyncSession]:
    async with _session_factory() as session:
        yield session
