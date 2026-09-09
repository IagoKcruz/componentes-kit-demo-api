import pytest
from app.domain.entities.usuario import Usuario
from app.domain.enums.tipo_usuario import TipoUsuario
from app.domain.exceptions.domain_exception import DomainException

CPF_VALIDO = "529.982.247-25"
EMAIL_VALIDO = "admin@teste.com"
HASH = "hash_qualquer"


def test_criar_usuario_valido():
    u = Usuario.criar("Admin", EMAIL_VALIDO, CPF_VALIDO, HASH, [TipoUsuario.ADMIN])
    assert u.nome == "Admin"
    assert u.ativo is True
    assert TipoUsuario.ADMIN in u.tipos


def test_criar_nome_com_espacos_e_trimado():
    u = Usuario.criar("  João  ", EMAIL_VALIDO, CPF_VALIDO, HASH, [TipoUsuario.USUARIO])
    assert u.nome == "João"


def test_criar_admin_com_outro_tipo_levanta_excecao():
    with pytest.raises(DomainException):
        Usuario.criar("Admin", EMAIL_VALIDO, CPF_VALIDO, HASH, [TipoUsuario.ADMIN, TipoUsuario.USUARIO])


def test_criar_sem_tipo_levanta_excecao():
    with pytest.raises(DomainException, match="ao menos um tipo"):
        Usuario.criar("User", EMAIL_VALIDO, CPF_VALIDO, HASH, [])


def test_criar_cpf_invalido_levanta_excecao():
    with pytest.raises(DomainException, match="CPF inválido"):
        Usuario.criar("User", EMAIL_VALIDO, "000.000.000-00", HASH, [TipoUsuario.USUARIO])


def test_criar_email_invalido_levanta_excecao():
    with pytest.raises(DomainException, match="E-mail inválido"):
        Usuario.criar("User", "email_invalido", CPF_VALIDO, HASH, [TipoUsuario.USUARIO])


def test_adicionar_tipo():
    u = Usuario.criar("User", EMAIL_VALIDO, CPF_VALIDO, HASH, [TipoUsuario.USUARIO])
    u.adicionarTipo(TipoUsuario.FUNCIONARIO)
    assert TipoUsuario.FUNCIONARIO in u.tipos


def test_adicionar_tipo_admin_em_usuario_comum_levanta_excecao():
    u = Usuario.criar("User", EMAIL_VALIDO, CPF_VALIDO, HASH, [TipoUsuario.USUARIO])
    with pytest.raises(DomainException):
        u.adicionarTipo(TipoUsuario.ADMIN)


def test_adicionar_tipo_duplicado_nao_duplica():
    u = Usuario.criar("User", EMAIL_VALIDO, CPF_VALIDO, HASH, [TipoUsuario.USUARIO])
    u.adicionarTipo(TipoUsuario.USUARIO)
    assert u.tipos.count(TipoUsuario.USUARIO) == 1


def test_remover_tipo():
    u = Usuario.criar("User", EMAIL_VALIDO, CPF_VALIDO, HASH, [TipoUsuario.USUARIO])
    u.adicionarTipo(TipoUsuario.FUNCIONARIO)
    u.removerTipo(TipoUsuario.FUNCIONARIO)
    assert TipoUsuario.FUNCIONARIO not in u.tipos


def test_remover_unico_tipo_levanta_excecao():
    u = Usuario.criar("User", EMAIL_VALIDO, CPF_VALIDO, HASH, [TipoUsuario.USUARIO])
    with pytest.raises(DomainException, match="ao menos um tipo"):
        u.removerTipo(TipoUsuario.USUARIO)


def test_ativar_desativar():
    u = Usuario.criar("User", EMAIL_VALIDO, CPF_VALIDO, HASH, [TipoUsuario.USUARIO])
    u.desativar()
    assert u.ativo is False
    u.ativar()
    assert u.ativo is True
