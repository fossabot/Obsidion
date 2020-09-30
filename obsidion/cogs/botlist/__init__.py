"""Import botlists."""

from .botlist import botlist


def setup(bot):
    """Setup."""
    bot.add_cog(botlist(bot))
