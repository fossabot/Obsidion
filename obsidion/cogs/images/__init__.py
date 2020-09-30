"""Setup images."""

from .images import Images


def setup(bot):
    """Setup."""
    bot.add_cog(Images(bot))
