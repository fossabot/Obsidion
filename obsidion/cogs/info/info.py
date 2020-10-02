"""Info cogs."""

import base64
from datetime import datetime
import io
import json
import logging

from aiohttp import ClientSession
import discord
from discord.ext import commands

from obsidion import constants
from obsidion.bot import Obsidion
from obsidion.utils.utils import get

log = logging.getLogger(__name__)


class Info(commands.Cog):
    """Commands that are bot related."""

    def __init__(self, bot: Obsidion) -> None:
        """Initialise the bot."""
        self.bot = bot

    @staticmethod
    async def get_uuid(session: ClientSession, username: str) -> str:
        """Get uuid from username.

        Args:
            session ([type]): aiohttp session
            username (str): username of player

        Returns:
            str: uuid if vaild username otherwise false
        """
        url = f"https://api.mojang.com/users/profiles/minecraft/{username}"
        async with session.get(url) as resp:
            if resp.status == 200:
                data = await resp.json()
                uuid = data["id"]
                return uuid
            return False

    @commands.command(
        aliases=["whois", "p", "names", "namehistory", "pastnames", "namehis"]
    )
    @commands.cooldown(rate=1, per=5.0, type=commands.BucketType.user)
    async def profile(self, ctx: commands.Context, username: str) -> None:
        """View a players Minecraft UUID, Username history and skin."""
        await ctx.channel.trigger_typing()
        if await self.bot.redis_session.exists(f"username_{username}"):
            uuid = await self.bot.redis_session.get(
                f"username_{username}", encoding="utf-8"
            )
        else:
            uuid = await self.get_uuid(ctx.bot.http_session, username)
            self.bot.redis_session.set(f"username_{username}", uuid, expire=28800)

        if not uuid:
            await ctx.send("That username is not been used.")
            return

        long_uuid = f"{uuid[0:8]}-{uuid[8:12]}-{uuid[12:16]}-{uuid[16:20]}-{uuid[20:]}"

        if await self.bot.redis_session.exists(uuid):
            names = json.loads(await self.bot.redis_session.get(uuid))
        else:
            names = await get(
                ctx.bot.http_session,
                f"https://api.mojang.com/user/profiles/{uuid}/names",
            )
            self.bot.redis_session.set(uuid, json.dumps(names), expire=28800)

        name_list = ""
        for name in names[::-1][:-1]:
            name1 = name["name"]
            date = datetime.utcfromtimestamp(
                int(str(name["changedToAt"])[:-3])
            ).strftime("%b %d, %Y")
            name_list += f"**{names.index(name)+1}.** `{name1}` - {date} " + "\n"
        original = names[0]["name"]
        name_list += f"**1.** `{original}` - First Username"

        uuids = "Short UUID: `" + uuid + "\n" + "`Long UUID: `" + long_uuid + "`"
        information = ""
        information += f"Username Changes: `{len(names)-1}`\n"

        embed = discord.Embed(title=f"Minecraft profile for {username}", color=0x00FF00)

        embed.add_field(name="UUID's", inline=False, value=uuids)
        embed.add_field(
            name="Textures",
            inline=True,
            value=f"Skin: [Open Skin](https://visage.surgeplay.com/bust/{uuid})",
        )
        embed.add_field(name="Information", inline=True, value=information)
        embed.add_field(name="Name History", inline=False, value=name_list)
        embed.set_thumbnail(url=(f"https://visage.surgeplay.com/bust/{uuid}"))

        await ctx.send(embed=embed)

    @staticmethod
    def get_server(ip: str, port: int) -> None:
        """Returns the server icon."""
        if ":" in ip:  # deal with them providing port in string instead of seperate
            ip, port = ip.split(":")
            return (ip, port)
        if port:
            return (ip, port)
        return (ip, None)

    @commands.command()
    @commands.cooldown(rate=1, per=5.0, type=commands.BucketType.user)
    async def server(
        self, ctx: commands.Context, server_ip: str, port: int = None
    ) -> None:
        """Get info on a minecraft server."""
        await ctx.channel.trigger_typing()
        url = f"{constants.Bot.api}/server/java"
        server_ip, _port = self.get_server(server_ip, port)
        if _port:
            port = _port
        if port:
            payload = {"server": server_ip, "port": port}
        else:
            payload = {"server": server_ip}

        if port:
            key = f"server_{server_ip}:ip"
        else:
            key = f"server_{server_ip}"
        if await self.bot.redis_session.exists(key):
            data = json.loads(await self.bot.redis_session.get(key))
        else:
            data = await get(ctx.bot.http_session, url, payload)
            self.bot.redis_session.set(key, json.dumps(data), expire=300)
        if not data:
            await ctx.send(
                (
                    f"{ctx.author}, :x: The Java edition Minecraft server `{server_ip}`"
                    " is currently not online or cannot be requested"
                )
            )
            return
        embed = discord.Embed(title=f"Java Server: {server_ip}", color=0x00FF00)
        embed.add_field(name="Description", value=data["description"])

        embed.add_field(
            name="Players",
            value=(
                f"Online: `{data['players']['online']:,}` \n "
                "Maximum: `{data['players']['max']:,}`"
            ),
        )
        if data["players"]["sample"]:
            names = ""
            for player in data["players"]["sample"]:
                names += f"{player['name']}\n"
            embed.add_field(name="Information", value=names, inline=False)
        embed.add_field(
            name="Version",
            value=(
                f"Java Edition \n Running: `{data['version']['name']}` \n "
                f"Protocol: `{data['version']['protocol']}`"
            ),
            inline=False,
        )
        if data["favicon"]:
            encoded = base64.decodebytes(data["favicon"][22:].encode("utf-8"))
            image_bytesio = io.BytesIO(encoded)
            favicon = discord.File(image_bytesio, "favicon.png")
            embed.set_thumbnail(url="attachment://favicon.png")
            await ctx.send(embed=embed, file=favicon)
        else:
            embed.set_thumbnail(
                url=(
                    "https://media.discordapp.net/attachments/493764139290984459"
                    "/602058959284863051/unknown.png"
                )
            )
            await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(rate=1, per=5.0, type=commands.BucketType.user)
    async def serverpe(
        self, ctx: commands.Context, server_ip: str, port: int = None
    ) -> None:
        """Get info on a minecraft PE server."""
        await ctx.channel.trigger_typing()
        url = f"{constants.Bot.api}/server/bedrock"
        server_ip, _port = self.get_server(server_ip, port)
        if _port:
            port = _port
        if port:
            payload = {"server": server_ip, "port": port}
        else:
            payload = {"server": server_ip}

        if port:
            key = f"bserver_{server_ip}:ip"
        else:
            key = f"bserver_{server_ip}"
        if await self.bot.redis_session.exists(key):
            data = json.loads(await self.bot.redis_session.get(key))
        else:
            data = await get(ctx.bot.http_session, url, payload)
            self.bot.redis_session.set(key, json.dumps(data), expire=300)
        if not data:
            await ctx.send(
                (
                    f"{ctx.author}, :x: The Bedrock edition Minecraft server "
                    "`{server_ip}` is currently not online or cannot be requested"
                )
            )
            return
        embed = discord.Embed(title=f"Bedrock Server: {server_ip}", color=0x00FF00)
        embed.add_field(name="Description", value=data["motd"])

        embed.add_field(
            name="Players",
            value=(
                f"Online: `{data['players']['online']:,}` \n Maximum: "
                f"`{data['players']['max']:,}`"
            ),
        )
        embed.add_field(
            name="Version",
            value=(
                f"Bedrock Edition \n Running: `{data['software']['version']}` "
                f"\n Map: `{data['map']}`"
            ),
            inline=True,
        )
        if data["players"]["names"]:
            names = ""
            for player in data["players"]["names"][:10]:
                names += f"{player}\n"
            embed.add_field(name="Players Online", value=names, inline=False)
        await ctx.send(embed=embed)

    @commands.command(aliases=["sales"])
    @commands.cooldown(rate=1, per=5.0, type=commands.BucketType.user)
    async def status(self, ctx: commands.Context) -> None:
        """Check the status of all the Mojang services."""
        await ctx.channel.trigger_typing()
        data = await get(ctx.bot.http_session, f"{constants.Bot.api}/mojang/check")
        sales_mapping = {
            "item_sold_minecraft": True,
            "prepaid_card_redeemed_minecraft": True,
            "item_sold_cobalt": False,
            "item_sold_scrolls": False,
        }
        payload = {"metricKeys": [k for (k, v) in sales_mapping.items() if v]}

        if await self.bot.redis_session.exists("status"):
            sales_data = json.loads(await self.bot.redis_session.get("status"))
        else:
            url = "https://api.mojang.com/orders/statistics"
            async with ctx.bot.http_session.post(url, json=payload) as resp:
                if resp.status == 200:
                    sales_data = await resp.json()
            await self.bot.redis_session.set("status", json.dumps(sales_data))

        services = ""
        for service in data:
            if data[service] == "green":
                services += (
                    f":green_heart: - {service}: **This service is healthy.** \n"
                )
            else:
                services += f":heart: - {service}: **This service is offline.** \n"
        embed = discord.Embed(title="Minecraft Service Status", color=0x00FF00)
        embed.add_field(
            name="Minecraft Game Sales",
            value=(
                f"Total Sales: **{sales_data['total']:,}** Last 24 Hours: "
                f"**{sales_data['last24h']:,}**"
            ),
        )
        embed.add_field(name="Minecraft Services:", value=services, inline=False)

        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(rate=1, per=1.0, type=commands.BucketType.user)
    async def mcbug(self, ctx: commands.Context, bug: str = None) -> None:
        """Gets info on a bug from bugs.mojang.com."""
        if not bug:
            await ctx.send(f"{ctx.message.author.mention},  :x: Please provide a bug.")
            return
        await ctx.channel.trigger_typing()
        data = await get(
            ctx.bot.http_session, f"https://bugs.mojang.com/rest/api/latest/issue/{bug}"
        )
        if not data:
            await ctx.send(
                f"{ctx.message.author.mention},  :x: The bug {bug} was not found."
            )
            return
        embed = discord.Embed(
            description=data["fields"]["description"],
            color=0x00FF00,
        )

        embed.set_author(
            name=f"{data['fields']['project']['name']} - {data['fields']['summary']}",
            url=f"https://bugs.mojang.com/browse/{bug}",
        )

        info = (
            f"Version: {data['fields']['project']['name']}\n"
            f"Reporter: {data['fields']['creator']['displayName']}\n"
            f"Created: {data['fields']['created']}\n"
            f"Votes: {data['fields']['votes']['votes']}\n"
            f"Updates: {data['fields']['updated']}\n"
            f"Watchers: {data['fields']['watches']['watchCount']}"
        )

        details = (
            f"Type: {data['fields']['issuetype']['name']}\n"
            f"Status: {data['fields']['status']['name']}\n"
        )
        if data["fields"]["resolution"]["name"]:
            details += f"Resolution: {data['fields']['resolution']['name']}\n"
        if "version" in data["fields"]:
            details += (
                "Affected: "
                f"{', '.join(s['name'] for s in data['fields']['versions'])}\n"
            )
        if "fixVersions" in data["fields"]:
            if len(data["fields"]["fixVersions"]) >= 1:
                details += (
                    f"Fixed Version: {data['fields']['fixVersions'][0]} + "
                    f"{len(data['fields']['fixVersions'])}\n"
                )

        embed.add_field(name="Information", value=info)
        embed.add_field(name="Details", value=details)

        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(rate=1, per=1.0, type=commands.BucketType.user)
    async def wiki(self, ctx: commands.Context, *, query: str) -> None:
        """Get an article from the minecraft wiki."""
        await ctx.channel.trigger_typing()

        def generate_payload(query: str) -> None:
            """Generate the payload for Gamepedia based on a query string."""
            payload = {
                "action": "query",
                "titles": query.replace(" ", "_"),
                "format": "json",
                "formatversion": "2",  # Cleaner json results
                "prop": "extracts",  # Include extract in returned results
                "exintro": "1",  # Only return summary paragraph(s) before main content
                "redirects": "1",  # Follow redirects
                "explaintext": "1",  # Make sure it's plaintext (not HTML)
            }
            return payload

        base_url = "https://minecraft.gamepedia.com/api.php"
        footer_icon = (
            "https://upload.wikimedia.org/wikipedia/commons/thumb/5/53"
            "/Wikimedia-logo.png/600px-Wikimedia-logo.png"
        )

        payload = generate_payload(query)

        result = await get(ctx.bot.http_session, base_url, payload)

        try:
            # Get the last page. Usually this is the only page.
            page = result["query"]["pages"][-1]
            title = page["title"]
            description = page["extract"].strip().replace("\n", "\n\n")
            url = f"https://minecraft.gamepedia.com/{title.replace(' ', '_')}"

            if len(description) > 1500:
                description = description[:1500].strip()
                description += f"... [(read more)]({url})"

            embed = discord.Embed(
                title=f"Minecraft Gamepedia: {title}",
                description=f"\u2063\n{description}\n\u2063",
                color=0x00FF00,
                url=url,
            )
            embed.set_footer(
                text="Information provided by Wikimedia", icon_url=footer_icon
            )
            await ctx.send(embed=embed)

        except KeyError:
            await ctx.send(f"I'm sorry, I couldn't find \"{query}\" on Gamepedia")

    # @commands.command()
    async def version(self, ctx: commands.Context) -> None:
        """Get version info."""
        await ctx.send("TODO")

    # @commands.command()
    async def colourcodes(self, ctx: commands.Context) -> None:
        """Get colourcodes info."""
        await ctx.send("TODO")

    # @commands.command()
    async def news(self, ctx: commands.Context) -> None:
        """Get recent news."""
        await ctx.send("TODO")
