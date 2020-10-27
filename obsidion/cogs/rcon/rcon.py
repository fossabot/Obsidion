"""Rcon cog."""

from asyncrcon import AsyncRCON, AuthenticationException
from discord.ext import commands

from obsidion.bot import Obsidion


class Rcon(commands.Cog):
    """Rcon."""

    def __init__(self, bot: Obsidion) -> None:
        """Init."""
        self.bot = bot

    @commands.command()
    @commands.cooldown(rate=1, per=5.0, type=commands.BucketType.user)
    async def add_rcon(
        self, ctx: commands.Context, addr: str, pw: str, message: str
    ) -> None:
        """Setup Rcon Channel."""
        await ctx.trigger_typing()

        _rcon = AsyncRCON(addr, pw)
        try:
            await _rcon.open_connection()
        except AuthenticationException:
            await ctx.send("Login failed: Unauthorized.")
            return

        res = await _rcon.command(message)
        await ctx.send(res)

        _rcon.close()

    @commands.command()
    @commands.cooldown(rate=1, per=5.0, type=commands.BucketType.user)
    async def del_rcon(
        self, ctx: commands.Context, addr: str, pw: str, message: str
    ) -> None:
        """Delete Rcon Info."""
        await ctx.trigger_typing()

        _rcon = AsyncRCON(addr, pw)
        try:
            await _rcon.open_connection()
        except AuthenticationException:
            await ctx.send("Login failed: Unauthorized.")
            return

        res = await _rcon.command(message)
        await ctx.send(res)

        _rcon.close()

    @commands.command()
    @commands.cooldown(rate=1, per=5.0, type=commands.BucketType.user)
    async def cmd(
        self, ctx: commands.Context, addr: str, pw: str, message: str
    ) -> None:
        """Send Command via Rcon."""
        await ctx.trigger_typing()

        _rcon = AsyncRCON(addr, pw)
        try:
            await _rcon.open_connection()
        except AuthenticationException:
            await ctx.send("Login failed: Unauthorized.")
            return

        res = await _rcon.command(message)
        await ctx.send(res)

        _rcon.close()

    @commands.command()
    @commands.cooldown(rate=1, per=5.0, type=commands.BucketType.user)
    async def blacklist(
        self, ctx: commands.Context, addr: str, pw: str, message: str
    ) -> None:
        """Edit blacklisted commands."""
        await ctx.trigger_typing()

        _rcon = AsyncRCON(addr, pw)
        try:
            await _rcon.open_connection()
        except AuthenticationException:
            await ctx.send("Login failed: Unauthorized.")
            return

        res = await _rcon.command(message)
        await ctx.send(res)

        _rcon.close()

    @commands.command()
    @commands.cooldown(rate=1, per=5.0, type=commands.BucketType.user)
    async def log(
        self, ctx: commands.Context, addr: str, pw: str, message: str
    ) -> None:
        """Setup Log Channel."""
        await ctx.trigger_typing()

        _rcon = AsyncRCON(addr, pw)
        try:
            await _rcon.open_connection()
        except AuthenticationException:
            await ctx.send("Login failed: Unauthorized.")
            return

        res = await _rcon.command(message)
        await ctx.send(res)

        _rcon.close()

    @commands.command()
    @commands.cooldown(rate=1, per=5.0, type=commands.BucketType.user)
    async def send(
        self, ctx: commands.Context, addr: str, pw: str, message: str
    ) -> None:
        """Send Message to Minecraft Server."""
        await ctx.trigger_typing()

        _rcon = AsyncRCON(addr, pw)
        try:
            await _rcon.open_connection()
        except AuthenticationException:
            await ctx.send("Login failed: Unauthorized.")
            return

        res = await _rcon.command(message)
        await ctx.send(res)

        _rcon.close()