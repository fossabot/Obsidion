"""Setup server info."""

from .servers import Servers


def setup(bot):
    """Setup."""
    bot.add_cog(Servers(bot))
