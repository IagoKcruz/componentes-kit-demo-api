from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    auth_habilitado: bool = True
    jwt_secret: str = "troque-esta-chave-em-producao"
    jwt_algoritmo: str = "HS256"
    jwt_expiracao_minutos: int = 60
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/agendamentos"
    debug: bool = False

    model_config = {"env_file": ".env", "case_sensitive": False}


settings = Settings()
