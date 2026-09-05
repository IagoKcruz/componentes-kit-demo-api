from uuid import UUID, uuid4
from dataclasses import dataclass, field
from app.domain.value_objects.email import Email
from app.domain.value_objects.cpf import CPF
from app.domain.enums.tipo_usuario import TipoUsuario
from app.domain.exceptions.domain_exception import DomainException


@dataclass
class Usuario:
    id: UUID
    nome: str
    email: Email
    cpf: CPF
    senha_hash: str
    ativo: bool
    tipos: list[TipoUsuario] = field(default_factory=list)

    @staticmethod
    def criar(
        nome: str,
        email: str,
        cpf: str,
        senha_hash: str,
        tipos: list[TipoUsuario],
    ) -> "Usuario":
        usuario = Usuario(
            id=uuid4(),
            nome=nome.strip(),
            email=Email(email),
            cpf=CPF(cpf),
            senha_hash=senha_hash,
            ativo=True,
            tipos=list(tipos),
        )
        usuario._validar_tipos()
        return usuario

    def _validar_tipos(self) -> None:
        if not self.tipos:
            raise DomainException("Usuário deve ter ao menos um tipo")
        if TipoUsuario.ADMIN in self.tipos and len(self.tipos) > 1:
            raise DomainException("Usuário admin não pode ter outros tipos atribuídos")

    def adicionar_tipo(self, tipo: TipoUsuario) -> None:
        if TipoUsuario.ADMIN in self.tipos:
            raise DomainException("Usuário admin não pode receber tipos adicionais")
        if tipo == TipoUsuario.ADMIN and self.tipos:
            raise DomainException("O tipo admin não pode ser combinado com outros tipos")
        if tipo not in self.tipos:
            self.tipos.append(tipo)

    def remover_tipo(self, tipo: TipoUsuario) -> None:
        if tipo not in self.tipos:
            raise DomainException(f"Usuário não possui o tipo '{tipo.value}'")
        if len(self.tipos) == 1:
            raise DomainException("Usuário deve manter ao menos um tipo")
        self.tipos.remove(tipo)

    def ativar(self) -> None:
        self.ativo = True

    def desativar(self) -> None:
        self.ativo = False
