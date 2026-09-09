from uuid import UUID
from fastapi import APIRouter, Depends, status
from app.application.contracts.iUnitOfWork import IUnitOfWork
from app.application.dtos.usuario_dto import CriarUsuarioDTO, UsuarioResponseDTO
from app.application.use_cases.usuario.criar_usuario_use_case import CriarUsuarioUseCase
from app.application.use_cases.usuario.buscar_usuario_use_case import (
    BuscarUsuarioPorIdUseCase,
    ListarUsuariosUseCase,
)
from app.presentation.dependencies.dependencies import get_uow
from app.presentation.dependencies.auth import verificar_autenticacao

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuários"],
    dependencies=[Depends(verificar_autenticacao)],
)


@router.post("/", response_model=UsuarioResponseDTO, status_code=status.HTTP_201_CREATED)
async def criar_usuario(dto: CriarUsuarioDTO, uow: IUnitOfWork = Depends(get_uow)):
    return await CriarUsuarioUseCase(uow).executar(dto)


@router.get("/", response_model=list[UsuarioResponseDTO])
async def listar_usuarios(uow: IUnitOfWork = Depends(get_uow)):
    return await ListarUsuariosUseCase(uow).executar()


@router.get("/{usuario_id}", response_model=UsuarioResponseDTO)
async def buscar_usuario(usuario_id: UUID, uow: IUnitOfWork = Depends(get_uow)):
    return await BuscarUsuarioPorIdUseCase(uow).executar(usuario_id)
