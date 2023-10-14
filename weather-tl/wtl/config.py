from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')
    database_url: PostgresDsn

@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    return settings

