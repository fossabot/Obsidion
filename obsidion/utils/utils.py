"""Some useful utils."""

import json

from aiohttp import ClientSession

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
