"""Setup rcon."""

from .rcon import Rcon


def setup(bot):
    """Setup."""
    bot.add_cog(Rcon(bot))
