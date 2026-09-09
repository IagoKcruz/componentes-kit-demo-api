import pytest
from app.domain.value_objects.email import Email
from app.domain.exceptions.domain_exception import DomainException


def test_email_valido():
    email = Email("usuario@teste.com")
    assert str(email) == "usuario@teste.com"


def test_email_sem_arroba():
    with pytest.raises(DomainException, match="E-mail inválido"):
        Email("usuarioteste.com")


def test_email_sem_dominio():
    with pytest.raises(DomainException, match="E-mail inválido"):
        Email("usuario@")


def test_email_vazio():
    with pytest.raises(DomainException, match="E-mail inválido"):
        Email("")


def test_email_sem_extensao():
    with pytest.raises(DomainException, match="E-mail inválido"):
        Email("usuario@dominio")
