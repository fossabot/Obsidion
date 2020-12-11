"""Import config."""

from obsidion.bot import Obsidion
from .config import Config


def setup(bot: Obsidion) -> None:
    """Setup."""
    bot.add_cog(Config(bot))
