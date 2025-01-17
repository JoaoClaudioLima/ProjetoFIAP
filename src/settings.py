from typing import ClassVar

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    VERSION: ClassVar[str] = "0.0.1"

    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8'
    )

    # Substituir a linha 15 pela 16 para construir a aplicação localmente.

    DATABASE_URL: ClassVar[str] = "postgresql://user:password@postgres:5432/mydatabase"
    # DATABASE_URL: ClassVar[str] = "postgresql://user:password@localhost:5432/mydatabase"
