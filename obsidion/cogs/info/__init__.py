"""Info."""

from obsidion.bot import Obsidion
from .info import Info


def setup(bot: Obsidion) -> None:
    """Setup."""
    bot.add_cog(Info(bot))
