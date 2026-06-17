"""Applicatie-instellingen, ingelezen uit omgevingsvariabelen of een .env-bestand."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Centrale configuratie van de applicatie."""

    app_name: str = "SHE-Programs RI&E"
    database_url: str = "sqlite:///./she_rie.db"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
