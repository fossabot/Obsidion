from .events import events


def setup(bot):
    bot.add_cog(events(bot))
