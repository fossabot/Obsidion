"""Setup hypixel."""

from obsidion.bot import Obsidion
from .hypixel import hypixel


def setup(bot: Obsidion) -> None:
    """Setup."""
    bot.add_cog(hypixel(bot))
