from abc import ABC, abstractmethod

from typing_extensions import Self

from app.domain.contracts.i_servico_repository import IServicoRepository
from app.domain.contracts.i_usuario_repository import IUsuarioRepository


class IUnitOfWork(ABC):
    servicos: IServicoRepository
    usuarios: IUsuarioRepository

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        if exc_type:
            await self.rollback()

    @abstractmethod
    async def commit(self) -> None: ...

    @abstractmethod
    async def rollback(self) -> None: ...
