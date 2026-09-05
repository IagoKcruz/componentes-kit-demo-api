import re
from dataclasses import dataclass
from app.domain.exceptions.domain_exception import DomainException


@dataclass(frozen=True)
class Email:
    valor: str

    def __post_init__(self):
        if not self._is_valido(self.valor):
            raise DomainException("E-mail inválido")

    @staticmethod
    def _is_valido(email: str) -> bool:
        padrao = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(padrao, email))

    def __str__(self) -> str:
        return self.valor
