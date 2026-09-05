from uuid import UUID
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from app.application.dtos.servico_dto import CriarServicoDTO, ServicoResponseDTO
from app.application.use_cases.servico.criar_servico_use_case import CriarServicoUseCase
from app.application.use_cases.servico.listar_servicos_use_case import ListarServicosUseCase
from app.domain.exceptions.domain_exception import DomainException
from app.presentation.dependencies.dependencies import get_servico_repository
from app.presentation.dependencies.auth import verificar_autenticacao

router = APIRouter(
    prefix="/servicos",
    tags=["Serviços"],
    dependencies=[Depends(verificar_autenticacao)],
)


@router.post("/", response_model=ServicoResponseDTO, status_code=status.HTTP_201_CREATED)
async def criar_servico(dto: CriarServicoDTO, repo=Depends(get_servico_repository)):
    try:
        return await CriarServicoUseCase(repo).executar(dto)
    except DomainException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.mensagem)


@router.get("/", response_model=List[ServicoResponseDTO])
async def listar_servicos(apenas_ativos: bool = True, repo=Depends(get_servico_repository)):
    return await ListarServicosUseCase(repo).executar(apenas_ativos)


@router.get("/{id}", response_model=ServicoResponseDTO)
async def buscar_servico(id: UUID, repo=Depends(get_servico_repository)):
    servico = await repo.buscar_por_id(id)
    if not servico:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Serviço não encontrado")
    return ServicoResponseDTO(
        id=servico.id,
        nome=servico.nome,
        descricao=servico.descricao,
        duracao_minutos=servico.duracao_minutos,
        preco=servico.preco,
        ativo=servico.ativo,
    )
