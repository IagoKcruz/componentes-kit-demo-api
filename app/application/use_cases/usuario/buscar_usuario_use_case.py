from uuid import UUID
from app.application.contracts.iUnitOfWork import IUnitOfWork
from app.domain.exceptions.entidade_nao_encontrada_error import EntidadeNaoEncontradaError
from app.application.dtos.usuario_dto import UsuarioResponseDTO
from app.application.mappers.usuario_mapper import UsuarioMapper


class BuscarUsuarioPorIdUseCase:
    def __init__(self, uow: IUnitOfWork):
        self._uow = uow

    async def executar(self, usuario_id: UUID) -> UsuarioResponseDTO:
        async with self._uow as uow:
            usuario = await uow.usuarios.buscar_por_id(usuario_id)
            if not usuario:
                raise EntidadeNaoEncontradaError("Usuário não encontrado")
            return UsuarioMapper.para_response_dto(usuario)


class ListarUsuariosUseCase:
    def __init__(self, uow: IUnitOfWork):
        self._uow = uow

    async def executar(self) -> list[UsuarioResponseDTO]:
        async with self._uow as uow:
            usuarios = await uow.usuarios.listar()
            return [UsuarioMapper.para_response_dto(u) for u in usuarios]
