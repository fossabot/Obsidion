"""Config related commands."""
import json

import discord
from discord.ext import commands

from obsidion.bot import Obsidion
from obsidion import constants


class Config(commands.Cog):
    """Config class."""

    def __init__(self, bot: Obsidion) -> None:
        """Init."""
        self.bot = bot

    @commands.group()
    async def account(self, ctx: commands.Context) -> None:
        """Discord account linking."""
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    @account.command(name="link")
    async def account_link(self, ctx: commands.Context, username: str) -> None:
        """Link account to discord account."""
        if await self.bot.db_pool.fetch(
            "SELECT username FROM discord_user WHERE id = $1", ctx.author.id
        ):
            await self.bot.db_pool.execute(
                "UPDATE discord_user SET username = $1 WHERE id = $2",
                username,
                ctx.author.id,
            )
        else:
            await self.bot.db_pool.execute(
                "INSERT INTO discord_user (id, username) VALUES ($1, $2)",
                ctx.author.id,
                username,
            )
        await ctx.send(f"Your account has been linked to {username}")

    @account.command(name="unlink")
    async def account_unlink(self, ctx: commands.Context) -> None:
        """Unlink minecraft account to discord account."""
        await self.bot.db_pool.execute(
            "UPDATE discord_user SET username = $1 WHERE id = $2", None, ctx.author.id
        )
        await ctx.send("Your account has been unlinked from any minecraft account")

    @commands.guild_only()
    @commands.group()
    @commands.has_guild_permissions(administrator=True)
    async def serverlink(self, ctx: commands.Context) -> None:
        """:ink a minecraft server to your guild."""
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    @serverlink.command(name="link")
    async def serverlink_link(self, ctx: commands.Context, server: str) -> None:
        """Link miencraft server to discord server."""
        if await self.bot.db_pool.fetch(
            "SELECT server FROM guild WHERE id = $1", ctx.guild.id
        ):
            await self.bot.db_pool.execute(
                "UPDATE guild SET server = $1 WHERE id = $2", server, ctx.guild.id
            )
        else:
            await self.bot.db_pool.execute(
                "INSERT INTO guild (id, server) VALUES ($1, $2)",
                ctx.guild.id,
                server,
            )

        await ctx.send(f"Your discord server has been linked to {server}")

    @serverlink.command(name="unlink")
    async def serverlink_unlink(self, ctx: commands.Context) -> None:
        """Unlink server from discord server."""
        await self.bot.db_pool.execute(
            "UPDATE guild SET server = $1 WHERE id = $2", None, ctx.guild.id
        )

        await ctx.send("Your discord server is no longer linked to a minecraft server")

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def prefix(self, ctx: commands.Context, new_prefix: str) -> None:
        """Set a custom prefix for the bot commands."""
        cur_prefix = ctx.prefix

        if cur_prefix == new_prefix:
            await ctx.send(
                f"{ctx.author}, You are already using that as your "
                + "set prefix for this guild.`"
            )
            return
        if await self.bot.db_pool.fetch(
            "SELECT prefix FROM guild WHERE id = $1", ctx.guild.id
        ):
            await self.bot.db_pool.execute(
                "UPDATE guild SET prefix = $1 WHERE id = $2", new_prefix, ctx.guild.id
            )
        else:
            await self.bot.db_pool.execute(
                "INSERT INTO guild (id, prefix) VALUES ($1, $2)",
                ctx.guild.id,
                new_prefix,
            )
        key = f"prefix_{ctx.guild.id}"
        user_id = self.bot.user.id
        prefix = [f"<@!{user_id}> ", f"<@{user_id}> ", new_prefix]
        await self.bot.redis_session.set(key, json.dumps(prefix), expire=28800)

        await ctx.send(f"{ctx.author}, The prefix has been changed to `{new_prefix}`")

    @commands.group()
    async def delete(self, ctx: commands.Context) -> None:
        """Discord account linking."""
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    @delete.command(name="user")
    async def delete_user(self, ctx: commands.Context) -> None:
        """This will delete all data that is linked to your account."""
        embed = discord.Embed(
            title="DELETE DATA",
            description="WARNING\n THIS IS AN IRREVERABLE ACTION AND WILL "
            + "DELETE ALL DATA LINKED TO YOUR ACCOUNT\nDO YOU WISH TO PROCEED?\nYES/NO",
            colour=0xFF0000,
        )
        await ctx.send(embed=embed)

        def yes(m: discord.Message) -> bool:
            return m.author == ctx.author and m.content.lower() in ["yes", "no"]

        delete = await self.bot.wait_for("message", check=yes, timeout=10)
        if delete.content.lower() == "yes":
            # deletes data
            await self.bot.db_pool.execute(
                "DELETE FROM discord_user WHERE id = $1", ctx.author.id
            )

            await ctx.send(
                f"{ctx.message.author.mention}, all data linked to your "
                + "discord account has been deleted."
            )
    @delete.command(name="guild")
    async def delete_guild(self, ctx: commands.Context) -> None:
        """This will delete all data that is linked to this guild."""
        embed = discord.Embed(
            title="DELETE DATA",
            description="WARNING\n THIS IS AN IRREVERABLE ACTION AND WILL "
            + f"DELETE ALL DATA LINKED TO YOUR GUILD AND RESET YOUR PREFIX TO {constants.Bot.default_prefix}\nDO YOU WISH TO PROCEED?\nYES/NO",
            colour=0xFF0000,
        )
        await ctx.send(embed=embed)

        def yes(m: discord.Message) -> bool:
            return m.author == ctx.author and m.content.lower() in ["yes", "no"]

        delete = await self.bot.wait_for("message", check=yes, timeout=10)
        if delete.content.lower() == "yes":
            # deletes data
            await self.bot.db_pool.execute(
                "DELETE FROM guild WHERE id = $1", ctx.guild.id
            )

            key = f"prefix_{ctx.guild.id}"
            user_id = self.bot.user.id
            prefix = [f"<@!{user_id}> ", f"<@{user_id}> ", constants.Bot.default_prefix]
            await self.bot.redis_session.set(key, json.dumps(prefix), expire=28800)

            await ctx.send(
                f"{ctx.message.author.mention}, all data linked to your "
                + "discord account has been deleted."
            )
