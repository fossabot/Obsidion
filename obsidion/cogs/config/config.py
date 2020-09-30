""" onfig related commands."""

from discord.ext import commands


class config(commands.Cog):
    """Config class."""

    def __init__(self, bot) -> None:
        """Init."""
        self.bot = bot
