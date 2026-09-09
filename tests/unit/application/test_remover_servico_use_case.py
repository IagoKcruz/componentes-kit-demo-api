import pytest
from decimal import Decimal
from uuid import uuid4
from unittest.mock import AsyncMock
from app.application.use_cases.servico.remover_servico_use_case import RemoverServicoUseCase
from app.domain.entities.servico import Servico
from app.domain.exceptions.domain_exception import DomainException


@pytest.fixture
def uow():
    mock = AsyncMock()
    mock.__aenter__.return_value = mock
    mock.__aexit__.return_value = False
    mock.servicos = AsyncMock()
    return mock


async def test_remover_servico_nao_encontrado_levanta_excecao(uow):
    uow.servicos.buscar_por_id.return_value = None

    with pytest.raises(DomainException, match="não encontrado"):
        await RemoverServicoUseCase(uow).executar(uuid4())


async def test_remover_servico_chama_deletar_com_id_correto(uow):
    servico = Servico.criar("Corte", "Desc", 30, Decimal("50"))
    uow.servicos.buscar_por_id.return_value = servico

    await RemoverServicoUseCase(uow).executar(servico.id)

    uow.servicos.deletar.assert_awaited_once_with(servico.id)
