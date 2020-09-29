from .rcon import rcon


def setup(bot):
    bot.add_cog(rcon(bot))
