from sqlalchemy.dialects.postgresql import insert as pg_insert

from app.domain.enums.tipo_usuario import TipoUsuario
from app.infrastructure.database.session import _sessionFactory
from app.infrastructure.database.models.usuario_model import TipoUsuarioModel


async def seedTiposUsuario() -> None:
    async with _sessionFactory() as session:
        for tipo in TipoUsuario:
            stmt = pg_insert(TipoUsuarioModel).values(nome=tipo.value).on_conflict_do_nothing()
            await session.execute(stmt)
        await session.commit()
