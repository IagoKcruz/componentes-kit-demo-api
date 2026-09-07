import pytest
from decimal import Decimal
from uuid import uuid4
from unittest.mock import AsyncMock
from app.application.use_cases.servico.atualizar_servico_use_case import AtualizarServicoUseCase
from app.application.dtos.servico_dto import AtualizarServicoDTO
from app.domain.entities.servico import Servico
from app.domain.exceptions.domain_exception import DomainException


@pytest.fixture
def repo():
    return AsyncMock()


async def test_atualizar_servico_nao_encontrado_levanta_excecao(repo):
    repo.buscar_por_id.return_value = None

    with pytest.raises(DomainException, match="não encontrado"):
        await AtualizarServicoUseCase(repo).executar(uuid4(), AtualizarServicoDTO(nome="Novo"))


async def test_atualizar_servico_retorna_dto_com_valores_novos(repo):
    servico = Servico.criar("Antigo", "Desc", 30, Decimal("10"))
    repo.buscar_por_id.return_value = servico
    repo.atualizar.return_value = servico

    dto = AtualizarServicoDTO(nome="Novo", preco=Decimal("20"))
    resultado = await AtualizarServicoUseCase(repo).executar(servico.id, dto)

    assert resultado.nome == "Novo"
    assert resultado.preco == Decimal("20")
    repo.atualizar.assert_awaited_once()


async def test_atualizar_servico_erro_no_repositorio_levanta_excecao(repo):
    servico = Servico.criar("Nome", "Desc", 30, Decimal("10"))
    repo.buscar_por_id.return_value = servico
    repo.atualizar.return_value = None

    with pytest.raises(DomainException, match="Erro ao atualizar"):
        await AtualizarServicoUseCase(repo).executar(servico.id, AtualizarServicoDTO(nome="Novo"))
