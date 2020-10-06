"""Redstone cogs."""

import logging
from math import ceil, floor

from discord.ext import commands

from obsidion.bot import Obsidion

log = logging.getLogger(__name__)


class Redstone(commands.Cog):
    """Commands that are bot related."""

    def __init__(self, bot: Obsidion) -> None:
        """Init."""
        self.bot = bot

    @commands.command()
    @commands.cooldown(rate=1, per=1.0, type=commands.BucketType.user)
    async def storage(self, ctx: commands.Context, items: int) -> None:
        """Calculate how many chests and shulkers you need for that number of items."""
        chest_count = round(items / (64 * 54) + 1, None)

        if chest_count == 1:
            await ctx.send("You need 1 chest or shulker box")
            return
        double_chests = int(chest_count / 2)
        shulker_chests = round(chest_count / (64 * 54) + 1, None)
        shulkers_in_slots = chest_count % (54)
        if chest_count % 2 == 1:
            await ctx.send(
                (
                    f"You need {double_chests:,} double chests and a single chest "
                    f"or you will need {shulker_chests} chest full of shulkers with "
                    f"{shulkers_in_slots} shulkers in the last chest"
                )
            )
        else:
            await ctx.send(
                (
                    f"You need {double_chests:,} double chests or you will "
                    f"need {shulker_chests:,} chest full of shulkers with "
                    f"{shulkers_in_slots} shulkers in the last chest"
                )
            )

    @commands.command()
    @commands.cooldown(rate=1, per=1.0, type=commands.BucketType.user)
    async def comparator(self, ctx: commands.Context, item_count: int) -> None:
        """Calculate the strength of a comparator output only works for a chest."""
        signal_strength = floor(1 + ((item_count / 64) / 54) * 14)
        await ctx.send(f"Comparator output of {signal_strength}")

    @commands.command()
    @commands.cooldown(rate=1, per=1.0, type=commands.BucketType.user)
    async def itemsfromredstone(self, ctx: commands.Context, item_count: int) -> None:
        """Calculate how many items for a redstone signal."""
        signal_strength = max(item_count, ceil((54 * 64 / 14) * (item_count - 1)))
        await ctx.send(f"You need at least {signal_strength} items")

    @commands.command()
    @commands.cooldown(rate=1, per=1.0, type=commands.BucketType.user)
    async def tick2second(self, ctx: commands.Context, ticks: int) -> None:
        """Convert seconds to tick."""
        seconds = ticks / 20
        await ctx.send(f"It takes {seconds} second for {ticks} to happen.")

    @commands.command()
    @commands.cooldown(rate=1, per=1.0, type=commands.BucketType.user)
    async def second2tick(self, ctx: commands.Context, seconds: float) -> None:
        """Convert ticks to seconds."""
        ticks = seconds * 20
        await ctx.send(f"There are {ticks} ticks in {seconds} seconds")

    @commands.command()
    async def seed(self, ctx: commands.Context, *, text: str) -> None:
        """Convert text to minecraft numerical seed."""
        h = 0
        for c in text:
            h = (31 * h + ord(c)) & 0xFFFFFFFF
        await ctx.send(((h + 0x80000000) & 0xFFFFFFFF) - 0x80000000)
