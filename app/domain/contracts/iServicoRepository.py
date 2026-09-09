from abc import ABC, abstractmethod
from uuid import UUID
from app.domain.entities.servico import Servico


class IServicoRepository(ABC):

    @abstractmethod
    async def salvar(self, servico: Servico) -> Servico:
        pass

    @abstractmethod
    async def buscarPorId(self, id: UUID) -> Servico | None:
        pass

    @abstractmethod
    async def listar(self, apenas_ativos: bool = True) -> list[Servico]:
        pass

    @abstractmethod
    async def atualizar(self, servico: Servico) -> Servico | None:
        pass

    @abstractmethod
    async def deletar(self, id: UUID) -> None:
        pass
