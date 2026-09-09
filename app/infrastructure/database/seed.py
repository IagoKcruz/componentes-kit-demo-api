from sqlmodel import select
from app.infrastructure.database.session import _session_factory
from app.infrastructure.database.models.usuario_model import TipoUsuarioModel


async def seed_tipos_usuario() -> None:
    tipos = ["admin", "usuario", "funcionario"]
    async with _session_factory() as session:
        for nome in tipos:
            result = await session.exec(
                select(TipoUsuarioModel).where(TipoUsuarioModel.nome == nome)
            )
            if not result.first():
                session.add(TipoUsuarioModel(nome=nome))
        await session.commit()
