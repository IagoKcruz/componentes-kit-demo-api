from app.domain.entities.servico import Servico
from app.domain.repositories.i_servico_repository import IServicoRepository
from app.application.dtos.servico_dto import CriarServicoDTO, ServicoResponseDTO


class CriarServicoUseCase:
    def __init__(self, servico_repository: IServicoRepository):
        self._servico_repository = servico_repository

    async def executar(self, dto: CriarServicoDTO) -> ServicoResponseDTO:
        servico = Servico.criar(
            nome=dto.nome,
            descricao=dto.descricao,
            duracao_minutos=dto.duracao_minutos,
            preco=dto.preco,
        )

        salvo = await self._servico_repository.salvar(servico)

        return ServicoResponseDTO(
            id=salvo.id,
            nome=salvo.nome,
            descricao=salvo.descricao,
            duracao_minutos=salvo.duracao_minutos,
            preco=salvo.preco,
            ativo=salvo.ativo,
        )
