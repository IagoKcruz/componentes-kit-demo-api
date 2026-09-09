from uuid import UUID
from fastapi import APIRouter, Depends, status
from app.application.contracts.iUnitOfWork import IUnitOfWork
from app.application.dtos.servicoDto import CriarServicoDTO, AtualizarServicoDTO, ServicoResponseDTO
from app.application.useCases.servico.criarServicoUseCase import CriarServicoUseCase
from app.application.useCases.servico.listarServicosUseCase import ListarServicosUseCase
from app.application.useCases.servico.atualizarServicoUseCase import AtualizarServicoUseCase
from app.application.useCases.servico.removerServicoUseCase import RemoverServicoUseCase
from app.application.mappers.servicoMapper import ServicoMapper
from app.domain.exceptions.entidadeNaoEncontradaError import EntidadeNaoEncontradaError
from app.presentation.dependencies.dependencies import getUow
from app.presentation.dependencies.auth import verificarAutenticacao

router = APIRouter(
    prefix="/servicos",
    tags=["Serviços"],
    dependencies=[Depends(verificarAutenticacao)],
)


@router.post("/", response_model=ServicoResponseDTO, status_code=status.HTTP_201_CREATED)
async def criarServico(dto: CriarServicoDTO, uow: IUnitOfWork = Depends(getUow)):
    return await CriarServicoUseCase(uow).executar(dto)


@router.get("/", response_model=list[ServicoResponseDTO])
async def listarServicos(apenas_ativos: bool = True, uow: IUnitOfWork = Depends(getUow)):
    return await ListarServicosUseCase(uow).executar(apenas_ativos)


@router.get("/{servico_id}", response_model=ServicoResponseDTO)
async def buscarServico(servico_id: UUID, uow: IUnitOfWork = Depends(getUow)):
    async with uow as u:
        servico = await u.servicos.buscarPorId(servico_id)
        if not servico:
            raise EntidadeNaoEncontradaError("Serviço não encontrado")
        return ServicoMapper.paraResponseDto(servico)


@router.patch("/{servico_id}", response_model=ServicoResponseDTO)
async def atualizarServico(servico_id: UUID, dto: AtualizarServicoDTO, uow: IUnitOfWork = Depends(getUow)):
    return await AtualizarServicoUseCase(uow).executar(servico_id, dto)


@router.delete("/{servico_id}", status_code=status.HTTP_204_NO_CONTENT)
async def removerServico(servico_id: UUID, uow: IUnitOfWork = Depends(getUow)):
    await RemoverServicoUseCase(uow).executar(servico_id)
