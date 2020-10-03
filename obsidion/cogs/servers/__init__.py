"""Setup server info."""

from obsidion.bot import Obsidion
from .servers import Servers


def setup(bot: Obsidion) -> None:
    """Setup."""
    bot.add_cog(Servers(bot))
