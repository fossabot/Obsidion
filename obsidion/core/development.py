import logging
from discord.ext import commands

log = logging.getLogger(__name__)


class development(commands.Cog):
    """
    commands useful when writing code for the bot
    should be owner only to prevent someone tampering
    with the bot
    """

    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        return await self.bot.is_owner(ctx.author)

    # for live development
    @commands.command(hidden=True)
    async def load(self, ctx: commands.Context, *, module: str):
        """Loads a module."""
        try:
            self.bot.load_extension(f"obsidion.{module}")
        except commands.ExtensionError as e:
            await ctx.send(
                f"{ctx.message.author.mention}, :x: {e.__class__.__name__}: {e}"
            )
        else:
            await ctx.send(
                f"{ctx.message.author.mention}, :white_check_mark: The cog {module} has been succesfully loaded"
            )

    @commands.command(hidden=True)
    async def unload(self, ctx: commands.Context, *, module: str):
        """Unloads a module."""
        try:
            self.bot.unload_extension(f"obsidion.{module}")
        except commands.ExtensionError as e:
            await ctx.send(
                f"{ctx.message.author.mention}, :x: {e.__class__.__name__}: {e}"
            )
        else:
            await ctx.send(
                f"{ctx.message.author.mention}, :white_check_mark: The cog {module} has been succesfully unloaded"
            )

    @commands.group(name="reload", hidden=True, invoke_without_command=True)
    async def _reload(self, ctx: commands.Context, *, module: str):
        """Reloads a module."""
        try:
            self.bot.reload_extension(f"obsidion.{module}")
        except commands.ExtensionError as e:
            await ctx.send(
                f"{ctx.message.author.mention}, :x: {e.__class__.__name__}: {e}"
            )
        else:
            await ctx.send(
                f"{ctx.message.author.mention}, :white_check_mark: The cog {module} has been succesfully reloaded"
            )

    @commands.command(hidden=True)
    async def shutdown(self, ctx: commands.Context):
        """shutdown the bot"""
        self.bot.close()

    @commands.command(hidden=True)
    async def reboot(self, _ctx: commands.Context):
        """shutdown the bot"""
        self.bot._recreate()


def setup(bot) -> None:
    """Load the Utils cog."""
    bot.add_cog(development(bot))
