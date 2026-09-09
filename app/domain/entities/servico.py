from uuid import UUID, uuid4
from dataclasses import dataclass
from decimal import Decimal
from app.domain.exceptions.domainException import DomainException


@dataclass
class Servico:
    id: UUID
    nome: str
    descricao: str
    duracaoMinutos: int
    preco: Decimal
    ativo: bool

    @staticmethod
    def criar(
        nome: str,
        descricao: str,
        duracaoMinutos: int,
        preco: Decimal,
    ) -> "Servico":
        if not nome.strip():
            raise DomainException("Nome do serviço é obrigatório")
        if duracaoMinutos <= 0:
            raise DomainException("Duração deve ser maior que zero")
        if preco < Decimal("0"):
            raise DomainException("Preço não pode ser negativo")

        return Servico(
            id=uuid4(),
            nome=nome.strip(),
            descricao=descricao,
            duracaoMinutos=duracaoMinutos,
            preco=preco,
            ativo=True,
        )

    def atualizar(
        self,
        nome: str | None = None,
        descricao: str | None = None,
        duracaoMinutos: int | None = None,
        preco: Decimal | None = None,
    ) -> None:
        if nome is not None:
            if not nome.strip():
                raise DomainException("Nome do serviço é obrigatório")
            self.nome = nome.strip()
        if descricao is not None:
            self.descricao = descricao
        if duracaoMinutos is not None:
            if duracaoMinutos <= 0:
                raise DomainException("Duração deve ser maior que zero")
            self.duracaoMinutos = duracaoMinutos
        if preco is not None:
            if preco < Decimal("0"):
                raise DomainException("Preço não pode ser negativo")
            self.preco = preco

    def ativar(self) -> None:
        self.ativo = True

    def desativar(self) -> None:
        self.ativo = False
