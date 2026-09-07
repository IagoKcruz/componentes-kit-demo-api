from uuid import UUID
from app.domain.repositories.i_servico_repository import IServicoRepository
from app.domain.exceptions.domain_exception import DomainException


class RemoverServicoUseCase:
    def __init__(self, servico_repository: IServicoRepository):
        self._servico_repository = servico_repository

    async def executar(self, id: UUID) -> None:
        servico = await self._servico_repository.buscar_por_id(id)
        if not servico:
            raise DomainException("Serviço não encontrado")

        await self._servico_repository.deletar(id)
