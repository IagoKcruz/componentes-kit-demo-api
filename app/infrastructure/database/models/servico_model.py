from uuid import UUID, uuid4
from datetime import datetime
from decimal import Decimal
from typing import Optional
from sqlmodel import SQLModel, Field


class ServicoModel(SQLModel, table=True):
    __tablename__ = "servicos"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    nome: str = Field(max_length=100)
    descricao: str = Field(default="")
    duracao_minutos: int
    preco: Decimal = Field(decimal_places=2, max_digits=10)
    ativo: bool = Field(default=True)
    criado_em: datetime = Field(default_factory=datetime.utcnow)
