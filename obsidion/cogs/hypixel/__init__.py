"""Setup hypixel."""

from .hypixel import hypixel


def setup(bot):
    """Setup."""
    bot.add_cog(hypixel(bot))
