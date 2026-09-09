from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")
ID = TypeVar("ID")


class IRepository(ABC, Generic[T, ID]):
    @abstractmethod
    async def buscarPorId(self, id: ID) -> T | None: ...

    @abstractmethod
    async def listar(self) -> list[T]: ...

    @abstractmethod
    async def salvar(self, entidade: T) -> T: ...

    @abstractmethod
    async def atualizar(self, entidade: T) -> T | None: ...

    @abstractmethod
    async def deletar(self, id: ID) -> None: ...
