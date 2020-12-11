"""Setup images."""

from obsidion.bot import Obsidion
from .images import Images


def setup(bot: Obsidion) -> None:
    """Setup."""
    bot.add_cog(Images(bot))
