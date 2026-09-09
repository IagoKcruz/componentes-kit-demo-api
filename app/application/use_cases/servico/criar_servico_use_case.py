from app.domain.entities.servico import Servico
from app.application.contracts.iUnitOfWork import IUnitOfWork
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
                duracao_minutos=dto.duracao_minutos,
                preco=dto.preco,
            )
            salvo = await uow.servicos.salvar(servico)
            await uow.commit()
            return ServicoMapper.para_response_dto(salvo)
