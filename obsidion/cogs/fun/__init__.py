"""Fun setup."""

from .fun import fun


def setup(bot):
    """Setup."""
    bot.add_cog(fun(bot))
