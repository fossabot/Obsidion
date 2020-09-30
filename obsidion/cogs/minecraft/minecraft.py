"""Minecraft cogs."""

import logging

from discord.ext import commands

log = logging.getLogger(__name__)


class Minecraft:
    """Minecraft."""

    def __init__(self, bot) -> None:
        """Init."""
        self.bot = bot

    @commands.command()
    async def recipie(self, ctx, name) -> None:
        """Get minecraft recipie."""
        pass

    @commands.command()
    async def render_block(self, ctx, block) -> None:
        """Render block."""
        pass

    @commands.command()
    async def item_render(self, ctx, item) -> None:
        """Render item."""
        pass

    @commands.commamd()
    async def minecraft_command(self, ctx, com) -> None:
        """Minecraft command."""
        pass
