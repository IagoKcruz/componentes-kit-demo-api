from app.application.contracts.iUnitOfWork import IUnitOfWork
from app.application.dtos.servico_dto import ServicoResponseDTO
from app.application.mappers.servico_mapper import ServicoMapper


class ListarServicosUseCase:
    def __init__(self, uow: IUnitOfWork):
        self._uow = uow

    async def executar(self, apenas_ativos: bool = True) -> list[ServicoResponseDTO]:
        async with self._uow as uow:
            servicos = await uow.servicos.listar(apenas_ativos)
            return [ServicoMapper.para_response_dto(s) for s in servicos]
