"""Start bot and pull in modules."""

import contextlib
import logging
from logging.handlers import RotatingFileHandler
from typing import Iterator

import discord

from obsidion import _update_event_loop_policy, constants

# Set the event loop policies here so any subsequent `new_event_loop()`
# calls, in particular those as a result of the following imports,
# return the correct loop object.
_update_event_loop_policy()

from obsidion.bot import Obsidion  # noqa: E402, I202, E402
from obsidion.utils.utils import prefix_callable  # type: ignore # noqa: E402

#
#     Obsidion - Discord Bot v0.4.0
#
#         Made by Darkflame72
#


class RemoveNoise(logging.Filter):
    """Remove noise from logfile."""

    def __init__(self) -> None:
        """Init."""
        super().__init__(name="discord.state")

    def filter(self, record: logging.LogRecord) -> bool:
        """Filter out unimportant info."""
        if record.levelname == "WARNING" and "referencing an unknown" in record.msg:
            return False
        return True


@contextlib.contextmanager
def setup_logging() -> Iterator[None]:
    """Setup logging."""
    try:
        # __enter__
        max_bytes = 32 * 1024 * 1024  # 32 MiB
        logging.getLogger("discord").setLevel(logging.INFO)
        logging.getLogger("discord.http").setLevel(logging.WARNING)
        logging.getLogger("discord.state").addFilter(RemoveNoise())

        log = logging.getLogger()
        log.setLevel(logging.INFO)
        handler = RotatingFileHandler(
            filename="obsidion.log",
            encoding="utf-8",
            mode="w",
            maxBytes=max_bytes,
            backupCount=5,
        )
        dt_fmt = "%Y-%m-%d %H:%M:%S"
        fmt = logging.Formatter(
            "[{asctime}] [{levelname:<7}] {name}: {message}", dt_fmt, style="{"
        )
        handler.setFormatter(fmt)
        log.addHandler(handler)

        yield
    finally:
        # __exit__
        handlers = log.handlers[:]
        for hdlr in handlers:
            hdlr.close()
            log.removeHandler(hdlr)


# set activity
activity = discord.Activity(
    name=constants.Bot.status,
    type=discord.ActivityType.watching,
)

intents = discord.Intents.none()
intents.messages = True
intents.guilds = True

mentions = discord.AllowedMentions(
    everyone=False,
)

bot = Obsidion(  # pytype: disable=wrong-arg-types
    case_insensitive=True,  # type: ignore
    activity=activity,
    command_prefix=prefix_callable,
    allowed_mentions=mentions,
    intents=intents,
)

# Load all required cogs

# core cogs
bot.load_extension("obsidion.core.development")
bot.load_extension("obsidion.core.help")
bot.load_extension("obsidion.core.error_handler")
bot.load_extension("obsidion.core.events")
bot.load_extension("obsidion.core.minecraft_news")

# extensions and main features
bot.load_extension("obsidion.cogs.fun")
bot.load_extension("obsidion.cogs.hypixel")
bot.load_extension("obsidion.cogs.images")
bot.load_extension("obsidion.cogs.info")
bot.load_extension("obsidion.cogs.misc")
bot.load_extension("obsidion.cogs.redstone")
bot.load_extension("obsidion.cogs.servers")
bot.load_extension("obsidion.cogs.config")
# bot.load_extension("obsidion.cogs.rcon")
# bot.load_extension("obsidion.cogs.minecraft")

if constants.Discord_bot_list.voting_enabled:
    bot.load_extension("obsidion.cogs.botlist")

# run bot
with setup_logging():
    bot.run(constants.Bot.discord_token)
