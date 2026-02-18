from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "DataVista API"
    environment: str = "development"
    secret_key: str = "change-me"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 120
    database_url: str = "postgresql+psycopg://postgres:postgres@db:5432/datavista"
    redis_url: str = "redis://redis:6379/0"
    max_upload_size_mb: int = 20

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
