from uuid import UUID
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.domain.contracts.i_servico_repository import IServicoRepository
from app.domain.entities.servico import Servico
from app.infrastructure.database.models.servico_model import ServicoModel
from app.infrastructure.repositories.repository import Repository


class ServicoRepository(Repository[Servico, ServicoModel, UUID], IServicoRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, ServicoModel)

    def _paraEntidade(self, model: ServicoModel) -> Servico:
        return Servico(
            id=model.id,
            nome=model.nome,
            descricao=model.descricao,
            duracaoMinutos=model.duracao_minutos,
            preco=model.preco,
            ativo=model.ativo,
        )

    def _paraModel(self, servico: Servico) -> ServicoModel:
        return ServicoModel(
            id=servico.id,
            nome=servico.nome,
            descricao=servico.descricao,
            duracao_minutos=servico.duracaoMinutos,
            preco=servico.preco,
            ativo=servico.ativo,
        )

    async def _aplicarCampos(self, servico: Servico, model: ServicoModel) -> None:
        model.nome = servico.nome
        model.descricao = servico.descricao
        model.duracao_minutos = servico.duracaoMinutos
        model.preco = servico.preco
        model.ativo = servico.ativo

    async def listar(self, apenas_ativos: bool = True) -> list[Servico]:
        stmt = select(ServicoModel)
        if apenas_ativos:
            stmt = stmt.where(ServicoModel.ativo.is_(True))  # type: ignore[attr-defined]
        result = await self._session.exec(stmt)
        return [self._paraEntidade(m) for m in result.all()]
