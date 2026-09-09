from uuid import UUID
from fastapi import APIRouter, Depends, status
from app.application.contracts.iUnitOfWork import IUnitOfWork
from app.application.dtos.servico_dto import CriarServicoDTO, AtualizarServicoDTO, ServicoResponseDTO
from app.application.use_cases.servico.criar_servico_use_case import CriarServicoUseCase
from app.application.use_cases.servico.listar_servicos_use_case import ListarServicosUseCase
from app.application.use_cases.servico.atualizar_servico_use_case import AtualizarServicoUseCase
from app.application.use_cases.servico.remover_servico_use_case import RemoverServicoUseCase
from app.application.mappers.servico_mapper import ServicoMapper
from app.domain.exceptions.entidade_nao_encontrada_error import EntidadeNaoEncontradaError
from app.presentation.dependencies.dependencies import get_uow
from app.presentation.dependencies.auth import verificar_autenticacao

router = APIRouter(
    prefix="/servicos",
    tags=["Serviços"],
    dependencies=[Depends(verificar_autenticacao)],
)


@router.post("/", response_model=ServicoResponseDTO, status_code=status.HTTP_201_CREATED)
async def criar_servico(dto: CriarServicoDTO, uow: IUnitOfWork = Depends(get_uow)):
    return await CriarServicoUseCase(uow).executar(dto)


@router.get("/", response_model=list[ServicoResponseDTO])
async def listar_servicos(apenas_ativos: bool = True, uow: IUnitOfWork = Depends(get_uow)):
    return await ListarServicosUseCase(uow).executar(apenas_ativos)


@router.get("/{servico_id}", response_model=ServicoResponseDTO)
async def buscar_servico(servico_id: UUID, uow: IUnitOfWork = Depends(get_uow)):
    async with uow as u:
        servico = await u.servicos.buscar_por_id(servico_id)
        if not servico:
            raise EntidadeNaoEncontradaError("Serviço não encontrado")
        return ServicoMapper.para_response_dto(servico)


@router.patch("/{servico_id}", response_model=ServicoResponseDTO)
async def atualizar_servico(servico_id: UUID, dto: AtualizarServicoDTO, uow: IUnitOfWork = Depends(get_uow)):
    return await AtualizarServicoUseCase(uow).executar(servico_id, dto)


@router.delete("/{servico_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remover_servico(servico_id: UUID, uow: IUnitOfWork = Depends(get_uow)):
    await RemoverServicoUseCase(uow).executar(servico_id)
