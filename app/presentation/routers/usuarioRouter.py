from uuid import UUID
from fastapi import APIRouter, Depends, status
from app.application.contracts.iUnitOfWork import IUnitOfWork
from app.application.dtos.usuarioDto import CriarUsuarioDTO, UsuarioResponseDTO
from app.application.useCases.usuario.criarUsuarioUseCase import CriarUsuarioUseCase
from app.application.useCases.usuario.buscarUsuarioUseCase import (
    BuscarUsuarioPorIdUseCase,
    ListarUsuariosUseCase,
)
from app.presentation.dependencies.dependencies import getUow
from app.presentation.dependencies.auth import verificarAutenticacao

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuários"],
    dependencies=[Depends(verificarAutenticacao)],
)


@router.post("/", response_model=UsuarioResponseDTO, status_code=status.HTTP_201_CREATED)
async def criarUsuario(dto: CriarUsuarioDTO, uow: IUnitOfWork = Depends(getUow)):
    return await CriarUsuarioUseCase(uow).executar(dto)


@router.get("/", response_model=list[UsuarioResponseDTO])
async def listarUsuarios(uow: IUnitOfWork = Depends(getUow)):
    return await ListarUsuariosUseCase(uow).executar()


@router.get("/{usuario_id}", response_model=UsuarioResponseDTO)
async def buscarUsuario(usuario_id: UUID, uow: IUnitOfWork = Depends(getUow)):
    return await BuscarUsuarioPorIdUseCase(uow).executar(usuario_id)
