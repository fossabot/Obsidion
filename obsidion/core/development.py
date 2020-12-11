"""Development related commands."""

import logging

from discord.ext import commands

from obsidion.bot import Obsidion

log = logging.getLogger(__name__)


class development(commands.Cog):
    """Commands useful when writing code for the bot."""

    def __init__(self, bot: Obsidion) -> None:
        """Init."""
        self.bot = bot

    async def cog_check(self, ctx: commands.Context) -> None:
        """Check if user is owner."""
        return await self.bot.is_owner(ctx.author)

    @commands.command(hidden=True)
    async def load(self, ctx: commands.Context, *, module: str) -> None:
        """Loads a module."""
        try:
            self.bot.load_extension(f"obsidion.{module}")
        except commands.ExtensionError as e:
            await ctx.send(
                f"{ctx.message.author.mention}, :x: {e.__class__.__name__}: {e}"
            )
        else:
            await ctx.send(
                (
                    f"{ctx.message.author.mention}, :white_check_mark: The cog "
                    f"`{module}` has been succesfully loaded"
                )
            )

    @commands.command(hidden=True)
    async def unload(self, ctx: commands.Context, *, module: str) -> None:
        """Unloads a module."""
        try:
            self.bot.unload_extension(f"obsidion.{module}")
        except commands.ExtensionError as e:
            await ctx.send(
                f"{ctx.message.author.mention}, :x: {e.__class__.__name__}: {e}"
            )
        else:
            await ctx.send(
                (
                    f"{ctx.message.author.mention}, :white_check_mark: "
                    f"The cog `{module}` has been succesfully unloaded"
                )
            )

    @commands.group(name="reload", hidden=True, invoke_without_command=True)
    async def _reload(self, ctx: commands.Context, *, module: str) -> None:
        """Reloads a module."""
        try:
            self.bot.reload_extension(f"obsidion.{module}")
        except commands.ExtensionError as e:
            await ctx.send(
                f"{ctx.message.author.mention}, :x: {e.__class__.__name__}: {e}"
            )
        else:
            await ctx.send(
                (
                    f"{ctx.message.author.mention}, :white_check_mark: The cog "
                    f"`{module}` has been succesfully reloaded"
                )
            )

    @commands.command(hidden=True)
    async def shutdown(self, ctx: commands.Context) -> None:
        """Shutdown the bot."""
        await self.bot.close()


def setup(bot: Obsidion) -> None:
    """Load the Utils cog."""
    bot.add_cog(development(bot))
