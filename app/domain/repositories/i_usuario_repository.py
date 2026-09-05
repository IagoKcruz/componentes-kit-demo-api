from abc import ABC, abstractmethod
from uuid import UUID
from app.domain.entities.usuario import Usuario


class IUsuarioRepository(ABC):

    @abstractmethod
    async def salvar(self, usuario: Usuario) -> Usuario:
        pass

    @abstractmethod
    async def buscar_por_id(self, id: UUID) -> Usuario | None:
        pass

    @abstractmethod
    async def buscar_por_email(self, email: str) -> Usuario | None:
        pass

    @abstractmethod
    async def buscar_por_cpf(self, cpf: str) -> Usuario | None:
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
