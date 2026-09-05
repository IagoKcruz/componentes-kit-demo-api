import bcrypt
from datetime import datetime, timedelta, timezone
from jose import jwt
from app.domain.repositories.i_usuario_repository import IUsuarioRepository
from app.domain.exceptions.domain_exception import DomainException
from app.application.dtos.auth_dto import LoginDTO, TokenResponseDTO
from app.infrastructure.config import settings


class LoginUseCase:
    def __init__(self, usuario_repository: IUsuarioRepository):
        self._usuario_repository = usuario_repository

    async def executar(self, dto: LoginDTO) -> TokenResponseDTO:
        usuario = await self._usuario_repository.buscar_por_email(dto.email)

        # mensagem genérica para não revelar se o email existe
        if not usuario or not bcrypt.checkpw(dto.senha.encode(), usuario.senha_hash.encode()):
            raise DomainException("Credenciais inválidas")

        if not usuario.ativo:
            raise DomainException("Usuário inativo")

        expiracao = datetime.now(timezone.utc) + timedelta(minutes=settings.jwt_expiracao_minutos)

        payload = {
            "sub": str(usuario.id),
            "email": str(usuario.email),
            "tipos": [t.value for t in usuario.tipos],
            "exp": expiracao,
        }

        token = jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algoritmo)

        return TokenResponseDTO(access_token=token)
