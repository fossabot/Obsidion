"""Fun related commands."""

import logging
from random import choice
from typing import List

from discord.ext import commands

minecraft = [
    "ᔑ",
    "ʖ",
    "ᓵ",
    "↸",
    "ᒷ",
    "⎓",
    "⊣",
    "⍑",
    "╎",
    "⋮",
    "ꖌ",
    "ꖎ",
    "ᒲ",
    "リ",
    "𝙹",
    "!",
    "¡",
    "ᑑ",
    "∷",
    "ᓭ",
    "ℸ",
    " ̣",
    "⚍",
    "⍊",
    "∴",
    " ̇",
    "|",
    "|",
    "⨅",
    "I",
    "II",
    "III",
    "IV",
    "V",
    "VI",
    "VII",
    "VIII",
    "IX",
    "X",
]
alphabet = "abcdefghijklmnopqrstuvwxyz123456789"

log = logging.getLogger(__name__)


def load_from_file(file: str) -> List[str]:
    """Load text from file

    Args:
        file (str): file name

    Returns:
        List[str]: list of input
    """
    with open(f"obsidion/cogs/fun/resources/{file}.txt") as f:
        content = f.readlines()
    return [x.strip() for x in content]


class fun(commands.Cog):
    """Commands that are fun related."""

    def __init__(self, bot) -> None:
        """Init."""
        self.bot = bot
        self.pvp_mes = load_from_file("pvp")
        self.kill_mes = load_from_file("kill")
        self.build_ideas_mes = load_from_file("build_ideas")

    @commands.command(aliases=["villagerspeak", "villagerspeech", "hmm"])
    @commands.cooldown(rate=1, per=1.0, type=commands.BucketType.user)
    async def villager(self, ctx: commands.Context, *, speech: str) -> None:
        """Convert english to Villager speech hmm."""
        split = speech.split(" ")
        sentence = ""
        for _ in split:
            sentence += " hmm"
        response = sentence.strip()
        await ctx.send(f"{ctx.message.author.mention}, `{response}`")

    @commands.command()
    @commands.cooldown(rate=1, per=1.0, type=commands.BucketType.user)
    async def enchant(self, ctx: commands.Context, *, msg: str) -> None:
        """Enchant a message."""
        response = ""
        for letter in msg:
            if letter in alphabet:
                response += minecraft[alphabet.index(letter)]
            else:
                response += letter
        await ctx.send(f"{ctx.message.author.mention}, `{response}`")

    @commands.command()
    @commands.cooldown(rate=1, per=1.0, type=commands.BucketType.user)
    async def unenchant(self, ctx: commands.Context, *, msg: str) -> None:
        """Disenchant a message."""
        response = ""
        for letter in msg:
            if letter in minecraft:
                response += alphabet[minecraft.index(letter)]
            else:
                response += letter
        await ctx.send(f"{ctx.message.author.mention}, `{response}`")

    @commands.command()
    @commands.cooldown(rate=1, per=1.0, type=commands.BucketType.user)
    async def creeper(self, ctx: commands.Context) -> None:
        """Aw man."""
        await ctx.send("Aw man")

    @commands.command(aliases=["idea", "bidea"])
    @commands.cooldown(rate=1, per=1.0, type=commands.BucketType.user)
    async def buildidea(self, ctx: commands.Context) -> None:
        """Get an idea for a new idea."""
        await ctx.send(
            f"Here is something cool to build: {choice(self.build_ideas_mes)}."
        )

    @commands.command(aliases=["slay"])
    @commands.cooldown(rate=1, per=1.0, type=commands.BucketType.user)
    async def kill(self, ctx, member=None) -> None:
        """Kill that pesky friend in a fun and stylish way."""
        if (
            not member
            or str(member) == f"<@{self.bot.owner_id}>"
            or str(member) == f"<@!{self.bot.owner_id}>"
            or str(member) == "<@691589447074054224>"
            or str(member) == "<@!691589447074054224>"
        ):
            # this included some protection for the owners and the bot itself
            await ctx.send("Good Try!")
            member = ctx.message.author.mention

        await ctx.send(choice(self.kill_mes).replace("member", member))

    @commands.command(aliases=["battle"])
    @commands.cooldown(rate=1, per=1.0, type=commands.BucketType.user)
    async def pvp(self, ctx, member1=None, member2=None) -> None:
        """Duel someone."""
        if member1:
            if not member2:
                member2 = ctx.message.author.mention

            await ctx.send(
                choice(self.pvp_mes)
                .replace("member1", member1)
                .replace("member2", member2)
            )
        else:
            await ctx.send("Please provide 2 people to fight")

    @commands.command()
    @commands.cooldown(rate=1, per=1.0, type=commands.BucketType.user)
    async def rps(self, ctx, user_choice=None) -> None:
        """play Rock Paper Shears."""
        options = ["rock", "paper", "shears"]
        if user_choice and user_choice in options:
            c_choice = choice(options)
            if user_choice == options[options.index(user_choice) - 1]:
                await ctx.send(f"You chose {user_choice}, I chose {c_choice} I win.")
            elif c_choice == user_choice:
                await ctx.send(
                    f"You chose {user_choice}, I chose {c_choice} looks like we have a tie."
                )
            else:
                await ctx.send(f"You chose {user_choice}, I chose {c_choice} you win.")
        else:
            await ctx.send(
                "That is an invalid option can you please choose from rock, paper or shears"
            )
