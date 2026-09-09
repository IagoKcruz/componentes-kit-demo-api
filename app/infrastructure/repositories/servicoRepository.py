from uuid import UUID
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.domain.entities.servico import Servico
from app.domain.contracts.iServicoRepository import IServicoRepository
from app.infrastructure.database.models.servicoModel import ServicoModel


class SqlModelServicoRepository(IServicoRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def salvar(self, servico: Servico) -> Servico:
        model = ServicoModel(
            id=servico.id,
            nome=servico.nome,
            descricao=servico.descricao,
            duracao_minutos=servico.duracaoMinutos,
            preco=servico.preco,
            ativo=servico.ativo,
        )
        self._session.add(model)
        return servico

    async def buscarPorId(self, id: UUID) -> Servico | None:
        model = await self._session.get(ServicoModel, id)
        return self._paraEntidade(model) if model else None

    async def listar(self, apenas_ativos: bool = True) -> list[Servico]:
        stmt = select(ServicoModel)
        if apenas_ativos:
            stmt = stmt.where(ServicoModel.ativo.is_(True))  # type: ignore[attr-defined]
        result = await self._session.exec(stmt)
        return [self._paraEntidade(m) for m in result.all()]

    async def atualizar(self, servico: Servico) -> Servico | None:
        model = await self._session.get(ServicoModel, servico.id)
        if not model:
            return None
        model.nome = servico.nome
        model.descricao = servico.descricao
        model.duracao_minutos = servico.duracaoMinutos
        model.preco = servico.preco
        model.ativo = servico.ativo
        return servico

    async def deletar(self, id: UUID) -> None:
        model = await self._session.get(ServicoModel, id)
        if model:
            await self._session.delete(model)

    def _paraEntidade(self, model: ServicoModel) -> Servico:
        return Servico(
            id=model.id,
            nome=model.nome,
            descricao=model.descricao,
            duracaoMinutos=model.duracao_minutos,
            preco=model.preco,
            ativo=model.ativo,
        )
