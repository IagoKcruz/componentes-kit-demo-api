from abc import ABC, abstractmethod
from uuid import UUID
from app.domain.entities.usuario import Usuario


class IUsuarioRepository(ABC):

    @abstractmethod
    async def salvar(self, usuario: Usuario) -> Usuario:
        pass

    @abstractmethod
    async def buscarPorId(self, id: UUID) -> Usuario | None:
        pass

    @abstractmethod
    async def buscarPorEmail(self, email: str) -> Usuario | None:
        pass

    @abstractmethod
    async def buscarPorCpf(self, cpf: str) -> Usuario | None:
        pass

    @abstractmethod
    async def listar(self) -> list[Usuario]:
        pass

    @abstractmethod
    async def atualizar(self, usuario: Usuario) -> Usuario | None:
        pass

    @abstractmethod
    async def deletar(self, id: UUID) -> None:
        pass
