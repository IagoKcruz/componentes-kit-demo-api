from typing_extensions import Self

from app.application.contracts.i_unit_of_work import IUnitOfWork
from app.infrastructure.database.session import _sessionFactory
from app.infrastructure.repositories.servico_repository import ServicoRepository
from app.infrastructure.repositories.usuario_repository import UsuarioRepository


class SqlModelUnitOfWork(IUnitOfWork):
    async def __aenter__(self) -> Self:
        self._session = _sessionFactory()
        self.servicos = ServicoRepository(self._session)
        self.usuarios = UsuarioRepository(self._session)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        try:
            if exc_type:
                await self.rollback()
        finally:
            await self._session.close()

    async def commit(self) -> None:
        await self._session.commit()

    async def rollback(self) -> None:
        await self._session.rollback()
