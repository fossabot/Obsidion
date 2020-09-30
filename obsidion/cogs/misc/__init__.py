"""Setup misc."""

from .misc import Miscellaneous


def setup(bot):
    """Setup."""
    bot.add_cog(Miscellaneous(bot))
