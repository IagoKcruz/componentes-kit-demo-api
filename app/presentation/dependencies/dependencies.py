from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from app.application.contracts.iUnitOfWork import IUnitOfWork
from app.infrastructure.database.session import get_session
from app.infrastructure.database.uow import SqlModelUnitOfWork
from app.infrastructure.repositories.sqlmodel_usuario_repository import SqlModelUsuarioRepository
from app.infrastructure.repositories.sqlmodel_servico_repository import SqlModelServicoRepository


def get_uow() -> IUnitOfWork:
    return SqlModelUnitOfWork()


async def get_usuario_repository(session: AsyncSession = Depends(get_session)) -> SqlModelUsuarioRepository:
    return SqlModelUsuarioRepository(session)


async def get_servico_repository(session: AsyncSession = Depends(get_session)) -> SqlModelServicoRepository:
    return SqlModelServicoRepository(session)
