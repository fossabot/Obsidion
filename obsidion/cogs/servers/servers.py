import discord
from discord.ext import commands
from .utils import (
    wyncraftClasses,
    hiveMCStatus,
    hiveMCGameStats,
    hiveMCRank,
    manacube,
    blocksmc,
    universocraft,
    minesaga,
    gommehd,
    veltpvp,
)
from obsidion.utils.utils import usernameToUUID
import json

hive_con = {
    # "survival_games": "SG",
    "blockparty": "BP",
    "cowboys_and_indians": "CAI",
    "cranked": "CR",
    "deathrun": "DR",
    "the_herobrine": "HB",
    "sg:heros": "HERO",
    "hide_and_seek": "HIDE",
    "one_in_the_chamber": "OITC",
    "splegg": "SP",
    "trouble_in_mineville": "TIMV",
    "skywars": "SKY",
    "the_lab": "LAB",
    "draw_it": "DRAW",
    "slaparoo": "SLAP",
    "electric_floor": "EF",
    "music_masters": "MM",
    "gravity": "GRAV",
    "restaurant_rush": "RR",
    "skygiants": "GNT",
    "skygiants:_mini": "GNTM",
    "pumpkinfection": "PMK",
    "survival_games_2": "SGN",
    "batterydash": "BD",
    "sploop": "SPL",
    "murder_in_mineville": "MIMV",
    "bedwars": "BED",
    "survive_the_night": "SURV",
    "explosive_eggs": "EE",
}


