"""Hypixel related commands."""

from asyncpixel import Client
import discord
from discord.ext import commands

from obsidion import constants
from obsidion.utils.utils import usernameToUUID


class hypixel(commands.Cog):
    """Hypixel cog."""

    def __init__(self, bot) -> None:
        """Init."""
        self.bot = bot
        self.session = bot.http_session

        self.hypixel_session = Client(api_key=str(constants.Bot.hypixelapi_token))

    @commands.command()
    async def watchdogstats(self, ctx: commands.Context) -> None:
        """Get the current watchdog statistics."""
        await ctx.channel.trigger_typing()
        data = await self.hypixel_session.get_watchdog_stats()
        embed = discord.Embed(title="Watchdog Stats", colour=0x00FF00)
        embed.add_field(
            name="Total Bans", value=f"{(data.watchdog_total + data.staff_total):,}"
        )
        embed.add_field(
            name="Watchdog Rolling Daily", value=f"{data.watchdog_rollingDaily:,}"
        )
        # embed.add_field(name="Last Minute", value=f"{data.last_minute:,}")
        embed.add_field(name="Staff Total", value=f"{data.staff_total:,}")
        embed.add_field(
            name="Staff Rolling Daily", value=f"{data.staff_rollingDaily:,}"
        )
        embed.timestamp = ctx.message.created_at
        await ctx.send(embed=embed)

    @commands.command()
    async def boosters(self, ctx: commands.Context) -> None:
        """Get the current boosters online."""
        await ctx.channel.trigger_typing()
        data = await self.hypixel_session.get_boosters()
        # it is a tuple of a list of all the different boosters
        embed = discord.Embed(
            title="Boosters",
            description=f"Total Boosters online: {len(data.boosters):,}",
            colour=0x00FF00,
        )
        embed.set_author(
            name="Hypixel",
            url="https://hypixel.net/forums/skyblock.157/",
            icon_url="https://hypixel.net/favicon-32x32.png",
        )
        embed.set_thumbnail(
            url="https://hypixel.net/styles/hypixel-v2/images/header-logo.png"
        )
        embed.timestamp = ctx.message.created_at
        await ctx.send(embed=embed)

    @commands.command()
    async def playercount(self, ctx: commands.Context) -> None:
        """Get the current players online."""
        await ctx.channel.trigger_typing()
        data = await self.hypixel_session.get_player_count()
        embed = discord.Embed(
            title="Players Online",
            description=f"Total Players online: {data}",            
            colour=0x00FF00,
        )
        embed.set_author(
            name="Hypixel",
            url="https://hypixel.net/forums/skyblock.157/",
            icon_url="https://hypixel.net/favicon-32x32.png",
        )
        embed.set_thumbnail(
            url="https://hypixel.net/styles/hypixel-v2/images/header-logo.png"
        )
        embed.timestamp = ctx.message.created_at
        await ctx.send(embed=embed)

    @commands.command()
    async def skyblocknews(self, ctx: commands.Context) -> None:
        """Get current Skyblock News."""
        await ctx.channel.trigger_typing()
        data = await self.hypixel_session.get_news()

        embed = discord.Embed(
                title="Skyblock News",
                description=f"There are currently {len(data)} news articles.",
                colour=0x00FF00,
            )
        embed.set_author(
            name="Hypixel",
            url="https://hypixel.net/forums/skyblock.157/",
            icon_url="https://hypixel.net/favicon-32x32.png",
        )
        embed.set_thumbnail(
            url="https://hypixel.net/styles/hypixel-v2/images/header-logo.png"
        )
        for i in range(len(data)):
            embed.add_field(name=f"{data[i].title}", value=f"[{data[i].text}]({data[i].link})")

        embed.timestamp = ctx.message.created_at
        await ctx.send(embed=embed)
            
    @commands.command()
    async def playerstatus(self, ctx: commands.Context, username: str) -> None:
        """Get the current players online."""
        await ctx.channel.trigger_typing()
        data = await self.hypixel_session.get_player_status(uuid=await usernameToUUID(username, ctx.bot.http_session))
        # embed = discord.Embed(
        #     title="Players Online",
        #     description=f"Total Players online: {data}",            
        #     colour=0x00FF00,
        # )
        # embed.set_author(
        #     name="Hypixel",
        #     url="https://hypixel.net/forums/skyblock.157/",
        #     icon_url="https://hypixel.net/favicon-32x32.png",
        # )
        # embed.set_thumbnail(
        #     url="https://hypixel.net/styles/hypixel-v2/images/header-logo.png"
        # )
        # embed.timestamp = ctx.message.created_at
        await ctx.send(data)