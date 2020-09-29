from .minecraft import minecraft


def setup(bot):
    bot.add_cog(minecraft(bot))
