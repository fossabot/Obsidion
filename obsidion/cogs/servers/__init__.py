from .servers import servers


def setup(bot):
    bot.add_cog(servers(bot))
