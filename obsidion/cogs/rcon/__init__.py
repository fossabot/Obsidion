"""Setup rcon."""

from obsidion.bot import Obsidion
from .rcon import Rcon


def setup(bot: Obsidion) -> None:
    """Setup."""
    bot.add_cog(Rcon(bot))
