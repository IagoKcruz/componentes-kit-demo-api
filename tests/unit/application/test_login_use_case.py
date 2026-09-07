import pytest
import bcrypt
from unittest.mock import AsyncMock, patch
from app.application.use_cases.auth.login_use_case import LoginUseCase
from app.application.dtos.auth_dto import LoginDTO
from app.domain.entities.usuario import Usuario
from app.domain.enums.tipo_usuario import TipoUsuario
from app.domain.exceptions.domain_exception import DomainException

CPF_VALIDO = "529.982.247-25"
SENHA = "Senha123!"
SENHA_HASH = bcrypt.hashpw(SENHA.encode(), bcrypt.gensalt()).decode()


@pytest.fixture
def repo():
    return AsyncMock()


@pytest.fixture(autouse=True)
def mock_settings():
    with patch("app.application.use_cases.auth.login_use_case.settings") as s:
        s.jwt_secret = "secret-de-teste"
        s.jwt_algoritmo = "HS256"
        s.jwt_expiracao_minutos = 60
        yield s


async def test_login_usuario_nao_encontrado_levanta_excecao(repo):
    repo.buscar_por_email.return_value = None

    with pytest.raises(DomainException, match="Credenciais inválidas"):
        await LoginUseCase(repo).executar(LoginDTO(email="nao@existe.com", senha=SENHA))


async def test_login_senha_errada_levanta_excecao(repo):
    usuario = Usuario.criar("Test", "a@b.com", CPF_VALIDO, SENHA_HASH, [TipoUsuario.USUARIO])
    repo.buscar_por_email.return_value = usuario

    with pytest.raises(DomainException, match="Credenciais inválidas"):
        await LoginUseCase(repo).executar(LoginDTO(email="a@b.com", senha="senha_errada"))


async def test_login_usuario_inativo_levanta_excecao(repo):
    usuario = Usuario.criar("Test", "a@b.com", CPF_VALIDO, SENHA_HASH, [TipoUsuario.USUARIO])
    usuario.desativar()
    repo.buscar_por_email.return_value = usuario

    with pytest.raises(DomainException, match="Usuário inativo"):
        await LoginUseCase(repo).executar(LoginDTO(email="a@b.com", senha=SENHA))


async def test_login_sucesso_retorna_token(repo):
    usuario = Usuario.criar("Test", "a@b.com", CPF_VALIDO, SENHA_HASH, [TipoUsuario.USUARIO])
    repo.buscar_por_email.return_value = usuario

    resultado = await LoginUseCase(repo).executar(LoginDTO(email="a@b.com", senha=SENHA))

    assert resultado.token_type == "bearer"
    assert len(resultado.access_token) > 0
