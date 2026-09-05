import re
from dataclasses import dataclass
from app.domain.exceptions.domain_exception import DomainException


@dataclass(frozen=True)
class CPF:
    valor: str

    def __post_init__(self):
        digitos = re.sub(r'\D', '', self.valor)
        if not self._is_valido(digitos):
            raise DomainException("CPF inválido")
        # frozen=True exige object.__setattr__ para reatribuir no __post_init__
        object.__setattr__(self, 'valor', self._formatar(digitos))

    @staticmethod
    def _is_valido(digitos: str) -> bool:
        if len(digitos) != 11:
            return False
        if len(set(digitos)) == 1:
            return False

        soma = sum(int(digitos[i]) * (10 - i) for i in range(9))
        primeiro = (soma * 10) % 11
        if primeiro in (10, 11):
            primeiro = 0
        if primeiro != int(digitos[9]):
            return False

        soma = sum(int(digitos[i]) * (11 - i) for i in range(10))
        segundo = (soma * 10) % 11
        if segundo in (10, 11):
            segundo = 0
        return segundo == int(digitos[10])

    @staticmethod
    def _formatar(digitos: str) -> str:
        return f"{digitos[:3]}.{digitos[3:6]}.{digitos[6:9]}-{digitos[9:]}"

    def __str__(self) -> str:
        return self.valor
