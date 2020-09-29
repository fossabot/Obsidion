from aiohypixel import HypixelSession

import discord
from discord.ext import commands

from obsidion import constants


class hypixel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.session = bot.http_session

        self.hypixel_session = HypixelSession(
            api_keys=(
                [str(constants.Bot.hypixelapi_token), "strong", "random key"]
            )  # I HATE THIS I NEED TO FIX THE LIBRARY
        )

    @commands.command()
    async def watchdogstats(self, ctx: commands.Context):
        """Get the current watchdog statistics."""
        await ctx.channel.trigger_typing()
        data = await self.hypixel_session.get_watchdog_stats()
        embed = discord.Embed(title="Watchdog Stats", colour=0x00FF00)
        embed.add_field(name="Total Bans", value=f"{data.total:,}")
        embed.add_field(name="Rolling Daily", value=f"{data.rolling_daily:,}")
        embed.add_field(name="Last Minute", value=f"{data.last_minute:,}")
        embed.add_field(name="Staff Total", value=f"{data.staff_total:,}")
        embed.add_field(
            name="Staff Rolling Daily", value=f"{data.staff_rolling_daily:,}"
        )
        embed.timestamp = ctx.message.created_at
        await ctx.send(embed=embed)

    @commands.command()
    async def boosters(self, ctx: commands.Context):
        """Get the current boosters online."""
        await ctx.channel.trigger_typing()
        data = await self.hypixel_session.get_boosters()
        # it is a tuple of a list of all the different boosters
        embed = discord.Embed(
            title="Boosters",
            description=f"Total Boosters online: {len(data[0]):,}",
            colour=0x00FF00,
        )
        await ctx.send(embed=embed)
