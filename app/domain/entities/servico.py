from uuid import UUID, uuid4
from dataclasses import dataclass
from decimal import Decimal
from app.domain.exceptions.domain_exception import DomainException


@dataclass
class Servico:
    id: UUID
    nome: str
    descricao: str
    duracao_minutos: int
    preco: Decimal
    ativo: bool

    @staticmethod
    def criar(
        nome: str,
        descricao: str,
        duracao_minutos: int,
        preco: Decimal,
    ) -> "Servico":
        if not nome.strip():
            raise DomainException("Nome do serviço é obrigatório")
        if duracao_minutos <= 0:
            raise DomainException("Duração deve ser maior que zero")
        if preco < Decimal("0"):
            raise DomainException("Preço não pode ser negativo")

        return Servico(
            id=uuid4(),
            nome=nome.strip(),
            descricao=descricao,
            duracao_minutos=duracao_minutos,
            preco=preco,
            ativo=True,
        )

    def atualizar(
        self,
        nome: str | None = None,
        descricao: str | None = None,
        duracao_minutos: int | None = None,
        preco: Decimal | None = None,
    ) -> None:
        if nome is not None:
            if not nome.strip():
                raise DomainException("Nome do serviço é obrigatório")
            self.nome = nome.strip()
        if descricao is not None:
            self.descricao = descricao
        if duracao_minutos is not None:
            if duracao_minutos <= 0:
                raise DomainException("Duração deve ser maior que zero")
            self.duracao_minutos = duracao_minutos
        if preco is not None:
            if preco < Decimal("0"):
                raise DomainException("Preço não pode ser negativo")
            self.preco = preco

    def ativar(self) -> None:
        self.ativo = True

    def desativar(self) -> None:
        self.ativo = False
