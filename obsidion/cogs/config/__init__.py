from .config import config


def setup(bot):
    bot.add_cog(config(bot))
