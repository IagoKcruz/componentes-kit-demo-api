from uuid import UUID, uuid4
from datetime import datetime, timezone
from sqlmodel import SQLModel, Field, Relationship


class UsuarioTipoLink(SQLModel, table=True):
    __tablename__ = "usuario_tipos"

    usuario_id: UUID = Field(foreign_key="usuarios.id", primary_key=True)
    tipo_id: int = Field(foreign_key="tipos_usuario.id", primary_key=True)


class TipoUsuarioModel(SQLModel, table=True):
    __tablename__ = "tipos_usuario"

    id: int | None = Field(default=None, primary_key=True)
    nome: str = Field(unique=True, max_length=20)

    usuarios: list["UsuarioModel"] = Relationship(
        back_populates="tipos",
        link_model=UsuarioTipoLink,
    )


class UsuarioModel(SQLModel, table=True):
    __tablename__ = "usuarios"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    nome: str = Field(max_length=100)
    email: str = Field(unique=True, max_length=255)
    cpf: str = Field(unique=True, max_length=14)
    senha_hash: str
    ativo: bool = Field(default=True)
    criado_em: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    tipos: list[TipoUsuarioModel] = Relationship(
        back_populates="usuarios",
        link_model=UsuarioTipoLink,
    )
