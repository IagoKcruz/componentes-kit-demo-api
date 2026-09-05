from sqlmodel import Session
from fastapi import Depends
from app.infrastructure.database.session import get_session
from app.infrastructure.repositories.sqlmodel_usuario_repository import SqlModelUsuarioRepository
from app.infrastructure.repositories.sqlmodel_servico_repository import SqlModelServicoRepository


def get_usuario_repository(session: Session = Depends(get_session)) -> SqlModelUsuarioRepository:
    return SqlModelUsuarioRepository(session)


def get_servico_repository(session: Session = Depends(get_session)) -> SqlModelServicoRepository:
    return SqlModelServicoRepository(session)
