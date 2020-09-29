from discord.ext import commands
from obsidion import constants
import discord
from datetime import datetime


class events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        if constants.Channels.new_guild_channel:
            users = sum(1 for m in guild.members if not m.bot)
            bots = sum(1 for m in guild.members if m.bot)
            members = f"Humans: `{users}/{len(guild.members)}` \n Bots: `{bots}/{len(guild.members)}`"
            embed = discord.Embed(name=f"{self.bot.user.name} has joined a guild")
            embed.set_footer(
                text=f"Guild: {len(self.bot.guilds):,} | Shard: {guild.shard_id}/{self.bot.shard_count-1} | rejoin"
            )
            guild_text = (
                f"Name: `{guild.name}`\n"
                f"ID: `{guild.id}`\n"
                f"Owner ID: `{guild.owner.id}`\n"
            )

            embed.add_field(name="Guild", value=guild_text)
            embed.add_field(name="Region", value=guild.region)
            embed.timestamp = datetime.now()
            if guild.icon_url:
                embed.set_thumbnail(url=guild.icon_url)
            else:
                embed.set_thumbnail(url="https://i.imgur.com/AFABgjD.png")
            channel = self.bot.get_channel(constants.Channels.new_guild_channel)
            await channel.send(embed=embed)
