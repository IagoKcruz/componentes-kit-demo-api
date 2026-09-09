import pytest
from decimal import Decimal
from unittest.mock import AsyncMock
from app.application.useCases.servico.listarServicosUseCase import ListarServicosUseCase
from app.domain.entities.servico import Servico


@pytest.fixture
def uow():
    mock = AsyncMock()
    mock.__aenter__.return_value = mock
    mock.__aexit__.return_value = False
    mock.servicos = AsyncMock()
    return mock


async def test_listar_retorna_lista_de_dtos(uow):
    uow.servicos.listar.return_value = [
        Servico.criar("Corte", "Desc A", 30, Decimal("10")),
        Servico.criar("Manicure", "Desc B", 45, Decimal("20")),
    ]

    resultado = await ListarServicosUseCase(uow).executar()

    assert len(resultado) == 2
    assert resultado[0].nome == "Corte"
    assert resultado[1].nome == "Manicure"


async def test_listar_apenas_ativos_passa_flag_ao_repo(uow):
    uow.servicos.listar.return_value = []

    await ListarServicosUseCase(uow).executar(apenas_ativos=False)

    uow.servicos.listar.assert_awaited_once_with(False)


async def test_listar_vazio_retorna_lista_vazia(uow):
    uow.servicos.listar.return_value = []
    resultado = await ListarServicosUseCase(uow).executar()
    assert resultado == []
