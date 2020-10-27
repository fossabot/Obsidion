"""Rcon cog."""

from asyncrcon import AsyncRCON, AuthenticationException
import discord
from discord.ext import commands

from obsidion.bot import Obsidion


class Rcon(commands.Cog):
    """Rcon."""

    def __init__(self, bot: Obsidion) -> None:
        """Init."""
        self.bot = bot

    async def right_channel(self, ctx: commands.Context) -> bool:
        channel = await self.bot.db_pool.fetchval(
            "SELECT channel FROM rcon WHERE id = $1", ctx.guild.id
        )
        return channel == ctx.guild.id

        return False

    async def rcon(self, server: str) -> AsyncRCON:
        address, password = await self.bot.db_pool.fetchrow(
            "SELECT (address, password) FROM rcon WHERE id = $1", server
        )
        _rcon = AsyncRCON(address, password)
        await _rcon.open_connection()

        return _rcon

    @commands.command()
    @commands.cooldown(rate=1, per=5.0, type=commands.BucketType.user)
    @commands.is_owner()
    async def add_rcon(
        self, ctx: commands.Context, addr: str, pw: str, channel: discord.TextChannel
    ) -> None:
        """Setup Rcon Channel."""
        await self.bot.db_pool.execute(
            "INSERT INTO rcon (id, address, password) VALUES ($1, $2, $3)",
            channel.id,
            addr,
            pw,
        )

    @commands.command()
    @commands.cooldown(rate=1, per=5.0, type=commands.BucketType.user)
    @commands.is_owner()
    async def del_rcon(
        self, ctx: commands.Context, addr: str, pw: str, message: str
    ) -> None:
        """Delete Rcon Info."""
        # TODO
        pass

    @commands.command()
    @commands.cooldown(rate=1, per=5.0, type=commands.BucketType.user)
    @commands.is_owner()
    async def blacklist(
        self, ctx: commands.Context, addr: str, pw: str, message: str
    ) -> None:
        """Edit blacklisted commands."""
        # TODO
        pass

    @commands.command()
    @commands.cooldown(rate=1, per=5.0, type=commands.BucketType.user)
    @commands.is_owner()
    async def log(
        self, ctx: commands.Context, addr: str, pw: str, message: str
    ) -> None:
        """Setup Log Channel."""
        # TODO
        pass

    @commands.command()
    @commands.cooldown(rate=1, per=5.0, type=commands.BucketType.user)
    @commands.right_channel()
    async def send(self, ctx: commands.Context, *, message: str) -> None:
        """Send Message to Minecraft Server."""
        await ctx.trigger_typing()

        try:
            _rcon = await self.rcon(ctx.guild.id)
        except AuthenticationException:
            await ctx.send("Login failed: Unauthorized.")
            return

        res = await _rcon.command(f"say {message}")
        await ctx.send(res)

        _rcon.close()

    @commands.command()
    @commands.cooldown(rate=1, per=5.0, type=commands.BucketType.user)
    @commands.right_channel()
    async def cmd(self, ctx: commands.Context, *, message: str) -> None:
        """Send Command via Rcon."""
        await ctx.trigger_typing()

        try:
            _rcon = await self.rcon(ctx.guild.id)
        except AuthenticationException:
            await ctx.send("Login failed: Unauthorized.")
            return

        res = await _rcon.command(message)
        await ctx.send(res)

        _rcon.close()