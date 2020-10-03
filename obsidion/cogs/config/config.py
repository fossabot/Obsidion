"""Config related commands."""

from discord.ext import commands

from obsidion.bot import Obsidion


class Config(commands.Cog):
    """Config class."""

    def __init__(self, bot: Obsidion) -> None:
        """Init."""
        self.bot = bot
