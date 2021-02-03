"""Setup hypixel."""
from .hypixel import hypixel


def setup(bot) -> None:
    """Setup."""
    bot.add_cog(hypixel(bot))