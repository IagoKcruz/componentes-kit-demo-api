from app.domain.entities.servico import Servico
from app.application.contracts.iUnitOfWork import IUnitOfWork
from app.application.dtos.servicoDto import CriarServicoDTO, ServicoResponseDTO
from app.application.mappers.servicoMapper import ServicoMapper


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
