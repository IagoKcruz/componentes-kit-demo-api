from app.application.dtos.usuario_dto import UsuarioResponseDTO
from app.domain.entities.usuario import Usuario


class UsuarioMapper:
    @staticmethod
    def paraResponseDto(usuario: Usuario) -> UsuarioResponseDTO:
        return UsuarioResponseDTO(
            id=usuario.id,
            nome=usuario.nome,
            email=str(usuario.email),
            cpf=str(usuario.cpf),
            ativo=usuario.ativo,
            tipos=usuario.tipos,
        )
