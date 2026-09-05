from typing import List
from app.domain.repositories.i_servico_repository import IServicoRepository
from app.application.dtos.servico_dto import ServicoResponseDTO


class ListarServicosUseCase:
    def __init__(self, servico_repository: IServicoRepository):
        self._servico_repository = servico_repository

    async def executar(self, apenas_ativos: bool = True) -> List[ServicoResponseDTO]:
        servicos = await self._servico_repository.listar(apenas_ativos)
        return [
            ServicoResponseDTO(
                id=s.id,
                nome=s.nome,
                descricao=s.descricao,
                duracao_minutos=s.duracao_minutos,
                preco=s.preco,
                ativo=s.ativo,
            )
            for s in servicos
        ]
