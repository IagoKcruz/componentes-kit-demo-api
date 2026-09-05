import re
from uuid import UUID
from sqlmodel import Session, select
from app.domain.entities.usuario import Usuario
from app.domain.enums.tipo_usuario import TipoUsuario
from app.domain.repositories.i_usuario_repository import IUsuarioRepository
from app.domain.value_objects.email import Email
from app.domain.value_objects.cpf import CPF
from app.infrastructure.database.models.usuario_model import (
    UsuarioModel,
    TipoUsuarioModel,
)


class SqlModelUsuarioRepository(IUsuarioRepository):
    def __init__(self, session: Session):
        self._session = session

    async def salvar(self, usuario: Usuario) -> Usuario:
        tipos_models = self._resolver_tipos(usuario.tipos)

        model = UsuarioModel(
            id=usuario.id,
            nome=usuario.nome,
            email=str(usuario.email),
            cpf=str(usuario.cpf),
            senha_hash=usuario.senha_hash,
            ativo=usuario.ativo,
            tipos=tipos_models,
        )

        self._session.add(model)
        self._session.commit()
        self._session.refresh(model)
        return self._para_entidade(model)

    async def buscar_por_id(self, id: UUID) -> Usuario | None:
        model = self._session.get(UsuarioModel, id)
        return self._para_entidade(model) if model else None

    async def buscar_por_email(self, email: str) -> Usuario | None:
        stmt = select(UsuarioModel).where(UsuarioModel.email == email)
        model = self._session.exec(stmt).first()
        return self._para_entidade(model) if model else None

    async def buscar_por_cpf(self, cpf: str) -> Usuario | None:
        digitos = re.sub(r'\D', '', cpf)
        cpf_formatado = f"{digitos[:3]}.{digitos[3:6]}.{digitos[6:9]}-{digitos[9:]}" if len(digitos) == 11 else cpf
        stmt = select(UsuarioModel).where(UsuarioModel.cpf == cpf_formatado)
        model = self._session.exec(stmt).first()
        return self._para_entidade(model) if model else None

    async def listar(self) -> list[Usuario]:
        models = self._session.exec(select(UsuarioModel)).all()
        return [self._para_entidade(m) for m in models]

    async def atualizar(self, usuario: Usuario) -> Usuario | None:
        model = self._session.get(UsuarioModel, usuario.id)
        if not model:
            return None

        model.nome = usuario.nome
        model.email = str(usuario.email)
        model.cpf = str(usuario.cpf)
        model.senha_hash = usuario.senha_hash
        model.ativo = usuario.ativo
        model.tipos = self._resolver_tipos(usuario.tipos)

        self._session.commit()
        self._session.refresh(model)
        return self._para_entidade(model)

    async def deletar(self, id: UUID) -> None:
        model = self._session.get(UsuarioModel, id)
        if model:
            self._session.delete(model)
            self._session.commit()

    def _resolver_tipos(self, tipos: list[TipoUsuario]) -> list[TipoUsuarioModel]:
        resultado = []
        for tipo in tipos:
            stmt = select(TipoUsuarioModel).where(TipoUsuarioModel.nome == tipo.value)
            model = self._session.exec(stmt).first()
            if model:
                resultado.append(model)
        return resultado

    def _para_entidade(self, model: UsuarioModel) -> Usuario:
        return Usuario(
            id=model.id,
            nome=model.nome,
            email=Email(model.email),
            cpf=CPF(model.cpf),
            senha_hash=model.senha_hash,
            ativo=model.ativo,
            tipos=[TipoUsuario(t.nome) for t in model.tipos],
        )
