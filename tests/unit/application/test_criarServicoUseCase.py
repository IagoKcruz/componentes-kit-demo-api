import pytest
from decimal import Decimal
from unittest.mock import AsyncMock
from app.application.useCases.servico.criarServicoUseCase import CriarServicoUseCase
from app.application.dtos.servicoDto import CriarServicoDTO
from app.domain.entities.servico import Servico


@pytest.fixture
def uow():
    mock = AsyncMock()
    mock.__aenter__.return_value = mock
    mock.__aexit__.return_value = False
    mock.servicos = AsyncMock()
    return mock


async def test_criar_servico_retorna_dto(uow):
    servico = Servico.criar("Corte", "Desc", 30, Decimal("50"))
    uow.servicos.salvar.return_value = servico

    dto = CriarServicoDTO(nome="Corte", descricao="Desc", duracaoMinutos=30, preco=Decimal("50"))
    resultado = await CriarServicoUseCase(uow).executar(dto)

    uow.servicos.salvar.assert_awaited_once()
    assert resultado.nome == "Corte"
    assert resultado.duracaoMinutos == 30
    assert resultado.ativo is True


async def test_criar_servico_propaga_excecao_de_dominio(uow):
    from app.domain.exceptions.domainException import DomainException

    with pytest.raises(DomainException):
        dto = CriarServicoDTO(nome="Nome", descricao="", duracaoMinutos=30, preco=Decimal("10"))
        uow.servicos.salvar.side_effect = DomainException("Erro interno")
        await CriarServicoUseCase(uow).executar(dto)
