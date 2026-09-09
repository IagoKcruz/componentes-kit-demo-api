from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.application.contracts.i_unit_of_work import IUnitOfWork
from app.application.dtos.usuario_dto import CriarUsuarioDTO, UsuarioResponseDTO
from app.application.use_cases.usuario.buscar_usuario_use_case import (
    BuscarUsuarioPorIdUseCase,
    ListarUsuariosUseCase,
)
from app.application.use_cases.usuario.criar_usuario_use_case import CriarUsuarioUseCase
from app.presentation.dependencies.auth import verificarAutenticacao
from app.presentation.dependencies.dependencies import getUow

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
