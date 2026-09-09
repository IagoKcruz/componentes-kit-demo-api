from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from app.application.contracts.iUnitOfWork import IUnitOfWork
from app.application.useCases.auth.loginUseCase import LoginUseCase
from app.infrastructure.config import settings
from app.infrastructure.database.session import getSession
from app.infrastructure.database.uow import SqlModelUnitOfWork
from app.infrastructure.repositories.usuarioRepository import UsuarioRepository
from app.infrastructure.repositories.servicoRepository import ServicoRepository


def getUow() -> IUnitOfWork:
    return SqlModelUnitOfWork()


async def getUsuarioRepository(session: AsyncSession = Depends(getSession)) -> UsuarioRepository:
    return UsuarioRepository(session)


async def getServicoRepository(session: AsyncSession = Depends(getSession)) -> ServicoRepository:
    return ServicoRepository(session)


async def getLoginUseCase(repo: UsuarioRepository = Depends(getUsuarioRepository)) -> LoginUseCase:
    return LoginUseCase(
        usuario_repository=repo,
        jwt_secret=settings.jwt_secret,
        jwt_algoritmo=settings.jwt_algoritmo,
        jwt_expiracao_minutos=settings.jwt_expiracao_minutos,
    )
