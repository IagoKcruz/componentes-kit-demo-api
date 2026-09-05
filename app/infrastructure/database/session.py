from collections.abc import Iterator
from sqlmodel import SQLModel, Session, create_engine, select
from app.infrastructure.config import settings

engine = create_engine(
    settings.database_url,
    echo=settings.debug,
)


def criar_tabelas() -> None:
    SQLModel.metadata.create_all(engine)


def seed_tipos_usuario() -> None:
    from app.infrastructure.database.models.usuario_model import TipoUsuarioModel

    tipos = ["admin", "usuario", "funcionario"]
    with Session(engine) as session:
        for nome in tipos:
            existe = session.exec(
                select(TipoUsuarioModel).where(TipoUsuarioModel.nome == nome)
            ).first()
            if not existe:
                session.add(TipoUsuarioModel(nome=nome))
        session.commit()


def get_session() -> Iterator[Session]:
    with Session(engine) as session:
        yield session
