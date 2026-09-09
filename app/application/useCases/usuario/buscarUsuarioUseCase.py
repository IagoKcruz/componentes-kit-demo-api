from uuid import UUID
from app.application.contracts.iUnitOfWork import IUnitOfWork
from app.domain.exceptions.entidadeNaoEncontradaError import EntidadeNaoEncontradaError
from app.application.dtos.usuarioDto import UsuarioResponseDTO
from app.application.mappers.usuarioMapper import UsuarioMapper


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
