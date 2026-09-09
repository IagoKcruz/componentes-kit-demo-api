from enum import Enum


class TipoUsuario(str, Enum):
    ADMIN = "admin"
    USUARIO = "usuario"
    FUNCIONARIO = "funcionario"
