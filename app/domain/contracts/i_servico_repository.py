from abc import abstractmethod
from uuid import UUID
from app.domain.contracts.i_repository import IRepository
from app.domain.entities.servico import Servico


class IServicoRepository(IRepository[Servico, UUID]):
    @abstractmethod
    async def listar(self, apenas_ativos: bool = True) -> list[Servico]: ...
