"""Hypixel related commands."""

from asyncpixel import Session
import discord
from discord.ext import commands

from obsidion import constants


class hypixel(commands.Cog):
    """Hypixel cog."""

    def __init__(self, bot) -> None:
        """Init."""
        self.bot = bot
        self.session = bot.http_session

        self.hypixel_session = Session(api_key=str(constants.Bot.hypixelapi_token))

    @commands.command()
    async def watchdogstats(self, ctx: commands.Context) -> None:
        """Get the current watchdog statistics."""
        await ctx.channel.trigger_typing()
        data = await self.hypixel_session.watchdogstats()
        embed = discord.Embed(title="Watchdog Stats", colour=0x00FF00)
        embed.add_field(
            name="Total Bans", value=f"{(data.watchdog_total + data.staff_total):,}"
        )
        embed.add_field(
            name="Watchdog Rolling Daily", value=f"{data.watchdog_rollingDaily:,}"
        )
        embed.add_field(name="Last Minute", value=f"{data.last_minute:,}")
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
        await ctx.send(embed=embed)
