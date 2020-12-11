"""Redstone."""

from obsidion.bot import Obsidion
from .redstone import Redstone


def setup(bot: Obsidion) -> None:
    """Setup."""
    bot.add_cog(Redstone(bot))
