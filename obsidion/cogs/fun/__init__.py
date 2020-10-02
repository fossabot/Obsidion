"""Fun setup."""

from obsidion.bot import Obsidion
from .fun import Fun


def setup(bot: Obsidion) -> None:
    """Setup."""
    bot.add_cog(Fun(bot))
