from datetime import datetime, timedelta, timezone

import anyio
import bcrypt
from jose import jwt

from app.application.dtos.auth_dto import LoginDTO, TokenResponseDTO
from app.domain.contracts.i_usuario_repository import IUsuarioRepository
from app.domain.exceptions.autenticacao_error import AutenticacaoError


class LoginUseCase:
    def __init__(
        self,
        usuario_repository: IUsuarioRepository,
        jwt_secret: str,
        jwt_algoritmo: str,
        jwt_expiracao_minutos: int,
    ):
        self._usuarioRepository = usuario_repository
        self._jwtSecret = jwt_secret
        self._jwtAlgoritmo = jwt_algoritmo
        self._jwtExpiracaoMinutos = jwt_expiracao_minutos

    async def executar(self, dto: LoginDTO) -> TokenResponseDTO:
        usuario = await self._usuarioRepository.buscarPorEmail(dto.email)

        if not usuario:
            raise AutenticacaoError("Credenciais inválidas")

        if not usuario.ativo:
            raise AutenticacaoError("Credenciais inválidas")

        senhaOk = await anyio.to_thread.run_sync(
            lambda: bcrypt.checkpw(dto.senha.encode(), usuario.senhaHash.encode())
        )
        if not senhaOk:
            raise AutenticacaoError("Credenciais inválidas")

        expiracao = datetime.now(timezone.utc) + timedelta(minutes=self._jwtExpiracaoMinutos)

        payload = {
            "sub": str(usuario.id),
            "email": str(usuario.email),
            "tipos": [t.value for t in usuario.tipos],
            "exp": expiracao,
        }

        token = jwt.encode(payload, self._jwtSecret, algorithm=self._jwtAlgoritmo)

        return TokenResponseDTO(access_token=token)
