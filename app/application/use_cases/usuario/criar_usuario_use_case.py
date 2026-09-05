import bcrypt
from app.domain.entities.usuario import Usuario
from app.domain.repositories.i_usuario_repository import IUsuarioRepository
from app.domain.exceptions.domain_exception import DomainException
from app.application.dtos.usuario_dto import CriarUsuarioDTO, UsuarioResponseDTO


class CriarUsuarioUseCase:
    def __init__(self, usuario_repository: IUsuarioRepository):
        self._usuario_repository = usuario_repository

    async def executar(self, dto: CriarUsuarioDTO) -> UsuarioResponseDTO:
        if await self._usuario_repository.buscar_por_email(dto.email):
            raise DomainException("E-mail já cadastrado")

        if await self._usuario_repository.buscar_por_cpf(dto.cpf):
            raise DomainException("CPF já cadastrado")

        senha_hash = bcrypt.hashpw(dto.senha.encode(), bcrypt.gensalt()).decode()

        usuario = Usuario.criar(
            nome=dto.nome,
            email=dto.email,
            cpf=dto.cpf,
            senha_hash=senha_hash,
            tipos=dto.tipos,
        )

        salvo = await self._usuario_repository.salvar(usuario)

        return UsuarioResponseDTO(
            id=salvo.id,
            nome=salvo.nome,
            email=str(salvo.email),
            cpf=str(salvo.cpf),
            ativo=salvo.ativo,
            tipos=salvo.tipos,
        )
