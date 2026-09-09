import anyio
import bcrypt
from datetime import datetime, timedelta, timezone
from jose import jwt
from app.domain.repositories.i_usuario_repository import IUsuarioRepository
from app.domain.exceptions.autenticacao_error import AutenticacaoError
from app.application.dtos.auth_dto import LoginDTO, TokenResponseDTO


class LoginUseCase:
    def __init__(
        self,
        usuario_repository: IUsuarioRepository,
        jwt_secret: str,
        jwt_algoritmo: str,
        jwt_expiracao_minutos: int,
    ):
        self._usuario_repository = usuario_repository
        self._jwt_secret = jwt_secret
        self._jwt_algoritmo = jwt_algoritmo
        self._jwt_expiracao_minutos = jwt_expiracao_minutos

    async def executar(self, dto: LoginDTO) -> TokenResponseDTO:
        usuario = await self._usuario_repository.buscar_por_email(dto.email)

        if not usuario:
            raise AutenticacaoError("Credenciais inválidas")

        senha_ok = await anyio.to_thread.run_sync(
            lambda: bcrypt.checkpw(dto.senha.encode(), usuario.senha_hash.encode())
        )
        if not senha_ok:
            raise AutenticacaoError("Credenciais inválidas")

        if not usuario.ativo:
            raise AutenticacaoError("Usuário inativo")

        expiracao = datetime.now(timezone.utc) + timedelta(minutes=self._jwt_expiracao_minutos)

        payload = {
            "sub": str(usuario.id),
            "email": str(usuario.email),
            "tipos": [t.value for t in usuario.tipos],
            "exp": expiracao,
        }

        token = jwt.encode(payload, self._jwt_secret, algorithm=self._jwt_algoritmo)

        return TokenResponseDTO(access_token=token)
