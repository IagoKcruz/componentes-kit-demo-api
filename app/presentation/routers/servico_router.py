from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from app.application.dtos.servico_dto import CriarServicoDTO, AtualizarServicoDTO, ServicoResponseDTO
from app.application.use_cases.servico.criar_servico_use_case import CriarServicoUseCase
from app.application.use_cases.servico.listar_servicos_use_case import ListarServicosUseCase
from app.application.use_cases.servico.atualizar_servico_use_case import AtualizarServicoUseCase
from app.application.use_cases.servico.remover_servico_use_case import RemoverServicoUseCase
from app.domain.exceptions.domain_exception import DomainException
from app.domain.repositories.i_servico_repository import IServicoRepository
from app.presentation.dependencies.dependencies import get_servico_repository
from app.presentation.dependencies.auth import verificar_autenticacao

router = APIRouter(
    prefix="/servicos",
    tags=["Serviços"],
    dependencies=[Depends(verificar_autenticacao)],
)


@router.post("/", response_model=ServicoResponseDTO, status_code=status.HTTP_201_CREATED)
async def criar_servico(dto: CriarServicoDTO, repo: IServicoRepository = Depends(get_servico_repository)):
    try:
        return await CriarServicoUseCase(repo).executar(dto)
    except DomainException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.mensagem)


@router.get("/", response_model=list[ServicoResponseDTO])
async def listar_servicos(apenas_ativos: bool = True, repo: IServicoRepository = Depends(get_servico_repository)):
    return await ListarServicosUseCase(repo).executar(apenas_ativos)


@router.get("/{servico_id}", response_model=ServicoResponseDTO)
async def buscar_servico(servico_id: UUID, repo: IServicoRepository = Depends(get_servico_repository)):
    servico = await repo.buscar_por_id(servico_id)
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


@router.patch("/{servico_id}", response_model=ServicoResponseDTO)
async def atualizar_servico(servico_id: UUID, dto: AtualizarServicoDTO, repo: IServicoRepository = Depends(get_servico_repository)):
    try:
        return await AtualizarServicoUseCase(repo).executar(servico_id, dto)
    except DomainException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.mensagem)


@router.delete("/{servico_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remover_servico(servico_id: UUID, repo: IServicoRepository = Depends(get_servico_repository)):
    try:
        await RemoverServicoUseCase(repo).executar(servico_id)
    except DomainException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.mensagem)
