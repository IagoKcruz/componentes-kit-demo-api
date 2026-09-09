import pytest
from decimal import Decimal
from app.domain.entities.servico import Servico
from app.domain.exceptions.domainException import DomainException


def test_criar_servico_valido():
    s = Servico.criar("Corte de Cabelo", "Desc", 45, Decimal("50.00"))
    assert s.nome == "Corte de Cabelo"
    assert s.duracaoMinutos == 45
    assert s.preco == Decimal("50.00")
    assert s.ativo is True


def test_criar_nome_com_espacos_e_trimado():
    s = Servico.criar("  Manicure  ", "Desc", 30, Decimal("0"))
    assert s.nome == "Manicure"


def test_criar_nome_vazio_levanta_excecao():
    with pytest.raises(DomainException, match="Nome do serviço é obrigatório"):
        Servico.criar("   ", "Desc", 30, Decimal("0"))


def test_criar_duracao_zero_levanta_excecao():
    with pytest.raises(DomainException, match="Duração deve ser maior que zero"):
        Servico.criar("Nome", "Desc", 0, Decimal("0"))


def test_criar_duracao_negativa_levanta_excecao():
    with pytest.raises(DomainException, match="Duração deve ser maior que zero"):
        Servico.criar("Nome", "Desc", -10, Decimal("0"))


def test_criar_preco_negativo_levanta_excecao():
    with pytest.raises(DomainException, match="Preço não pode ser negativo"):
        Servico.criar("Nome", "Desc", 30, Decimal("-1"))


def test_criar_preco_zero_e_valido():
    s = Servico.criar("Nome", "Desc", 30, Decimal("0"))
    assert s.preco == Decimal("0")


def test_atualizar_nome():
    s = Servico.criar("Antigo", "Desc", 30, Decimal("10"))
    s.atualizar(nome="Novo")
    assert s.nome == "Novo"


def test_atualizar_preco():
    s = Servico.criar("Nome", "Desc", 30, Decimal("10"))
    s.atualizar(preco=Decimal("99.90"))
    assert s.preco == Decimal("99.90")


def test_atualizar_nome_vazio_levanta_excecao():
    s = Servico.criar("Nome", "Desc", 30, Decimal("10"))
    with pytest.raises(DomainException, match="Nome do serviço é obrigatório"):
        s.atualizar(nome="   ")


def test_atualizar_duracao_invalida_levanta_excecao():
    s = Servico.criar("Nome", "Desc", 30, Decimal("10"))
    with pytest.raises(DomainException, match="Duração deve ser maior que zero"):
        s.atualizar(duracaoMinutos=0)


def test_atualizar_sem_campos_nao_altera():
    s = Servico.criar("Nome", "Desc", 30, Decimal("10"))
    s.atualizar()
    assert s.nome == "Nome"
    assert s.duracaoMinutos == 30
