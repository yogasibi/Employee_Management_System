""" config.py"""
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

    """ BaseSettings reads configuration from environment variables.
    env_file=".env" loads our local configuration."""

    DATABASE_URL: str

    model_config = SettingsConfigDict(
        env_file = ".env",
        extra="ignore"
    )

settings = Settings()