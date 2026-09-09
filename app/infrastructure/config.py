from pathlib import Path
from pydantic_settings import BaseSettings

_BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    auth_habilitado: bool = True
    jwt_secret: str = "troque-esta-chave-em-producao"
    jwt_algoritmo: str = "HS256"
    jwt_expiracao_minutos: int = 60
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/agendamentos"
    debug: bool = False

    model_config = {
        "env_file": str(_BASE_DIR / ".env"),
        "env_file_encoding": "utf-8",
        "case_sensitive": False,
    }


settings = Settings()
