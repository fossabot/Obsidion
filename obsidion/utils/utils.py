async def get(session, url: str, params: dict = None, json: dict = None) -> dict:
    """Get the json from a webpage.

    Args:
        session ([type]): aiohttp session to use
        url (str): url of restapi
        params (dict, optional): paramters to pass to request Defaults to None.
        json (dict, optional): json to pass to request. Defaults to None.

    Returns:
        dict: [description]
    """
    async with session.get(url, params=params, json=json) as resp:
        if resp.status == 200:
            data = await resp.json()
            return data
        return False


async def usernameToUUID(username: str, session) -> str:
    """Takes in an mc username and tries to convert it to a mc uuid.

    Args:
        username (str): username of player which uuid will be from
        session ([type]): aiohttp session

    Returns:
        str: uuid of player
    """

    response = await session.post(
        "https://api.mojang.com/profiles/minecraft", json=[username]
    )

    data = await response.json()

    if response.status == 204 or data == []:
        return False

    return data[0]["id"]


async def UUIDToUsername(uuid: str, session) -> str:
    """Takes in a minecraft UUID and converts it to a minecraft username.

    Args:
        uuid (str): uuid of player
        session ([type]): aiohttp session to use

    Returns:
        str: username of player from uuid
    """

    data = await session.get(f"https://api.mojang.com/user/profiles/{uuid}/names")

    if data.status == 204:
        return False

    data = await data.json()

    if not data:
        return False

    return data[len(data) - 1]["name"]
