"""Import config."""

from .config import config
from obsidion.bot import Obsidion


def setup(bot: Obsidion) -> None:
    """Setup."""
    bot.add_cog(config(bot))
