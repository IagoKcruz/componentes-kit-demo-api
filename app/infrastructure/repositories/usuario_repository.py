from uuid import UUID

from sqlalchemy.orm import selectinload
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.domain.contracts.i_usuario_repository import IUsuarioRepository
from app.domain.entities.usuario import Usuario
from app.domain.enums.tipo_usuario import TipoUsuario
from app.domain.exceptions.domain_exception import DomainException
from app.domain.exceptions.validacao_error import ValidacaoError
from app.domain.value_objects.cpf import CPF
from app.domain.value_objects.email import Email
from app.infrastructure.database.models.usuario_model import (
    TipoUsuarioModel,
    UsuarioModel,
)
from app.infrastructure.repositories.repository import Repository


class UsuarioRepository(Repository[Usuario, UsuarioModel, UUID], IUsuarioRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, UsuarioModel)

    def _queryOptions(self) -> list:
        return [selectinload(UsuarioModel.tipos)]  # type: ignore[arg-type]

    def _paraEntidade(self, model: UsuarioModel) -> Usuario:
        return Usuario(
            id=model.id,
            nome=model.nome,
            email=Email(model.email),
            cpf=CPF(model.cpf),
            senhaHash=model.senha_hash,
            ativo=model.ativo,
            tipos=[TipoUsuario(t.nome) for t in model.tipos],
        )

    def _paraModel(self, usuario: Usuario) -> UsuarioModel:
        return UsuarioModel(
            id=usuario.id,
            nome=usuario.nome,
            email=str(usuario.email),
            cpf=str(usuario.cpf),
            senha_hash=usuario.senhaHash,
            ativo=usuario.ativo,
        )

    async def _aplicarCampos(self, usuario: Usuario, model: UsuarioModel) -> None:
        model.nome = usuario.nome
        model.email = str(usuario.email)
        model.cpf = str(usuario.cpf)
        model.senha_hash = usuario.senhaHash
        model.ativo = usuario.ativo
        model.tipos = await self._buscarTipoModels(usuario.tipos)

    async def salvar(self, usuario: Usuario) -> Usuario:
        tiposModels = await self._buscarTipoModels(usuario.tipos)
        model = self._paraModel(usuario)
        model.tipos = tiposModels
        self._session.add(model)
        return usuario

    async def buscarPorEmail(self, email: str) -> Usuario | None:
        result = await self._session.exec(
            select(UsuarioModel)
            .where(UsuarioModel.email == email)
            .options(*self._queryOptions())
        )
        model = result.first()
        return self._paraEntidade(model) if model else None

    async def buscarPorCpf(self, cpf: str) -> Usuario | None:
        try:
            cpfFormatado = CPF(cpf).valor
        except DomainException:
            raise ValidacaoError("CPF inválido")
        result = await self._session.exec(
            select(UsuarioModel)
            .where(UsuarioModel.cpf == cpfFormatado)
            .options(*self._queryOptions())
        )
        model = result.first()
        return self._paraEntidade(model) if model else None

    async def _buscarTipoModels(self, tipos: list[TipoUsuario]) -> list[TipoUsuarioModel]:
        nomes = [t.value for t in tipos]
        result = await self._session.exec(
            select(TipoUsuarioModel).where(TipoUsuarioModel.nome.in_(nomes))  # type: ignore[attr-defined]
        )
        return list(result.all())
