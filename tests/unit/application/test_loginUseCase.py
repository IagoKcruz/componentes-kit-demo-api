import pytest
import bcrypt
from unittest.mock import AsyncMock
from app.application.useCases.auth.loginUseCase import LoginUseCase
from app.application.dtos.authDto import LoginDTO
from app.domain.entities.usuario import Usuario
from app.domain.enums.tipoUsuario import TipoUsuario
from app.domain.exceptions.domainException import DomainException

CPF_VALIDO = "529.982.247-25"
SENHA = "Senha123!"
SENHA_HASH = bcrypt.hashpw(SENHA.encode(), bcrypt.gensalt()).decode()

JWT_SECRET = "secret-de-teste"
JWT_ALGORITMO = "HS256"
JWT_EXPIRACAO = 60


@pytest.fixture
def repo():
    return AsyncMock()


def _use_case(repo):
    return LoginUseCase(repo, JWT_SECRET, JWT_ALGORITMO, JWT_EXPIRACAO)


async def test_login_usuario_nao_encontrado_levanta_excecao(repo):
    repo.buscarPorEmail.return_value = None

    with pytest.raises(DomainException, match="Credenciais inválidas"):
        await _use_case(repo).executar(LoginDTO(email="nao@existe.com", senha=SENHA))


async def test_login_senha_errada_levanta_excecao(repo):
    usuario = Usuario.criar("Test", "a@b.com", CPF_VALIDO, SENHA_HASH, [TipoUsuario.USUARIO])
    repo.buscarPorEmail.return_value = usuario

    with pytest.raises(DomainException, match="Credenciais inválidas"):
        await _use_case(repo).executar(LoginDTO(email="a@b.com", senha="senha_errada"))


async def test_login_usuario_inativo_levanta_excecao(repo):
    usuario = Usuario.criar("Test", "a@b.com", CPF_VALIDO, SENHA_HASH, [TipoUsuario.USUARIO])
    usuario.desativar()
    repo.buscarPorEmail.return_value = usuario

    with pytest.raises(DomainException, match="Usuário inativo"):
        await _use_case(repo).executar(LoginDTO(email="a@b.com", senha=SENHA))


async def test_login_sucesso_retorna_token(repo):
    usuario = Usuario.criar("Test", "a@b.com", CPF_VALIDO, SENHA_HASH, [TipoUsuario.USUARIO])
    repo.buscarPorEmail.return_value = usuario

    resultado = await _use_case(repo).executar(LoginDTO(email="a@b.com", senha=SENHA))

    assert resultado.tokenType == "bearer"
    assert len(resultado.accessToken) > 0
