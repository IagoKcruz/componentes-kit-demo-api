from uuid import UUID
from app.domain.entities.usuario import Usuario
from app.domain.repositories.i_usuario_repository import IUsuarioRepository
from app.domain.exceptions.domain_exception import DomainException
from app.application.dtos.usuario_dto import UsuarioResponseDTO


def _para_dto(usuario: Usuario) -> UsuarioResponseDTO:
    return UsuarioResponseDTO(
        id=usuario.id,
        nome=usuario.nome,
        email=str(usuario.email),
        cpf=str(usuario.cpf),
        ativo=usuario.ativo,
        tipos=usuario.tipos,
    )


class BuscarUsuarioPorIdUseCase:
    def __init__(self, usuario_repository: IUsuarioRepository):
        self._usuario_repository = usuario_repository

    async def executar(self, id: UUID) -> UsuarioResponseDTO:
        usuario = await self._usuario_repository.buscar_por_id(id)
        if not usuario:
            raise DomainException("Usuário não encontrado")
        return _para_dto(usuario)


class ListarUsuariosUseCase:
    def __init__(self, usuario_repository: IUsuarioRepository):
        self._usuario_repository = usuario_repository

    async def executar(self) -> list[UsuarioResponseDTO]:
        usuarios = await self._usuario_repository.listar()
        return [_para_dto(u) for u in usuarios]
