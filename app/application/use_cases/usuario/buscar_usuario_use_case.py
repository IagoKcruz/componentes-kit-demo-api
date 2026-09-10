from uuid import UUID

from app.application.contracts.i_unit_of_work import IUnitOfWork
from app.application.dtos.usuario_dto import UsuarioResponseDTO
from app.application.mappers.usuario_mapper import UsuarioMapper
from app.domain.exceptions.entidade_nao_encontrada_error import (
    EntidadeNaoEncontradaError,
)


class BuscarUsuarioPorIdUseCase:
    def __init__(self, uow: IUnitOfWork):
        self._uow = uow

    async def executar(self, usuario_id: UUID) -> UsuarioResponseDTO:
        async with self._uow as uow:
            usuario = await uow.usuarios.buscarPorId(usuario_id)
            if not usuario:
                raise EntidadeNaoEncontradaError("Usuário não encontrado")
            return UsuarioMapper.paraResponseDto(usuario)


class ListarUsuariosUseCase:
    def __init__(self, uow: IUnitOfWork):
        self._uow = uow

    async def executar(self) -> list[UsuarioResponseDTO]:
        async with self._uow as uow:
            usuarios = await uow.usuarios.listar()
            return [UsuarioMapper.paraResponseDto(u) for u in usuarios]
