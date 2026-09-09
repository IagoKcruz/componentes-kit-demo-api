from uuid import UUID, uuid4
from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy import Column
from sqlalchemy.types import DateTime
from sqlmodel import SQLModel, Field


class ServicoModel(SQLModel, table=True):
    __tablename__ = "servicos"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    nome: str = Field(max_length=100)
    descricao: str = Field(default="")
    duracao_minutos: int
    preco: Decimal = Field(decimal_places=2, max_digits=10)
    ativo: bool = Field(default=True)
    criado_em: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), nullable=False),
    )
