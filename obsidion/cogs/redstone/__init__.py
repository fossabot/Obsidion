"""Redstone."""

from .redstone import Redstone


def setup(bot):
    """Setup."""
    bot.add_cog(Redstone(bot))
