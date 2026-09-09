from uuid import UUID
from app.application.contracts.iUnitOfWork import IUnitOfWork
from app.domain.exceptions.entidadeNaoEncontradaError import EntidadeNaoEncontradaError
from app.application.dtos.servicoDto import AtualizarServicoDTO, ServicoResponseDTO
from app.application.mappers.servicoMapper import ServicoMapper


class AtualizarServicoUseCase:
    def __init__(self, uow: IUnitOfWork):
        self._uow = uow

    async def executar(self, servico_id: UUID, dto: AtualizarServicoDTO) -> ServicoResponseDTO:
        async with self._uow as uow:
            servico = await uow.servicos.buscarPorId(servico_id)
            if not servico:
                raise EntidadeNaoEncontradaError("Serviço não encontrado")

            servico.atualizar(
                nome=dto.nome,
                descricao=dto.descricao,
                duracaoMinutos=dto.duracaoMinutos,
                preco=dto.preco,
            )

            atualizado = await uow.servicos.atualizar(servico)
            if not atualizado:
                raise EntidadeNaoEncontradaError("Serviço não encontrado")

            await uow.commit()
            return ServicoMapper.paraResponseDto(atualizado)
