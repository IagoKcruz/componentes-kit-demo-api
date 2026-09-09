from uuid import UUID
from sqlalchemy.orm import selectinload
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.domain.entities.usuario import Usuario
from app.domain.enums.tipo_usuario import TipoUsuario
from app.domain.repositories.i_usuario_repository import IUsuarioRepository
from app.domain.value_objects.email import Email
from app.domain.value_objects.cpf import CPF
from app.infrastructure.database.models.usuario_model import UsuarioModel, TipoUsuarioModel


class SqlModelUsuarioRepository(IUsuarioRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def salvar(self, usuario: Usuario) -> Usuario:
        tipos_models = await self._buscar_tipo_models(usuario.tipos)
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
        return usuario

    async def buscar_por_id(self, id: UUID) -> Usuario | None:
        result = await self._session.exec(
            select(UsuarioModel)
            .where(UsuarioModel.id == id)
            .options(selectinload(UsuarioModel.tipos))  # type: ignore[arg-type]
        )
        model = result.first()
        return self._para_entidade(model) if model else None

    async def buscar_por_email(self, email: str) -> Usuario | None:
        result = await self._session.exec(
            select(UsuarioModel)
            .where(UsuarioModel.email == email)
            .options(selectinload(UsuarioModel.tipos))  # type: ignore[arg-type]
        )
        model = result.first()
        return self._para_entidade(model) if model else None

    async def buscar_por_cpf(self, cpf: str) -> Usuario | None:
        cpf_formatado = CPF(cpf).valor
        result = await self._session.exec(
            select(UsuarioModel)
            .where(UsuarioModel.cpf == cpf_formatado)
            .options(selectinload(UsuarioModel.tipos))  # type: ignore[arg-type]
        )
        model = result.first()
        return self._para_entidade(model) if model else None

    async def listar(self) -> list[Usuario]:
        result = await self._session.exec(
            select(UsuarioModel).options(selectinload(UsuarioModel.tipos))  # type: ignore[arg-type]
        )
        return [self._para_entidade(m) for m in result.all()]

    async def atualizar(self, usuario: Usuario) -> Usuario | None:
        model = await self._session.get(UsuarioModel, usuario.id)
        if not model:
            return None
        model.nome = usuario.nome
        model.email = str(usuario.email)
        model.cpf = str(usuario.cpf)
        model.senha_hash = usuario.senha_hash
        model.ativo = usuario.ativo
        model.tipos = await self._buscar_tipo_models(usuario.tipos)
        return usuario

    async def deletar(self, id: UUID) -> None:
        model = await self._session.get(UsuarioModel, id)
        if model:
            await self._session.delete(model)

    async def _buscar_tipo_models(self, tipos: list[TipoUsuario]) -> list[TipoUsuarioModel]:
        nomes = [t.value for t in tipos]
        result = await self._session.exec(
            select(TipoUsuarioModel).where(TipoUsuarioModel.nome.in_(nomes))  # type: ignore[attr-defined]
        )
        return list(result.all())

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
