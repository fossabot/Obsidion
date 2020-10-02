"""Setup misc."""

from obsidion.bot import Obsidion
from .misc import Miscellaneous


def setup(bot: Obsidion) -> None:
    """Setup."""
    bot.add_cog(Miscellaneous(bot))
