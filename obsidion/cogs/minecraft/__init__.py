"""Setup cog."""

from .minecraft import minecraft
from obsidion.bot import Obsidion


def setup(bot: Obsidion) -> None:
    """Setup."""
    bot.add_cog(minecraft(bot))
