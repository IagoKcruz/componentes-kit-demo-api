from abc import abstractmethod
from typing import Generic, Type, TypeVar
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.domain.contracts.i_repository import IRepository

T = TypeVar("T")
M = TypeVar("M")
ID = TypeVar("ID")


class Repository(IRepository[T, ID], Generic[T, M, ID]):
    def __init__(self, session: AsyncSession, modelClass: Type):
        self._session = session
        self._modelClass = modelClass

    def _queryOptions(self) -> list:
        return []

    async def buscarPorId(self, id: ID) -> T | None:
        stmt = select(self._modelClass).where(self._modelClass.id == id)
        opts = self._queryOptions()
        if opts:
            stmt = stmt.options(*opts)
        result = await self._session.exec(stmt)
        model = result.first()
        return self._paraEntidade(model) if model else None

    async def listar(self) -> list[T]:
        stmt = select(self._modelClass)
        opts = self._queryOptions()
        if opts:
            stmt = stmt.options(*opts)
        result = await self._session.exec(stmt)
        return [self._paraEntidade(m) for m in result.all()]

    async def salvar(self, entidade: T) -> T:
        model = self._paraModel(entidade)
        self._session.add(model)
        return entidade

    async def atualizar(self, entidade: T) -> T | None:
        model = await self._session.get(self._modelClass, entidade.id)  # type: ignore[attr-defined]
        if not model:
            return None
        await self._aplicarCampos(entidade, model)
        return entidade

    async def deletar(self, id: ID) -> None:
        model = await self._session.get(self._modelClass, id)
        if model:
            await self._session.delete(model)

    @abstractmethod
    def _paraEntidade(self, model) -> T: ...

    @abstractmethod
    def _paraModel(self, entidade: T): ...

    @abstractmethod
    async def _aplicarCampos(self, entidade: T, model) -> None: ...
