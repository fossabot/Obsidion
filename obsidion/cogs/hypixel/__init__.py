from .hypixel import hypixel


def setup(bot):
    bot.add_cog(hypixel(bot))
