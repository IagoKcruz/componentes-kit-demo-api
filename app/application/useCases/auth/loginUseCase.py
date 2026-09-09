import anyio
import bcrypt
from datetime import datetime, timedelta, timezone
from jose import jwt
from app.domain.contracts.iUsuarioRepository import IUsuarioRepository
from app.domain.exceptions.autenticacaoError import AutenticacaoError
from app.application.dtos.authDto import LoginDTO, TokenResponseDTO


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

        senhaOk = await anyio.to_thread.run_sync(
            lambda: bcrypt.checkpw(dto.senha.encode(), usuario.senhaHash.encode())
        )
        if not senhaOk:
            raise AutenticacaoError("Credenciais inválidas")

        if not usuario.ativo:
            raise AutenticacaoError("Usuário inativo")

        expiracao = datetime.now(timezone.utc) + timedelta(minutes=self._jwtExpiracaoMinutos)

        payload = {
            "sub": str(usuario.id),
            "email": str(usuario.email),
            "tipos": [t.value for t in usuario.tipos],
            "exp": expiracao,
        }

        token = jwt.encode(payload, self._jwtSecret, algorithm=self._jwtAlgoritmo)

        return TokenResponseDTO(accessToken=token)
