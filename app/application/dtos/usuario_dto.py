from uuid import UUID
from pydantic import BaseModel, EmailStr, Field
from app.domain.enums.tipo_usuario import TipoUsuario


class CriarUsuarioDTO(BaseModel):
    nome: str = Field(min_length=2, max_length=100)
    email: EmailStr
    cpf: str
    senha: str = Field(min_length=6)
    tipos: list[TipoUsuario]


class UsuarioResponseDTO(BaseModel):
    id: UUID
    nome: str
    email: str
    cpf: str
    ativo: bool
    tipos: list[TipoUsuario]

    model_config = {"from_attributes": True}
