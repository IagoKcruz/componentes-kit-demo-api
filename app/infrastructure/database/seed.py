from sqlmodel import select

from app.infrastructure.database.session import _sessionFactory
from app.infrastructure.database.models.usuario_model import TipoUsuarioModel


async def seedTiposUsuario() -> None:
    tipos = ["admin", "usuario", "funcionario"]
    async with _sessionFactory() as session:
        for nome in tipos:
            result = await session.exec(
                select(TipoUsuarioModel).where(TipoUsuarioModel.nome == nome)
            )
            if not result.first():
                session.add(TipoUsuarioModel(nome=nome))
        await session.commit()
