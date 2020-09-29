from .redstone import redstone


def setup(bot):
    bot.add_cog(redstone(bot))
