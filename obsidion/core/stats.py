from discord.ext.commands import Cog, Context

from obsidion.bot import Obsidion


class Stats(Cog):
    """A cog which provides a way to hook onto Discord events and forward to stats."""

    def __init__(self, bot: Obsidion):
        self.bot = bot

    @Cog.listener()
    async def on_command_completion(self, ctx: Context) -> None:
        """Report completed commands to statsd."""
        command_name = ctx.command.qualified_name.replace(" ", "_")

        self.bot.stats.incr(f"commands.{command_name}")


def setup(bot: Obsidion) -> None:
    """Load the stats cog."""
    bot.add_cog(Stats(bot))
