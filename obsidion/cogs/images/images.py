"""Images cog."""

import logging

import discord
from discord.ext import commands

from obsidion.bot import Obsidion
from obsidion.utils.utils import usernameToUUID

log = logging.getLogger(__name__)


class Images(commands.Cog):
    """Images cog."""

    def __init__(self, bot: Obsidion) -> None:
        """Init."""
        self.session = bot.http_session
        self.bot = bot

    @commands.command(aliases=["ach", "advancement"])
    @commands.cooldown(rate=1, per=5.0, type=commands.BucketType.user)
    async def achievement(
        self, ctx: commands.Context, block_name: str, title: str, *, text: str
    ) -> None:
        """Create your very own custom Minecraft achievements."""
        await ctx.channel.trigger_typing()
        text = text.replace(" ", "%20")
        embed = discord.Embed(color=0x00FF00)
        embed.set_image(
            url=(
                "https://api.bowie-co.nz/api/v1/images/"
                f"advancement?item={block_name}&title={title}&text={text}"
            )
        )
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(rate=1, per=5.0, type=commands.BucketType.user)
    async def sign(
        self,
        ctx: commands.Context,
        *,
        text: str,
    ) -> None:
        """Create a Minecraft sign with custom text."""
        await ctx.channel.trigger_typing()
        split = text.replace(" ", "%20").split("|")
        line1 = split[0] if len(split) >= 1 else "%20"
        line2 = split[1] if len(split) >= 2 else "%20"
        line3 = split[2] if len(split) >= 3 else "%20"
        line4 = split[3] if len(split) >= 4 else "%20"
        embed = discord.Embed(color=0x00FF00)
        embed.set_image(
            url=(
                "https://api.bowie-co.nz/api/v1/images/sign?line1="
                f"{line1}&line2={line2}&line3={line3}&line4={line4}"
            )
        )
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(rate=1, per=5.0, type=commands.BucketType.user)
    async def avatar(self, ctx: commands.Context, username: str) -> None:
        """Renders a Minecraft players face."""
        await ctx.channel.trigger_typing()
        uuid = await usernameToUUID(username, ctx.bot.http_session)
        if uuid:
            embed = discord.Embed(
                description=(
                    f"Here is: `{username}`'s Face! "
                    f"\n **[DOWNLOAD](https://visage.surgeplay.com/face/512/{uuid})**"
                ),
                color=0x00FF00,
            )
            embed.set_image(url=f"https://visage.surgeplay.com/face/512/{uuid}")

            await ctx.send(embed=embed)
        else:
            await ctx.send(
                (
                    f"{ctx.message.author.mention}, :x: The user: "
                    f"`{username}` does not exist!"
                )
            )

    @commands.command()
    @commands.cooldown(rate=1, per=5.0, type=commands.BucketType.user)
    async def skull(self, ctx: commands.Context, username: str = None) -> None:
        """Renders a Minecraft players skull."""
        await ctx.channel.trigger_typing()
        uuid = await usernameToUUID(username, ctx.bot.http_session)
        if uuid:
            embed = discord.Embed(
                description=(
                    f"Here is: `{username}`'s Skull! \n "
                    f"**[DOWNLOAD](https://visage.surgeplay.com/head/512/{uuid})**"
                ),
                color=0x00FF00,
            )
            embed.set_image(url=f"https://visage.surgeplay.com/head/512/{uuid}")

            await ctx.send(embed=embed)
        else:
            await ctx.send(
                (
                    f"{ctx.message.author.mention}, :x: The user: `{username}` "
                    "does not exist!"
                )
            )

    @commands.command()
    @commands.cooldown(rate=1, per=5.0, type=commands.BucketType.user)
    async def skin(self, ctx: commands.Context, username: str) -> None:
        """Renders a Minecraft players skin."""
        await ctx.channel.trigger_typing()
        uuid = await usernameToUUID(username, ctx.bot.http_session)
        if uuid:
            embed = discord.Embed(
                description=(
                    f"Here is: `{username}`'s Skin! \n "
                    f"**[DOWNLOAD](https://visage.surgeplay.com/full/512/{uuid})**"
                ),
                color=0x00FF00,
            )
            embed.set_image(url=f"https://visage.surgeplay.com/full/512/{uuid}")

            await ctx.send(embed=embed)
        else:
            await ctx.send(
                (
                    f"{ctx.message.author.mention}, :x: The user: "
                    "`{username}` does not exist!"
                )
            )

    @commands.command()
    @commands.cooldown(rate=1, per=5.0, type=commands.BucketType.user)
    async def render(
        self, ctx: commands.Context, render_type: str, username: str
    ) -> None:
        """Renders a Minecraft players skin in 6 different ways.

        You can choose from these 6 render types: face,
        front, frontfull, head, bust & skin.
        """
        await ctx.channel.trigger_typing()
        renders = ["face", "front", "frontfull", "head", "bust", "skin"]
        if render_type not in renders:
            await ctx.send(
                (
                    f"{ctx.message.author.mention}, Please supply a render type. Your "
                    "options are:\n `face`, `front`, `frontfull`, `head`, `bust`, "
                    "`skin` \n Type: ?render <render type> <username>"
                )
            )
            return
        uuid = await usernameToUUID(username, ctx.bot.http_session)
        if uuid:
            embed = discord.Embed(
                description=(
                    f"Here is: `{username}`'s {render_type}! \n "
                    f"**[DOWNLOAD](https://visage.surgeplay.com/{render_type}"
                    f"/512/{uuid})**"
                ),
                color=0x00FF00,
            )
            embed.set_image(
                url=f"https://visage.surgeplay.com/{render_type}/512/{uuid}"
            )

            await ctx.send(embed=embed)
        else:
            await ctx.send(
                (
                    f"{ctx.message.author.mention}, :x: The user: `{username}`"
                    " does not exist!"
                )
            )
