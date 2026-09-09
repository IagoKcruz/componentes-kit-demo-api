from uuid import UUID
from decimal import Decimal
from pydantic import BaseModel, Field


class CriarServicoDTO(BaseModel):
    nome: str = Field(min_length=2, max_length=100)
    descricao: str = ""
    duracaoMinutos: int = Field(gt=0)
    preco: Decimal = Field(ge=0, decimal_places=2)


class AtualizarServicoDTO(BaseModel):
    nome: str | None = Field(None, min_length=2, max_length=100)
    descricao: str | None = None
    duracaoMinutos: int | None = Field(None, gt=0)
    preco: Decimal | None = Field(None, ge=0, decimal_places=2)


class ServicoResponseDTO(BaseModel):
    id: UUID
    nome: str
    descricao: str
    duracaoMinutos: int
    preco: Decimal
    ativo: bool

    model_config = {"from_attributes": True}
