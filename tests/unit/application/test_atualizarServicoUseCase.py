import pytest
from decimal import Decimal
from uuid import uuid4
from unittest.mock import AsyncMock
from app.application.useCases.servico.atualizarServicoUseCase import AtualizarServicoUseCase
from app.application.dtos.servicoDto import AtualizarServicoDTO
from app.domain.entities.servico import Servico
from app.domain.exceptions.entidadeNaoEncontradaError import EntidadeNaoEncontradaError


@pytest.fixture
def uow():
    mock = AsyncMock()
    mock.__aenter__.return_value = mock
    mock.__aexit__.return_value = False
    mock.servicos = AsyncMock()
    return mock


async def test_atualizar_servico_nao_encontrado_levanta_excecao(uow):
    uow.servicos.buscarPorId.return_value = None

    with pytest.raises(EntidadeNaoEncontradaError, match="não encontrado"):
        await AtualizarServicoUseCase(uow).executar(uuid4(), AtualizarServicoDTO(nome="Novo"))


async def test_atualizar_servico_retorna_dto_com_valores_novos(uow):
    servico = Servico.criar("Antigo", "Desc", 30, Decimal("10"))
    uow.servicos.buscarPorId.return_value = servico
    uow.servicos.atualizar.return_value = servico

    dto = AtualizarServicoDTO(nome="Novo", preco=Decimal("20"))
    resultado = await AtualizarServicoUseCase(uow).executar(servico.id, dto)

    assert resultado.nome == "Novo"
    assert resultado.preco == Decimal("20")
    uow.servicos.atualizar.assert_awaited_once()


async def test_atualizar_servico_erro_no_repositorio_levanta_excecao(uow):
    servico = Servico.criar("Nome", "Desc", 30, Decimal("10"))
    uow.servicos.buscarPorId.return_value = servico
    uow.servicos.atualizar.return_value = None

    with pytest.raises(EntidadeNaoEncontradaError, match="não encontrado"):
        await AtualizarServicoUseCase(uow).executar(servico.id, AtualizarServicoDTO(nome="Novo"))
