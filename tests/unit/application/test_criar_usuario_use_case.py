import pytest
from unittest.mock import AsyncMock
from app.application.use_cases.usuario.criar_usuario_use_case import CriarUsuarioUseCase
from app.application.dtos.usuario_dto import CriarUsuarioDTO
from app.domain.entities.usuario import Usuario
from app.domain.enums.tipo_usuario import TipoUsuario
from app.domain.exceptions.domain_exception import DomainException

CPF_VALIDO = "529.982.247-25"


@pytest.fixture
def uow():
    mock = AsyncMock()
    mock.__aenter__.return_value = mock
    mock.__aexit__.return_value = False
    mock.usuarios = AsyncMock()
    return mock


async def test_criar_usuario_email_duplicado_levanta_excecao(uow):
    uow.usuarios.buscarPorEmail.return_value = object()

    dto = CriarUsuarioDTO(nome="Test", email="a@b.com", cpf=CPF_VALIDO, senha="Senha123", tipos=[TipoUsuario.USUARIO])
    with pytest.raises(DomainException, match="E-mail já cadastrado"):
        await CriarUsuarioUseCase(uow).executar(dto)


async def test_criar_usuario_cpf_duplicado_levanta_excecao(uow):
    uow.usuarios.buscarPorEmail.return_value = None
    uow.usuarios.buscarPorCpf.return_value = object()

    dto = CriarUsuarioDTO(nome="Test", email="a@b.com", cpf=CPF_VALIDO, senha="Senha123", tipos=[TipoUsuario.USUARIO])
    with pytest.raises(DomainException, match="CPF já cadastrado"):
        await CriarUsuarioUseCase(uow).executar(dto)


async def test_criar_usuario_retorna_dto(uow):
    uow.usuarios.buscarPorEmail.return_value = None
    uow.usuarios.buscarPorCpf.return_value = None

    usuario = Usuario.criar("Test", "a@b.com", CPF_VALIDO, "hash", [TipoUsuario.USUARIO])
    uow.usuarios.salvar.return_value = usuario

    dto = CriarUsuarioDTO(nome="Test", email="a@b.com", cpf=CPF_VALIDO, senha="Senha123", tipos=[TipoUsuario.USUARIO])
    resultado = await CriarUsuarioUseCase(uow).executar(dto)

    assert resultado.nome == "Test"
    assert TipoUsuario.USUARIO in resultado.tipos
    uow.usuarios.salvar.assert_awaited_once()
