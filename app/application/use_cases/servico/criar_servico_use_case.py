from app.domain.entities.servico import Servico
from app.application.contracts.i_unit_of_work import IUnitOfWork
from app.application.dtos.servico_dto import CriarServicoDTO, ServicoResponseDTO
from app.application.mappers.servico_mapper import ServicoMapper


class CriarServicoUseCase:
    def __init__(self, uow: IUnitOfWork):
        self._uow = uow

    async def executar(self, dto: CriarServicoDTO) -> ServicoResponseDTO:
        async with self._uow as uow:
            servico = Servico.criar(
                nome=dto.nome,
                descricao=dto.descricao,
                duracaoMinutos=dto.duracaoMinutos,
                preco=dto.preco,
            )
            salvo = await uow.servicos.salvar(servico)
            await uow.commit()
            return ServicoMapper.paraResponseDto(salvo)
