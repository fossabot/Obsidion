from .botlist import botlist


def setup(bot):
    bot.add_cog(botlist(bot))
