"""Settings management for the bot."""

from uuid import UUID
from functools import lru_cache

from pydantic import BaseSettings, HttpUrl, PositiveInt


class Settings(BaseSettings):
    """Bot config settings."""

    DISCORD_TOKEN: str = None
    API_URL: HttpUrl = "https://api.obsidion-dev.com/api/v1"
    HYPIXEL_API_TOKEN: UUID = None
    ACTIVITY: str = "for @Obsidion help"
    DEFAULT_PREFIX: str = "/"
    NEW_GUILD_CHANNEL: PositiveInt = None
    STACK_TRACE_CHANNEL: PositiveInt = None
    FEEDBACK_CHANNEL: PositiveInt = None
    BUG_CHANNEL: PositiveInt = None
    DB_USERNAME: str = "discord"
    DB_HOST: str = "db"
    DB_PASSWORD: str = "hunter12"
    DB_DATABASE: str = "discord"
    DB_PORT: PositiveInt = 5432
    REDIS_HOST: str = "redis"
    REDIS_PORT: PositiveInt = 6379
    REDIS_PASSWORD: str = None
    DEV: bool = False

    class Config:
        """Config for pydantic."""

        # Env will always take priority and is recommended for production
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    """Get settings object and cache it."""
    return Settings()
