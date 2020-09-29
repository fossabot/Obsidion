from .images import images


def setup(bot):
    bot.add_cog(images(bot))
