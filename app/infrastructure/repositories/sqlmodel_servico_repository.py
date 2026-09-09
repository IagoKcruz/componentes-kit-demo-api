from uuid import UUID
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.domain.entities.servico import Servico
from app.domain.repositories.i_servico_repository import IServicoRepository
from app.infrastructure.database.models.servico_model import ServicoModel


class SqlModelServicoRepository(IServicoRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def salvar(self, servico: Servico) -> Servico:
        model = ServicoModel(
            id=servico.id,
            nome=servico.nome,
            descricao=servico.descricao,
            duracao_minutos=servico.duracao_minutos,
            preco=servico.preco,
            ativo=servico.ativo,
        )
        self._session.add(model)
        return servico

    async def buscar_por_id(self, id: UUID) -> Servico | None:
        model = await self._session.get(ServicoModel, id)
        return self._para_entidade(model) if model else None

    async def listar(self, apenas_ativos: bool = True) -> list[Servico]:
        stmt = select(ServicoModel)
        if apenas_ativos:
            stmt = stmt.where(ServicoModel.ativo.is_(True))  # type: ignore[attr-defined]
        result = await self._session.exec(stmt)
        return [self._para_entidade(m) for m in result.all()]

    async def atualizar(self, servico: Servico) -> Servico | None:
        model = await self._session.get(ServicoModel, servico.id)
        if not model:
            return None
        model.nome = servico.nome
        model.descricao = servico.descricao
        model.duracao_minutos = servico.duracao_minutos
        model.preco = servico.preco
        model.ativo = servico.ativo
        return servico

    async def deletar(self, id: UUID) -> None:
        model = await self._session.get(ServicoModel, id)
        if model:
            await self._session.delete(model)

    def _para_entidade(self, model: ServicoModel) -> Servico:
        return Servico(
            id=model.id,
            nome=model.nome,
            descricao=model.descricao,
            duracao_minutos=model.duracao_minutos,
            preco=model.preco,
            ativo=model.ativo,
        )
