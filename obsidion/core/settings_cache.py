import discord
from typing import Union, Dict, Optional, List

from .config import get_settings


async def prefix_callable(bot, guild: discord.Guild) -> List[str]:
    """Prefix."""
    key = f"prefix_{guild.id}"
    # redis = await bot.redis.exists(key)
    # if redis:
    #     return [str(redis)]
    db_prefix = await bot.db.fetchval(
        "SELECT prefix FROM guild WHERE id = $1", guild.id
    )
    if db_prefix:
        prefix = db_prefix
    else:
        prefix = get_settings().DEFAULT_PREFIX
    await bot.redis.set(key, prefix, expire=28800)
    return [str(prefix)]


async def fetch_locale(bot, guild) -> str:
    """Prefix."""
    if not guild:
        return None
    # key = f"locale_{guild.id}"
    # redis = await bot.redis.exists(key)
    # if redis:
    #     return redis
    db_locale = await bot.db.fetchval(
        "SELECT locale FROM guild WHERE id = $1", guild.id
    )
    if db_locale:
        locale = db_locale
    else:
        locale = "en-us"
    # await bot.redis.set(key, locale, expire=28800)
    return locale
