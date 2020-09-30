"""Redstone cogs."""

import logging
from math import ceil, floor

from discord.ext import commands

log = logging.getLogger(__name__)


class Redstone(commands.Cog):
    """Commands that are bot related."""

    def __init__(self, bot) -> None:
        """Init."""
        self.bot = bot

    @commands.command()
    @commands.cooldown(rate=1, per=1.0, type=commands.BucketType.user)
    async def storage(self, ctx, items: int) -> None:
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
                f"You need {double_chests:,} double chests and a single chest or you will need {shulker_chests} chest full of shulkers with {shulkers_in_slots} shulkers in the last chest"
            )
        else:
            await ctx.send(
                f"You need {double_chests:,} double chests or you will need {shulker_chests:,} chest full of shulkers with {shulkers_in_slots} shulkers in the last chest"
            )

    @commands.command()
    @commands.cooldown(rate=1, per=1.0, type=commands.BucketType.user)
    async def comparator(self, ctx, item_count: int) -> None:
        """Calculate the strength of a comparator output only works for a chest."""
        signal_strength = floor(1 + ((item_count / 64) / 54) * 14)
        await ctx.send(f"Comparator output of {signal_strength}")

    @commands.command()
    @commands.cooldown(rate=1, per=1.0, type=commands.BucketType.user)
    async def itemsfromredstone(self, ctx, item_count: int):
        """calculate how many items for a redstone signal."""
        signal_strength = max(item_count, ceil((54 * 64 / 14) * (item_count - 1)))
        await ctx.send(f"You need at least {signal_strength} items")

    @commands.command()
    @commands.cooldown(rate=1, per=1.0, type=commands.BucketType.user)
    async def tick2second(self, ctx, ticks: int) -> None:
        """Convert seconds to tick."""
        seconds = ticks / 20
        await ctx.send(f"It takes {seconds} second for {ticks} to happen.")

    @commands.command()
    @commands.cooldown(rate=1, per=1.0, type=commands.BucketType.user)
    async def second2tick(self, ctx, seconds: float) -> None:
        """Convert ticks to seconds."""
        ticks = seconds * 20
        await ctx.send(f"There are {ticks} ticks in {seconds} seconds")