class servers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(rate=1, per=5.0, type=commands.BucketType.user)
    async def wyncraft(self, ctx: commands.Context, username: str):
        """Get statistics of a player on wynncraft."""
        await ctx.trigger_typing()
        if await self.bot.redis_session.exists(f"wyncraft_{username}"):
            data = json.loads(await self.bot.redis_session.get(f"wyncraft_{username}"))
        else:
            data = await wyncraftClasses(username, ctx.bot.http_session)
            self.bot.redis_session.set(
                f"wyncraft_{username}", json.dumps(data), expire=28800
            )
        if not data:
            await ctx.send(
                f"`{username}` has not logged onto Wynncraft or their status is not available."
            )
            return
        len_data = len(data["classes"])
        embed = discord.Embed(color=0xA4EC66)
        embed.set_author(
            name=f"WynnCraft information for {username}",
            url=f"https://wynncraft.com/stats/player/{username}",
            icon_url="https://cdn.wynncraft.com/img/wynn.png",
        )
        embed.set_thumbnail(
            url=f"https://visage.surgeplay.com/bust/{await usernameToUUID(username, ctx.bot.http_session)}"
        )
        embed.timestamp = ctx.message.created_at
        for i in range(len_data):
            embed.add_field(
                name=data["classes"][i]["class_name"],
                value=(
                    f"Class Name: `{data['classes'][i]['class_name']}`\n"
                    f"Class Level: `{data['classes'][i]['class_level']}`\n"
                    f"Class Deaths: `{data['classes'][i]['class_deaths']}`"
                ),
            )
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(rate=1, per=5.0, type=commands.BucketType.user)
    async def gommehd(self, ctx: commands.Context, username: str):
        """Get statistics of a player on gommehd."""
        await ctx.trigger_typing()
        if await self.bot.redis_session.exists(f"gommehd_{username}"):
            data = json.loads(await self.bot.redis_session.get(f"gommehd_{username}"))
        else:
            data = await gommehd(username, ctx.bot.http_session)
            self.bot.redis_session.set(
                f"gommehd_{username}", json.dumps(data), expire=28800
            )
        if data == False:
            await ctx.send(
                f"`{username}` has not logged onto GommeHD or their status is not available."
            )
            return
        embed = discord.Embed(color=0xF1A90F)
        embed.set_author(
            name=f"GommeHD information for {username}",
            url=f"https://www.gommehd.net/player/index?playerName={username}",
            icon_url="https://www.gommehd.net/images/brandmark@3x.png",
        )
        embed.set_thumbnail(
            url=f"https://visage.surgeplay.com/bust/{await usernameToUUID(username, ctx.bot.http_session)}"
        )
        embed.timestamp = ctx.message.created_at
        for game in data["game_stats"]:
            value = ""
            name = list(game)
            name_new = name[0]
            scores = game[name_new]
            for key in scores.keys():
                value += f"{key}: {scores[key]}\n"
            embed.add_field(name=name_new, value=value)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(rate=1, per=5.0, type=commands.BucketType.user)
    async def veltpvp(self, ctx: commands.Context, username: str):
        """Get statistics of a player on veltpvp."""
        await ctx.trigger_typing()
        if await self.bot.redis_session.exists(f"veltpvp_{username}"):
            data = json.loads(await self.bot.redis_session.get(f"veltpvp_{username}"))
        else:
            data = await veltpvp(username, ctx.bot.http_session)
            self.bot.redis_session.set(
                f"veltpvp_{username}", json.dumps(data), expire=28800
            )
        if not data:
            await ctx.send(
                f"`{username}` has not logged onto VeltPVP or their status is not available."
            )
            return
        embed = discord.Embed(color=0x2E39A7)
        embed.set_author(
            name=f"VeltPVP information for {username}",
            url=f"https://www.veltpvp.com/u/{username}",
            icon_url="https://www.veltpvp.com/resources/images/nav-logo.png",
        )
        embed.set_thumbnail(
            url=f"https://visage.surgeplay.com/bust/{await usernameToUUID(username, ctx.bot.http_session)}"
        )
        embed.timestamp = ctx.message.created_at
        embed.add_field(
            name=("VeltPVP Stats"),
            value=(
                f"Rank: `{data['rank']}`\nLast Seen: `{data['last_seen']}`\nCurrent Status: `{data['current_status']}`\nFirst Joined: `{data['first_joined']}`\nTime Played: `{data['time_played']}`"
            ),
        )
        embed.add_field(
            name=("VeltPVP HCF Stats"),
            value=(
                f"Kills: `{data['game_stats'][0]['HCF']['Kills']}`\nDeaths: `{data['game_stats'][0]['HCF']['Deaths']}`\nKDR: `{data['game_stats'][0]['HCF']['KDR']}`"
            ),
        )
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(rate=1, per=5.0, type=commands.BucketType.user)
    async def blocksmc(self, ctx: commands.Context, username: str):
        """Get statistics of a player on blocksmc."""
        await ctx.trigger_typing()
        if await self.bot.redis_session.exists(f"blocksmc_{username}"):
            data = json.loads(await self.bot.redis_session.get(f"blocksmc_{username}"))
        else:
            data = await blocksmc(username, ctx.bot.http_session)
            self.bot.redis_session.set(
                f"blocksmc_{username}", json.dumps(data), expire=28800
            )
        if not data:
            await ctx.send(
                f"`{username}` has not logged onto BlocksMC or their status is not available."
            )
            return
        embed = discord.Embed(color=0x008CD3)
        embed.set_author(
            name=f"BlocksMC information for {username}",
            url=f"https://blocksmc.com/player/{username}",
            icon_url="https://blocksmc.com/templates3/src/logo-gray-sm.png",
        )
        embed.set_thumbnail(
            url=f"https://visage.surgeplay.com/bust/{await usernameToUUID(username, ctx.bot.http_session)}"
        )
        embed.timestamp = ctx.message.created_at
        for game in data["game_stats"]:
            value = ""
            name = list(game)
            name_new = name[0]
            scores = game[name_new]
            for key in scores.keys():
                value += f"{key}: {scores[key]}\n"
            embed.add_field(name=name_new, value=value)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(rate=1, per=5.0, type=commands.BucketType.user)
    async def universocraft(self, ctx: commands.Context, username: str):
        """Get statistics of a player on universocraft."""
        await ctx.trigger_typing()
        if await self.bot.redis_session.exists(f"universocraft_{username}"):
            data = json.loads(
                await self.bot.redis_session.get(f"universocraft_{username}")
            )
        else:
            data = await universocraft(username, ctx.bot.http_session)
            self.bot.redis_session.set(
                f"universocraft_{username}", json.dumps(data), expire=28800
            )
        if not data:
            await ctx.send(
                f"`{username}` has not logged onto UniversoCraft or their status is not available."
            )
            return
        embed = discord.Embed(color=0x82C228)
        embed.set_author(
            name=f"UniversoCraft information for {username}",
            url=f"https://www.universocraft.com/members/{username}",
            icon_url="https://www.universocraft.com/favicon.ico",
        )
        embed.set_thumbnail(
            url=f"https://visage.surgeplay.com/bust/{await usernameToUUID(username, ctx.bot.http_session)}"
        )
        embed.timestamp = ctx.message.created_at
        for game in data["game_stats"]:
            value = ""
            name = list(game)
            name_new = name[0]
            scores = game[name_new]
            for key in scores.keys():
                value += f"{key}: {scores[key]}\n"
            embed.add_field(name=name_new, value=value)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(rate=1, per=5.0, type=commands.BucketType.user)
    async def minesaga(self, ctx: commands.Context, username: str):
        """Get statistics of a player on minesaga."""
        await ctx.trigger_typing()
        if await self.bot.redis_session.exists(f"minesaga_{username}"):
            data = json.loads(await self.bot.redis_session.get(f"minesaga_{username}"))
        else:
            data = await minesaga(username, ctx.bot.http_session)
            self.bot.redis_session.set(
                f"minesaga_{username}", json.dumps(data), expire=28800
            )
        if not data:
            await ctx.send(
                f"`{username}` has not logged onto Minesaga or their status is not available."
            )
            return
        embed = discord.Embed(color=0x6696C2)
        embed.set_author(
            name=f"Minesaga information for {username}",
            url=f"https://www.minesaga.org/members/{username}",
            icon_url="https://www.minesaga.org/favicon.ico",
        )
        embed.set_thumbnail(
            url=f"https://visage.surgeplay.com/bust/{await usernameToUUID(username, ctx.bot.http_session)}"
        )
        embed.timestamp = ctx.message.created_at
        for game in data["game_stats"]:
            value = ""
            name = list(game)
            name_new = name[0]
            scores = game[name_new]
            for key in scores.keys():
                value += f"{key}: {scores[key]}\n"
            embed.add_field(name=name_new, value=value)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(rate=1, per=5.0, type=commands.BucketType.user)
    async def manacube(self, ctx: commands.Context, username: str):
        """Get statistics of a player on manacube."""
        await ctx.trigger_typing()
        if await self.bot.redis_session.exists(f"manacube_{username}"):
            data = json.loads(await self.bot.redis_session.get(f"manacube_{username}"))
        else:
            data = await manacube(username, ctx.bot.http_session)
            self.bot.redis_session.set(
                f"manacube_{username}", json.dumps(data), expire=28800
            )
        if not data:
            await ctx.send(
                f"`{username}` has not logged onto Minesaga or their status is not available."
            )
            return
        embed = discord.Embed(color=0x11B7C4)
        embed.set_author(
            name=f"Manacube information for {username}",
            url=f"https://manacube.com/stats/player/{username}/",
            icon_url="https://manacube.com/styles/ndzn/manacube/img/logo-cube.png",
        )
        embed.set_thumbnail(
            url=f"https://visage.surgeplay.com/bust/{await usernameToUUID(username, ctx.bot.http_session)}"
        )
        embed.timestamp = ctx.message.created_at
        embed.add_field(
            name=("Manacube Stats"),
            value=(
                f"Rank: `{data['rank']}`\nCubits: `{data['cubits']}`\nFirst Seen: `{data['firstSeen']}`\nLast Seen: `{data['lastSeenAgo']}`"
            ),
        )
        embed.add_field(
            name=("Manacube Parkour Stats"),
            value=(
                f"Playtime: `{data['parkour']['playtime']}`\nMana: `{data['parkour']['mana']}`\nScore: `{data['parkour']['score']}`\nCourses: `{data['parkour']['courses']}`"
            ),
        )
        embed.add_field(
            name=("Manacube Axtec Stats"),
            value=(
                f"Playtime: `{data['aztec']['playtime']}`\nMob Kills: `{data['aztec']['mobKills']}`\nMana: `{data['aztec']['mana']}`\nMoney: `{data['aztec']['money']}`"
            ),
        )
        embed.add_field(
            name=("Manacube Oasis Stats"),
            value=(
                f"Playtime: `{data['oasis']['playtime']}`\nMob Kills: `{data['oasis']['mobKills']}`\nMana: `{data['oasis']['mana']}`\nMoney: `{data['oasis']['money']}`"
            ),
        )
        embed.add_field(
            name=("Manacube Islands Stats"),
            value=(
                f"Playtime: `{data['islands']['playtime']}`\nMob Kills: `{data['islands']['mobKills']}`\nSilver: `{data['islands']['silver']}`\nMoney: `{data['islands']['money']}`"
            ),
        )
        embed.add_field(
            name=("Manacube Survival Stats"),
            value=(
                f"Playtime: `{data['survival']['playtime']}`\nMob Kills: `{data['survival']['mobKills']}`\nMoney: `{data['survival']['money']}`\nQuests: `{data['survival']['quests']}`"
            ),
        )

        embed.add_field(
            name=("Manacube Aether Stats"),
            value=(
                f"Playtime: `{data['aether']['playtime']}`\nMining Level: `{data['aether']['miningLevel']}`\nMoney: `{data['aether']['money']}`\nRebirths: `{data['aether']['rebirths']}`"
            ),
        )
        embed.add_field(
            name=("Manacube Atlas Stats"),
            value=(
                f"Playtime: `{data['atlas']['playtime']}`\nMining Level: `{data['atlas']['miningLevel']}`\nMoney: `{data['atlas']['money']}`\nRebirths: `{data['aether']['rebirths']}`"
            ),
        )
        embed.add_field(
            name=("Manacube Creative Stats"),
            value=(
                f"Playtime: `{data['creative']['playtime']}`\nBlocks Placed: `{data['creative']['blocksplaced']}`\nBlocks Broken: `{data['creative']['blocksbroken']}`"
            ),
        )
        embed.add_field(
            name=("Manacube KitPvP Stats"),
            value=(
                f"Playtime: `{data['kitpvp']['playtime']}`\nLevel: `{data['kitpvp']['level']}`\nMoney: `{data['kitpvp']['money']}`\nKills: `{data['kitpvp']['kills']}`"
            ),
        )
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(rate=1, per=5.0, type=commands.BucketType.user)
    async def hiverank(self, ctx: commands.Context, username: str):
        """View the rank of a player on hiverank."""
        await ctx.trigger_typing()
        if await self.bot.redis_session.exists(f"hiveMCRank_{username}"):
            data = json.loads(
                await self.bot.redis_session.get(f"hiveMCRank_{username}")
            )
        else:
            data = await hiveMCRank(username, ctx.bot.http_session)
            self.bot.redis_session.set(
                f"hiveMCRank_{username}", json.dumps(data), expire=28800
            )
        if not data:
            await ctx.send(
                f"`{username}` has not logged onto Hive or there are no ranks available."
            )
            return
        embed = discord.Embed(color=0xFFAF03)
        embed.set_author(
            name=f"Hive rank for {username}",
            url=f"https://www.hivemc.com/player/{username}",
            icon_url="https://www.hivemc.com/img/white-logo.png",
        )
        embed.set_thumbnail(
            url=f"https://visage.surgeplay.com/bust/{await usernameToUUID(username, ctx.bot.http_session)}"
        )
        embed.timestamp = ctx.message.created_at
        embed.add_field(name="rank", value=(f"Rank: `{data['rank'][0]}`"))
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(rate=1, per=5.0, type=commands.BucketType.user)
    async def hivestatus(self, ctx: commands.Context, username: str):
        """View the status of a player on hive"""
        await ctx.trigger_typing()
        if await self.bot.redis_session.exists(f"hiveMCStatus_{username}"):
            data = json.loads(
                await self.bot.redis_session.get(f"hiveMCStatus_{username}")
            )
        else:
            data = await hiveMCStatus(username, ctx.bot.http_session)
            self.bot.redis_session.set(
                f"hiveMCStatus_{username}", json.dumps(data), expire=28800
            )
        if not data:
            await ctx.send(
                f"`{username}` has not logged onto Hive or their status is not available."
            )
            return
        embed = discord.Embed(color=0xFFAF03)
        embed.set_author(
            name=f"Hive Status for {username}",
            url=f"https://www.hivemc.com/player/{username}",
            icon_url="https://www.hivemc.com/img/white-logo.png",
        )
        embed.set_thumbnail(
            url=f"https://visage.surgeplay.com/bust/{await usernameToUUID(username, ctx.bot.http_session)}"
        )
        embed.timestamp = ctx.message.created_at
        embed.add_field(
            name="description",
            value=(f"Description: `{data['status'][0]['description']}`"),
        )
        embed.add_field(name="game", value=(f"Game: `{data['status'][0]['game']}`"))
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(rate=1, per=5.0, type=commands.BucketType.user)
    async def hivestats(self, ctx: commands.Context, username: str, game: str):
        """Get statistics of a player on hive."""
        await ctx.trigger_typing()

        if game.lower() in hive_con:
            if await self.bot.redis_session.exists(
                f"hiveMCGameStats_{hive_con[game.lower()]}_{username}"
            ):
                data = json.loads(
                    await self.bot.redis_session.get(
                        f"hiveMCGameStats_{hive_con[game.lower()]}_{username}"
                    )
                )
            else:
                data = await hiveMCGameStats(
                    username, hive_con[game.lower()], ctx.bot.http_session
                )
                self.bot.redis_session.set(
                    f"hiveMCGameStats_{hive_con[game.lower()]}_{username}",
                    json.dumps(data),
                    expire=28800,
                )
            embed = discord.Embed(color=0xFFAF03)
            embed.set_author(
                name=f"Hive Stats for {username}",
                url=f"https://www.hivemc.com/player/{username}",
                icon_url="https://www.hivemc.com/img/white-logo.png",
            )
            embed.set_thumbnail(
                url=f"https://visage.surgeplay.com/bust/{await usernameToUUID(username, ctx.bot.http_session)}"
            )
            embed.timestamp = ctx.message.created_at
            if not data:
                await ctx.send("No stats found")
                return
            del data["stats"][0]["UUID"]
            if "cached" in data["stats"][0]:
                del data["stats"][0]["cached"]
            if "firstLogin" in data["stats"][0]:
                del data["stats"][0]["firstLogin"]
            if "lastLogin" in data["stats"][0]:
                del data["stats"][0]["lastLogin"]
            if "achievements" in data["stats"][0]:
                del data["stats"][0]["achievements"]
            if "title" in data["stats"][0]:
                del data["stats"][0]["title"]
            value = ""
            for stat in data["stats"][0]:
                if isinstance(data["stats"][0][stat], list) or isinstance(
                    data["stats"][0][stat], dict
                ):
                    pass
                else:
                    value += f"`{stat}`: {data['stats'][0][stat]}\n"
            embed.add_field(
                name=f"{game.replace('_', ' ').upper()} Stats", value=value,
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send("Sorry that game was not recognized as a Hive game")
