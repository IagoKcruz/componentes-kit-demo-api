from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from app.application.dtos.usuario_dto import CriarUsuarioDTO, UsuarioResponseDTO
from app.application.use_cases.usuario.criar_usuario_use_case import CriarUsuarioUseCase
from app.application.use_cases.usuario.buscar_usuario_use_case import (
    BuscarUsuarioPorIdUseCase,
    ListarUsuariosUseCase,
)
from app.domain.exceptions.domain_exception import DomainException
from app.domain.repositories.i_usuario_repository import IUsuarioRepository
from app.presentation.dependencies.dependencies import get_usuario_repository
from app.presentation.dependencies.auth import verificar_autenticacao

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuários"],
    dependencies=[Depends(verificar_autenticacao)],
)


@router.post("/", response_model=UsuarioResponseDTO, status_code=status.HTTP_201_CREATED)
async def criar_usuario(dto: CriarUsuarioDTO, repo: IUsuarioRepository = Depends(get_usuario_repository)):
    try:
        return await CriarUsuarioUseCase(repo).executar(dto)
    except DomainException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.mensagem)


@router.get("/", response_model=list[UsuarioResponseDTO])
async def listar_usuarios(repo: IUsuarioRepository = Depends(get_usuario_repository)):
    return await ListarUsuariosUseCase(repo).executar()


@router.get("/{usuario_id}", response_model=UsuarioResponseDTO)
async def buscar_usuario(usuario_id: UUID, repo: IUsuarioRepository = Depends(get_usuario_repository)):
    try:
        return await BuscarUsuarioPorIdUseCase(repo).executar(usuario_id)
    except DomainException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.mensagem)
