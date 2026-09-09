from abc import abstractmethod
from uuid import UUID

from app.domain.contracts.i_repository import IRepository
from app.domain.entities.usuario import Usuario


class IUsuarioRepository(IRepository[Usuario, UUID]):
    @abstractmethod
    async def buscarPorEmail(self, email: str) -> Usuario | None: ...

    @abstractmethod
    async def buscarPorCpf(self, cpf: str) -> Usuario | None: ...
