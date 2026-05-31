from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'

    secret: str = 'SECRET'
    access_token_lifetime_seconds: int = 3600
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')


settings = Settings()