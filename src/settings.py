from typing import ClassVar

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    VERSION: ClassVar[str] = "0.0.1"

    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8'
    )
    DATABASE_URL: ClassVar[str] = "postgresql://user:password@localhost:5432/mydatabase"
