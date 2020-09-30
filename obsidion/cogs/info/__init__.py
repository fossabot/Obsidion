"""Info."""

from .info import info


def setup(bot):
    """Setup."""
    bot.add_cog(info(bot))
