"""Settings management for the bot."""

from uuid import UUID
from functools import lru_cache
import logging

from pydantic import BaseSettings, HttpUrl, PositiveInt, RedisDsn, PostgresDsn
from pydantic.color import Color
import discord

log = logging.getLogger("obsidion")


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
    DB: PostgresDsn = None
    REDIS: RedisDsn = None
    DEV: bool = False
    COLOR: Color = None

    class Config:
        """Config for pydantic."""

        # Env will always take priority and is recommended for production
        env_file = ".env"
        env_file_encoding = "utf-8"


async def prefix_callable(bot, guild: discord.Guild) -> str:
    """Prefix."""
    key = f"prefix_{guild.id}"
    if await bot.redis.exists(key):
        return await bot.redis.get(key)
    db_prefix = await bot.db.fetchval(
        "SELECT prefix FROM guild WHERE id = $1", guild.id
    )
    if db_prefix:
        prefix = db_prefix
    else:
        prefix = get_settings().DEFAULT_PREFIX
    await bot.redis.set(key, prefix, expire=28800)
    return prefix


@lru_cache()
def get_settings() -> Settings:
    """Get settings object and cache it."""
    return Settings()
