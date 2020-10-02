"""Info."""

from .info import info
from obsidion.bot import Obsidion


def setup(bot: Obsidion) -> None:
    """Setup."""
    bot.add_cog(info(bot))
