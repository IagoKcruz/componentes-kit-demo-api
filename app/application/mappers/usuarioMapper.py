from app.domain.entities.usuario import Usuario
from app.application.dtos.usuarioDto import UsuarioResponseDTO


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
