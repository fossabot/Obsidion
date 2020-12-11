"""Import botlists."""

from obsidion.bot import Obsidion
from .botlist import botlist


def setup(bot: Obsidion) -> None:
    """Setup."""
    bot.add_cog(botlist(bot))
