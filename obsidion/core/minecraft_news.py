import logging
from datetime import datetime
from time import mktime
import discord
import feedparser
from discord.ext import commands, tasks

from obsidion.bot import Obsidion

Minecraft_News_RSS = "https://www.minecraft.net/en-us/feeds/community-content/rss"
Categories = ("Minecraft Builds", "News", "Deep Dives", "Guides")

log = logging.getLogger(__name__)


class MinecraftNews(commands.Cog):
    """Post minecraft news"""

    def __init__(self, bot: Obsidion):
        self.bot = bot
        self.last_data = datetime.now()
        self.get_media.start()

    @tasks.loop(minutes=10)
    async def get_media(self) -> None:
        async with self.bot.http_session.get(Minecraft_News_RSS) as resp:
            text = await resp.text()
        data = feedparser.parse(text)

        # select the most recent post
        latest_post = data["entries"][0]

        # run checks to see wether it should be posted

        time = datetime.fromtimestamp(mktime(latest_post["published_parsed"]))

        if time <= self.last_data:
            return
        # create discord embed
        description = f"Summary: {latest_post['summary']}"

        embed = discord.Embed(
            title=latest_post["title_detail"]["value"]
            .replace("--", ": ")
            .replace("-", " ")
            .upper(),
            description=description,
            colour=0x00FF00,
            url=latest_post["id"],
        )

        # add categories
        embed.set_image(url=f"https://minecraft.net{latest_post['imageurl']}")
        embed.add_field(name="Category", value=latest_post["primarytag"])
        # author info
        # embed.set_thumbnail =
        # embed.add_field(name="Author:", value)

        # create footer
        embed.set_footer(text="Article Published")
        embed.timestamp = time
        self.last_data = time

        # create title
        embed.set_author(
            name="New Article on Minecraft.net",
            url=f"https://minecraft.net{latest_post['imageurl']}",
            icon_url="https://www.minecraft.net/etc.clientlibs/minecraft/clientlibs/main/resources/img/menu/menu-buy--reversed.gif",
        )

        # send embed
        channel = self.bot.get_channel(725790318938685520)
        message = await channel.send(embed=embed)
        await message.publish()

    def cog_unload(self) -> None:
        """Stop news posting tasks on cog unload."""
        self.get_media.cancel()


def setup(bot: Obsidion) -> None:
    """Add `News` cog."""
    bot.add_cog(MinecraftNews(bot))
