"""Minecraft cogs."""

import logging

from discord.ext import commands

from obsidion.bot import Obsidion

log = logging.getLogger(__name__)


class Minecraft:
    """Minecraft."""

    def __init__(self, bot: Obsidion) -> None:
        """Init."""
        self.bot = bot

    @commands.command()
    async def recipie(self, ctx: commands.Context, name: str) -> None:
        """Get minecraft recipie."""
        pass

    @commands.command()
    async def render_block(self, ctx: commands.Context, block: str) -> None:
        """Render block."""
        pass

    @commands.command()
    async def item_render(self, ctx: commands.Context, item: str) -> None:
        """Render item."""
        pass

    @commands.commamd()
    async def minecraft_command(self, ctx: commands.Context, com: str) -> None:
        """Minecraft command."""
        pass
