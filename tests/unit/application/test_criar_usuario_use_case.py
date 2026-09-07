import pytest
from unittest.mock import AsyncMock
from app.application.use_cases.usuario.criar_usuario_use_case import CriarUsuarioUseCase
from app.application.dtos.usuario_dto import CriarUsuarioDTO
from app.domain.entities.usuario import Usuario
from app.domain.enums.tipo_usuario import TipoUsuario
from app.domain.exceptions.domain_exception import DomainException

CPF_VALIDO = "529.982.247-25"


@pytest.fixture
def repo():
    return AsyncMock()


async def test_criar_usuario_email_duplicado_levanta_excecao(repo):
    repo.buscar_por_email.return_value = object()

    dto = CriarUsuarioDTO(nome="Test", email="a@b.com", cpf=CPF_VALIDO, senha="Senha123", tipos=[TipoUsuario.USUARIO])
    with pytest.raises(DomainException, match="E-mail já cadastrado"):
        await CriarUsuarioUseCase(repo).executar(dto)


async def test_criar_usuario_cpf_duplicado_levanta_excecao(repo):
    repo.buscar_por_email.return_value = None
    repo.buscar_por_cpf.return_value = object()

    dto = CriarUsuarioDTO(nome="Test", email="a@b.com", cpf=CPF_VALIDO, senha="Senha123", tipos=[TipoUsuario.USUARIO])
    with pytest.raises(DomainException, match="CPF já cadastrado"):
        await CriarUsuarioUseCase(repo).executar(dto)


async def test_criar_usuario_retorna_dto(repo):
    repo.buscar_por_email.return_value = None
    repo.buscar_por_cpf.return_value = None

    usuario = Usuario.criar("Test", "a@b.com", CPF_VALIDO, "hash", [TipoUsuario.USUARIO])
    repo.salvar.return_value = usuario

    dto = CriarUsuarioDTO(nome="Test", email="a@b.com", cpf=CPF_VALIDO, senha="Senha123", tipos=[TipoUsuario.USUARIO])
    resultado = await CriarUsuarioUseCase(repo).executar(dto)

    assert resultado.nome == "Test"
    assert TipoUsuario.USUARIO in resultado.tipos
    repo.salvar.assert_awaited_once()
