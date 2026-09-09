from abc import ABC, abstractmethod
from app.domain.contracts.iServicoRepository import IServicoRepository
from app.domain.contracts.iUsuarioRepository import IUsuarioRepository


class IUnitOfWork(ABC):
    servicos: IServicoRepository
    usuarios: IUsuarioRepository

    async def __aenter__(self) -> "IUnitOfWork":
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        if exc_type:
            await self.rollback()

    @abstractmethod
    async def commit(self) -> None: ...

    @abstractmethod
    async def rollback(self) -> None: ...
