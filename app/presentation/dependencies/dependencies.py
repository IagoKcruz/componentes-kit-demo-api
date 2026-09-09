from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from app.application.contracts.iUnitOfWork import IUnitOfWork
from app.application.use_cases.auth.login_use_case import LoginUseCase
from app.infrastructure.config import settings
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


async def get_login_use_case(repo: SqlModelUsuarioRepository = Depends(get_usuario_repository)) -> LoginUseCase:
    return LoginUseCase(
        usuario_repository=repo,
        jwt_secret=settings.jwt_secret,
        jwt_algoritmo=settings.jwt_algoritmo,
        jwt_expiracao_minutos=settings.jwt_expiracao_minutos,
    )
