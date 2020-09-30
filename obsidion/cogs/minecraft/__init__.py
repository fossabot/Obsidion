"""Setup cog."""

from .minecraft import minecraft


def setup(bot):
    """Setup."""
    bot.add_cog(minecraft(bot))
