from discord.ext import commands
from random import choice
import discord
import resource
import aiohttp
import datetime, time

class Miscellaneous(commands.Cog, name="Miscellaneous"):
    def __init__(self, bot):
        self.bot = bot
        self.session = bot.session

    @commands.command()
    async def invite(self, ctx):
        """Provied the link to invite the bot to your server"""
        embed = discord.Embed(
            description=f"**[Click here to add {self.bot.user.name} to your Discord server](https://discordapp.com/oauth2/authorize?client_id=691589447074054224&scope=bot)**", color=0x00ff00)
        await ctx.send(embed=embed)

    @commands.command()
    async def ping(self, ctx):
        """Check ping of client, message and api"""
        latency = round(self.bot.latency * 1000)
        embed = discord.Embed(title="Bot's Ping", color=0x00ff00)
        embed.add_field(name="API Ping", value=f"`{latency}ms`")

        await ctx.send(embed=embed)

    @commands.command()
    async def stats(self, ctx):
        """View statistics about the bot"""

        current_time = time.time()
        difference = int(round(current_time - self.bot.start_time))
        text = str(datetime.timedelta(seconds=difference))

        total_users = sum(len(guild.members) for guild in self.bot.guilds)
        text_channels = sum(len(guild.text_channels)
                            for guild in self.bot.guilds)
        voice_channels = sum(len(guild.voice_channels)
                             for guild in self.bot.guilds)

        ram = round(resource.getrusage(
            resource.RUSAGE_SELF).ru_maxrss / (2**20), 2)

        statics = ""
        statics += f"Guilds: `{len(self.bot.guilds):,}`\n"
        statics += f"Users: `{total_users:,}`\n"
        statics += f"Channels: `{text_channels+voice_channels:,}`\n"
        statics += f"Memory Usage: `{ram:,}MB`\n"
        statics += f"Uptime: `{text}`\n"
        statics += f"Discord.py: `v{discord.__version__}`"

        links = ""
        links += "[INVITE BOT](https://discordapp.com/oauth2/authorize?client_id=691589447074054224&scope=bot)\n"
        links += "[GITHUB](https://github.com/Darkflame72/Minecraft-Discord)\n"
        links += "[SUPPORT SERVER](https://discord.gg/invite/7BRD7s6)\n"

        embed = discord.Embed(title="Stats", color=0x00ff00)
        embed.add_field(name=":newspaper: STATS", value=statics, inline=True)
        embed.add_field(name=":link: LINKS", value=links, inline=True)

        await ctx.send(embed=embed)

    @commands.command(hidden=True)
    async def help(self, ctx, *cog_name):
        """Gets all cogs and commands of mine."""
        if cog_name:
            if len(cog_name) > 1:
                await ctx.send(f"{ctx.message.author.mention}, :x: Please enter only one command for help")
            else:
                # get information on 1 cog
                cog_name = cog_name[0]
                found = False
                for x in self.bot.cogs:
                    for y in self.bot.get_cog(x).get_commands():
                        if y.name == cog_name:
                            embed = discord.Embed(
                                title=cog_name, description=y.help, color=0x00ff00)
                            await ctx.message.add_reaction("\N{WHITE HEAVY CHECK MARK}")
                            await ctx.author.send(embed=embed)
                            found = True
                            break
                if not found:
                    await ctx.send(f"{ctx.message.author.mention}, :x: That command is not found please try again")
        else:
            if ctx.guild is None:
                prefix = "/"
            else:
                prefix = self.bot.pool["guilds"][str(ctx.guild.id)]["prefix"]
            embed = discord.Embed(
                description=f"Below is a list of commands you can use\n To use commands type `{prefix}command` or <@{self.bot.user.id}> command \n To get more information about a command type: `{prefix}help command`", color=0x00ff00)
            embed.set_author(name="Bot's Commands")
            # General help command
            for cog in self.bot.cogs:
                cogs = []
                cog_commands = self.bot.get_cog(cog).get_commands()
                for c in cog_commands:
                    if not c.hidden:
                        cogs.append(c.name)
                if len(cogs) > 0:
                    embed.add_field(
                        name=cog, value=f"`{'`, `'.join(cogs)}`", inline=False)
            embed.set_footer(text="Version: 0.1 | Authors: Darkflame72#1150")
            await ctx.send(embed=embed)

    @commands.command(aliases=["alias", "a"])
    async def aliases(self, ctx):
        """Lists all the aliases you can use."""
        if ctx.guild is None:
            prefix = "/"
        else:
            prefix = self.bot.pool["guilds"][str(ctx.guild.id)]["prefix"]
        embed = discord.Embed(
            description=f"Below is a list of command aliases you can use\n To use aliases type `{prefix}alias` or <@{self.bot.user.id}> alias \n To get more information about a command type: `{prefix}help command`", color=0x00ff00)
        embed.set_author(name="Bot's Commands")
        # General help command
        for cog in self.bot.cogs:
            cogs = []
            cog_commands = self.bot.get_cog(cog).get_commands()
            for c in cog_commands:
                if not c.hidden and len(c.aliases) >= 1:
                    cogs.append(f"**{c.name}**: `{', '.join(c.aliases)}`\n")
            if len(cogs) >= 1:
                embed.add_field(
                    name=cog, value=f"{''.join(cogs)}", inline=False)
        embed.set_footer(text="Version: 0.1 | Authors: Darkflame72#1150")
        await ctx.send(embed=embed)

    @commands.command()
    async def credits(self, ctx):
        embed = discord.Embed(
            title=f"{self.bot.user.name} Bot Credits", color=0x00ff00)
        embed.add_field(
            name="Developers", value="[Darkflame72#1150](https://github.com/Darkflame72/)")
        #embed.add_field(name="Staff", value="")
        embed.add_field(
            name="Beta Testers", value="[Abhishek Rameshand#8069](https://www.youtube.com/channel/UC0L0CPqIoZzKeV7ndIXjZZw), [Arrow_Plays#8625](https://github.com/AjayACST/)")
        embed.add_field(
            name="Contribute", value="[Contribute on Github](https://github.com/Darkflame72/Osisdion/)")
        third_party = ""
        third_party += "This bot uses some external services to add extra features.\n"
        third_party += "Skin renders - [Visage](https://visage.surgeplay.com/index.html)\n"
        third_party += "Mojang API - [Wiki.vg](https://wiki.vg/Mojang_API)\n"
        third_party += "Discord.py - [discord.py Github](https://github.com/Rapptz/discord.py)"
        embed.add_field(name="Third Party Stuff",
                        value=third_party, inline=False)

        embed.set_footer(text="Version: 0.1 | Authors: Darkflame72#1150")
        await ctx.send(embed=embed)

    @commands.command()
    async def wiki(self, ctx, *, query):
        """Get an article from the minecraft wiki"""
        async with ctx.channel.typing():
            base_url = "https://minecraft.gamepedia.com/api.php"
            footer_icon = (
                "https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Wikimedia-logo.png"
                "/600px-Wikimedia-logo.png"
            )

            payload = generate_payload(query)

            async with self.session.get(base_url, params=payload) as resp:
                result = await resp.json()

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
                    description=u"\u2063\n{}\n\u2063".format(description),
                    color=0x00ff00,
                    url=url,
                )
                embed.set_footer(
                    text="Information provided by Wikimedia", icon_url=footer_icon
                )
                await ctx.send(embed=embed)

            except KeyError:
                await ctx.send(f"I'm sorry, I couldn't find \"{query}\" on Gamepedia")
    # @commands.command()
    # async def aliases(self, ctx, command_name=None):
    #    pass

    # @commands.command()
    # async def credits(self, ctx):
    #    pass

    # @commands.command()
    # async def tutorial(self, ctx):
    #    pass


def generate_payload(query):
    """Generate the payload for Gamepedia based on a query string."""
    payload = {}
    payload["action"] = "query"
    payload["titles"] = query.replace(" ", "_")
    payload["format"] = "json"
    payload["formatversion"] = "2"  # Cleaner json results
    payload["prop"] = "extracts"  # Include extract in returned results
    # Only return summary paragraph(s) before main content
    payload["exintro"] = "1"
    payload["redirects"] = "1"  # Follow redirects
    payload["explaintext"] = "1"  # Make sure it's plaintext (not HTML)
    return payload
