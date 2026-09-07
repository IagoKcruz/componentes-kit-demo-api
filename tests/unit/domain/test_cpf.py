import pytest
from app.domain.value_objects.cpf import CPF
from app.domain.exceptions.domain_exception import DomainException


def test_cpf_valido():
    cpf = CPF("529.982.247-25")
    assert str(cpf) == "529.982.247-25"


def test_cpf_aceita_sem_mascara():
    cpf = CPF("52998224725")
    assert str(cpf) == "529.982.247-25"


def test_cpf_digitos_iguais_invalido():
    with pytest.raises(DomainException, match="CPF inválido"):
        CPF("000.000.000-00")


def test_cpf_digito_verificador_errado():
    with pytest.raises(DomainException, match="CPF inválido"):
        CPF("529.982.247-00")


def test_cpf_tamanho_errado():
    with pytest.raises(DomainException, match="CPF inválido"):
        CPF("123.456")


def test_cpf_segundo_valido():
    cpf = CPF("111.444.777-35")
    assert str(cpf) == "111.444.777-35"
