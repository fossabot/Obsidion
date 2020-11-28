"""Some useful utils."""
from __future__ import annotations

import json
from typing import TYPE_CHECKING, Union

from aiohttp import ClientSession
import asyncpg
import discord

from obsidion import constants

if TYPE_CHECKING:
    from obsidion.bot import Obsidion


class ApiError(Exception):
    """Custom API Error."""

    pass


async def get(
    session: ClientSession, url: str, params: dict = None, json: dict = None
) -> dict:
    """Get the json from a webpage.

    Args:
        session (ClientSession): aiohttp session to use
        url (str): url of restapi
        params (dict, optional): paramters to pass to request Defaults to None.
        json (dict, optional): json to pass to request. Defaults to None.

    Raises:
        ApiError: Error.

    Returns:
        dict: json response
    """
    async with session.get(url, params=params, json=json) as resp:
        if resp.status == 200:
            data = await resp.json()
            return data
        raise ApiError("API returned invalid response.")


async def usernameToUUID(username: str, bot: Obsidion) -> str:
    """Takes in an mc username and tries to convert it to a mc uuid.

    Args:
        username (str): username of player which uuid will be from
        bot (Obsidion): Obsidion bot

    Returns:
        str: uuid of player
    """
    key = f"username2uuid_{username}"
    if await bot.redis_session.exists(key):
        data = json.loads(await bot.redis_session.get(key))
    else:
        url = f"https://api.mojang.com/users/profiles/minecraft/{username}"
        data = await get(bot.http_session, url)
        await bot.redis_session.set(key, json.dumps(data), expire=28800)

    return data["id"]


async def player_info(uuid: str, bot: Obsidion) -> dict:
    """Takes in an mc username and tries to convert it to a mc uuid.

    Args:
        uuid (str): username of player which uuid will be from
        bot (Obsidion): Obsidion bot

    Returns:
        dict: player info
    """
    key = uuid
    if await bot.redis_session.exists(key):
        data = json.loads(await bot.redis_session.get(key))
    else:
        url = f"https://api.mojang.com/user/profiles/{uuid}/names"
        data = await get(bot.http_session, url)
        await bot.redis_session.set(key, json.dumps(data), expire=28800)

    return data


async def UUIDToUsername(uuid: str, bot: Obsidion) -> str:
    """Takes in a minecraft UUID and converts it to a minecraft username.

    Args:
        uuid (str): uuid of player
        bot (Obsidion): Obsidion bot

    Returns:
        str: username of player from uuid
    """
    data = await player_info(uuid, bot)

    return data[len(data) - 1]["name"]


async def create_db(conn: asyncpg.Connection) -> None:
    """Create database."""
    await conn.execute(
        """
        CREATE TABLE discord_user(
            id bigint PRIMARY KEY,
            username text
        )
    """
    )

    await conn.execute(
        """
        CREATE TABLE guild(
            id bigint PRIMARY KEY,
            prefix text,
            server text
        )
    """
    )
    await conn.execute(
        """
        CREATE TABLE rcon(
            id bigint PRIMARY KEY,
            address text,
            password text,
            channel bigint,
            roles biginit[]
        )
    """
    )


async def get_username(
    bot: Obsidion, username: str, user_id: discord.User.id
) -> Union[str, None]:
    """Get username from discord.

    Args:
        bot ([type]): Obsidion
        username (str): username of player
        user_id ([type]): id of discord user

    Returns:
        str: username
    """
    _username = await bot.db_pool.fetchval(
        "SELECT username FROM discord_user WHERE id = $1", user_id
    )
    if not _username and not username:
        return
    username = _username if _username else username
    return username


async def prefix_callable(bot: Obsidion, msg: discord.Message) -> list:
    """Prefix."""
    key = f"prefix_{msg.guild.id}"
    if await bot.redis_session.exists(key):
        return json.loads(await bot.redis_session.get(key))
    user_id = bot.user.id
    prefix = [f"<@!{user_id}> ", f"<@{user_id}> "]

    # If in direct messages
    if msg.guild is None:
        prefix.append(constants.Bot.default_prefix)
        return prefix
    if await bot.db_pool.fetchval(
        "SELECT prefix FROM guild WHERE id = $1", msg.guild.id
    ):
        guild_prefixes = await bot.db_pool.fetchval(
            "SELECT prefix FROM guild WHERE id = $1", msg.guild.id
        )
        prefix.append(guild_prefixes)
    else:
        prefix.append(constants.Bot.default_prefix)
    await bot.redis_session.set(key, json.dumps(prefix), expire=28800)
    return prefix
