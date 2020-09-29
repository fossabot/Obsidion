import asyncio
import datetime
import logging
import socket
import sys
from enum import IntEnum
from typing import Optional

import aiohttp
import aioredis
import discord
import fakeredis.aioredis
from discord.ext import commands
import asyncpg

from obsidion import constants
from obsidion.core.global_checks import init_global_checks

log = logging.getLogger(__name__)

__all__ = ["Obsidion", "ExitCodes"]


class Obsidion(commands.AutoShardedBot):
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.http_session: Optional[aiohttp.ClientSession] = None
        self.redis_session: Optional[aioredis.Redis] = None
        self.redis_ready = asyncio.Event()
        self.redis_closed = False
        self.db_pool = None
        self.db_ready = asyncio.Event()

        self._connector = None
        self._resolver = None

        self.uptime = None

        # Do basic checks on every command
        init_global_checks(self)

    async def _create_db_pool(self) -> None:
        """
        Create the postgres connection pool.
        """
        self.db_pool = await asyncpg.create_pool(
            database=constants.Database.database,
            user=constants.Database.username,
            password=constants.Database.password,
            host=constants.Database.host,
            port=constants.Database.port,
        )

        self.db_ready.set()

    async def _create_redis_session(self) -> None:
        """
        Create the Redis connection pool, and then open the redis event gate.
        If constants.Redis.use_fakeredis is True, we'll set up a fake redis pool instead
        of attempting to communicate with a real Redis server. This is useful because it
        means contributors don't necessarily need to get Redis running locally just
        to run the bot.
        The fakeredis cache won't have persistence across restarts, but that
        usually won't matter for local bot testing.
        """
        if not constants.Redis.enabled:
            log.info(
                "Using fakeredis instead of communicating with a real Redis server."
            )
            self.redis_session = await fakeredis.aioredis.create_redis_pool()
        else:
            self.redis_session = await aioredis.create_redis_pool(
                address=(constants.Redis.host, constants.Redis.port),
            )

        self.redis_closed = False
        self.redis_ready.set()

    async def login(self, *args, **kwargs) -> None:
        """Re-create the connector and set up sessions before logging into Discord."""
        self._recreate()
        await self.stats.create_socket()
        await super().login(*args, **kwargs)
        self.uptime = datetime.datetime.now()

    async def close(self) -> None:
        """Close the Discord connection and the aiohttp session, connector, statsd client, and resolver."""
        await super().close()

        if self.http_session:
            await self.http_session.close()

        if self._connector:
            await self._connector.close()

        if self._resolver:
            await self._resolver.close()

        if self.stats._transport:
            self.stats._transport.close()

        if self.redis_session:
            self.redis_closed = True
            self.redis_session.close()
            self.redis_ready.clear()
            await self.redis_session.wait_closed()

    def _recreate(self) -> None:
        """Re-create the connector, aiohttp session, the APIClient and the Redis session."""
        # Use asyncio for DNS resolution instead of threads so threads aren't spammed.
        # Doesn't seem to have any state with regards to being closed, so no need to worry?
        self._resolver = aiohttp.AsyncResolver()

        # Its __del__ does send a warning but it doesn't always show up for some reason.
        if self._connector and not self._connector._closed:
            log.warning(
                "The previous connector was not closed; it will remain open and be overwritten"
            )

        if self.redis_session and not self.redis_session.closed:
            log.warning(
                "The previous redis pool was not closed; it will remain open and be overwritten"
            )

        # Create the redis session
        self.loop.create_task(self._create_redis_session())

        # Create the postgres pool
        self.loop.create_task(self._create_db_pool())

        # Use AF_INET as its socket family to prevent HTTPS related problems both locally
        # and in production.
        self._connector = aiohttp.TCPConnector(
            resolver=self._resolver,
            family=socket.AF_INET,
        )

        # Client.login() will call HTTPClient.static_login() which will create a session using
        # this connector attribute.
        self.http.connector = self._connector

        # Its __del__ does send a warning but it doesn't always show up for some reason.
        if self.http_session and not self.http_session.closed:
            log.warning(
                "The previous session was not closed; it will remain open and be overwritten"
            )

        self.http_session = aiohttp.ClientSession(connector=self._connector)

    async def get_context(self, message, *, cls=commands.Context):
        return await super().get_context(message, cls=cls)

    async def process_commands(self, message: discord.Message):
        if not message.author.bot:
            ctx = await self.get_context(message)
            await self.invoke(ctx)
        else:
            ctx = None

    async def logout(self):
        """Logs out of Discord and closes all connections."""
        await super().logout()

    async def shutdown(self, *, restart: bool = False):
        """Gracefully quit Obsidion.
        The program will exit with code :code:`0` by default.
        Parameters
        ----------
        restart : bool
            If :code:`True`, the program will exit with code :code:`26`.
        """
        if not restart:
            self._shutdown_mode = ExitCodes.SHUTDOWN
        else:
            self._shutdown_mode = ExitCodes.RESTART

        await self.logout()
        sys.exit(self._shutdown_mode)


class ExitCodes(IntEnum):
    # This needs to be an int enum to be used
    # with sys.exit
    CRITICAL = 1
    SHUTDOWN = 0
    RESTART = 26
