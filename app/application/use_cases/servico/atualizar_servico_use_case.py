from uuid import UUID
from app.domain.repositories.i_servico_repository import IServicoRepository
from app.domain.exceptions.domain_exception import DomainException
from app.application.dtos.servico_dto import AtualizarServicoDTO, ServicoResponseDTO


class AtualizarServicoUseCase:
    def __init__(self, servico_repository: IServicoRepository):
        self._servico_repository = servico_repository

    async def executar(self, servico_id: UUID, dto: AtualizarServicoDTO) -> ServicoResponseDTO:
        servico = await self._servico_repository.buscar_por_id(servico_id)
        if not servico:
            raise DomainException("Serviço não encontrado")

        servico.atualizar(
            nome=dto.nome,
            descricao=dto.descricao,
            duracao_minutos=dto.duracao_minutos,
            preco=dto.preco,
        )

        atualizado = await self._servico_repository.atualizar(servico)
        if not atualizado:
            raise DomainException("Erro ao atualizar serviço")

        return ServicoResponseDTO(
            id=atualizado.id,
            nome=atualizado.nome,
            descricao=atualizado.descricao,
            duracao_minutos=atualizado.duracao_minutos,
            preco=atualizado.preco,
            ativo=atualizado.ativo,
        )
