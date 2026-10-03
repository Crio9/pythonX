from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    db_host: str
    db_port: str
    db_user: str
    db_password: str
    db_name: str

    SECRET_KEY: str
    TOKEN_LIFETIME_MINUTES: int
    TOKEN_ALGORITHM: str

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()

DB_URL = f"postgresql+psycopg2://{settings.db_user}:{settings.db_password}@{settings.db_host}:{settings.db_port}/{settings.db_name}"
