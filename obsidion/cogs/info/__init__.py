from .info import info


def setup(bot):
    bot.add_cog(info(bot))
