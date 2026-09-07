import pytest
from decimal import Decimal
from unittest.mock import AsyncMock
from app.application.use_cases.servico.criar_servico_use_case import CriarServicoUseCase
from app.application.dtos.servico_dto import CriarServicoDTO
from app.domain.entities.servico import Servico


@pytest.fixture
def repo():
    return AsyncMock()


async def test_criar_servico_retorna_dto(repo):
    servico = Servico.criar("Corte", "Desc", 30, Decimal("50"))
    repo.salvar.return_value = servico

    dto = CriarServicoDTO(nome="Corte", descricao="Desc", duracao_minutos=30, preco=Decimal("50"))
    resultado = await CriarServicoUseCase(repo).executar(dto)

    repo.salvar.assert_awaited_once()
    assert resultado.nome == "Corte"
    assert resultado.duracao_minutos == 30
    assert resultado.ativo is True


async def test_criar_servico_propaga_excecao_de_dominio(repo):
    from app.domain.exceptions.domain_exception import DomainException
    import pytest

    with pytest.raises(DomainException):
        dto = CriarServicoDTO(nome="Nome", descricao="", duracao_minutos=30, preco=Decimal("10"))
        # simula falha no repositório
        repo.salvar.side_effect = DomainException("Erro interno")
        await CriarServicoUseCase(repo).executar(dto)
