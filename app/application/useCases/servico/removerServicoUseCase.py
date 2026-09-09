from uuid import UUID
from app.application.contracts.iUnitOfWork import IUnitOfWork
from app.domain.exceptions.entidadeNaoEncontradaError import EntidadeNaoEncontradaError


class RemoverServicoUseCase:
    def __init__(self, uow: IUnitOfWork):
        self._uow = uow

    async def executar(self, servico_id: UUID) -> None:
        async with self._uow as uow:
            servico = await uow.servicos.buscarPorId(servico_id)
            if not servico:
                raise EntidadeNaoEncontradaError("Serviço não encontrado")

            await uow.servicos.deletar(servico_id)
            await uow.commit()
