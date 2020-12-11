"""Setup cog."""

from obsidion.bot import Obsidion
from .minecraft import minecraft


def setup(bot: Obsidion) -> None:
    """Setup."""
    bot.add_cog(minecraft(bot))
