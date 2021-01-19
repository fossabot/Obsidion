"""Core Commands."""
import datetime
import sys
import asyncio
import contextlib
import logging
import inspect
import os
from typing import List
import aiohttp


import discord
from obsidion import __version__
from .utils.chat_formatting import (
    humanize_timedelta,
    pagify,
    box,
)
from .utils.predicates import MessagePredicate
from obsidion.core.i18n import Translator, cog_i18n

from discord.ext import commands

log = logging.getLogger("obsidion")

_ = Translator("Dev", __file__)


@cog_i18n(_)
class Core(commands.Cog):
    """Commands related to core functions."""

    def __init__(self, bot):
        """Init Core Commands."""
        self.bot = bot

    @commands.command(hidden=True)
    async def ping(self, ctx: commands.Context):
        """Pong."""
        await ctx.send("Pong.")

    @commands.command()
    async def info(self, ctx: commands.Context):
        """Shows info about Obsidion."""
        author_repo = "https://github.com/Darkflame72"
        org_repo = "https://github.com/Obsidion-dev"
        obsidion_repo = org_repo + "/Obsidion"
        support_server_url = "https://discord.gg/rnAtymZnzH"
        dpy_repo = "https://github.com/Rapptz/discord.py"
        python_url = "https://www.python.org/"
        since = datetime.datetime(2020, 3, 23)
        days_since = (datetime.datetime.utcnow() - since).days

        app_info = await self.bot.application_info()
        if app_info.team:
            owner = app_info.team.name
        else:
            owner = app_info.owner

        dpy_version = "[{}]({})".format(discord.__version__, dpy_repo)
        python_version = "[{}.{}.{}]({})".format(*sys.version_info[:3], python_url)
        obsidion_version = "[{}]({})".format(__version__, obsidion_repo)

        about = _(
            "This bot is an instance of [Obsidion, an open source Discord bot]({}) "
            "created by [Darkflame72]({}) and [improved by many]({}).\n\n"
            "Obsidion is backed by a passionate community who contributes and "
            "creates content for everyone to enjoy. [Join us today]({}) "
            "and help us improve!\n\n"
            "(c) Obsidion-dev"
        ).format(obsidion_repo, author_repo, org_repo, support_server_url)

        embed = discord.Embed(color=self.bot.color)
        embed.add_field(name=("Instance owned by"), value=str(owner))
        embed.add_field(name="Python", value=python_version)
        embed.add_field(name="discord.py", value=dpy_version)
        embed.add_field(name=("Obsidion version"), value=obsidion_version)
        embed.add_field(name=("Docker hub image"), value=obsidion_version)
        embed.add_field(name=("About Obsidion"), value=about, inline=False)

        embed.set_footer(
            text=_("Bringing joy since 23rd March 2020 (over {} days ago!)").format(
                days_since
            )
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def uptime(self, ctx: commands.Context):
        """Shows Obsidion's uptime."""
        since = ctx.bot.uptime.strftime("%Y-%m-%d %H:%M:%S")
        delta = datetime.datetime.utcnow() - self.bot.uptime
        uptime_str = humanize_timedelta(timedelta=delta) or _("Less than one second")
        await ctx.send(
            _("Been up for: **{time_quantity}** (since {timestamp} UTC)").format(
                time_quantity=uptime_str, timestamp=since
            )
        )

    @commands.command()
    async def invite(self, ctx: commands.Context) -> None:
        """Invite the bot to your server."""
        embed = discord.Embed(
            description=_(
                "You can invite {name} to your Discord server by"
                " [clicking here]({invite})."
            ).format(name=self.bot.user.name, invite=self.bot._invite),
            color=self.bot.color,
        )

        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.is_owner()
    async def leave(self, ctx: commands.Context):
        """Leaves the current server."""
        await ctx.send(_("Are you sure you want me to leave this server? (y/n)"))

        pred = MessagePredicate.yes_or_no(ctx)
        try:
            await self.bot.wait_for("message", check=pred)
        except asyncio.TimeoutError:
            await ctx.send(_("Response timed out."))
            return
        else:
            if pred.result is True:
                await ctx.send(_("Alright. Bye :wave:"))
                log.debug(_("Leaving guild '{}'").format(ctx.guild.name))
                await ctx.guild.leave()
            else:
                await ctx.send(_("Alright, I'll stay then. :)"))

    @commands.command()
    @commands.is_owner()
    async def servers(self, ctx: commands.Context):
        """Lists and allows [botname] to leave servers."""
        guilds = sorted(list(self.bot.guilds), key=lambda s: s.name.lower())
        msg = ""
        responses = []
        for i, server in enumerate(guilds, 1):
            msg += "{}: {} (`{}`)\n".format(i, server.name, server.id)
            responses.append(str(i))

        for page in pagify(msg, ["\n"]):
            await ctx.send(page)

        query = await ctx.send(_("To leave a server, just type its number."))

        pred = MessagePredicate.contained_in(responses, ctx)
        try:
            await self.bot.wait_for("message", check=pred, timeout=15)
        except asyncio.TimeoutError:
            try:
                await query.delete()
            except discord.errors.NotFound:
                pass
        else:
            await self.leave_confirmation(guilds[pred.result], ctx)

    async def leave_confirmation(self, guild, ctx):
        if guild.owner.id == ctx.bot.user.id:
            await ctx.send(_("I cannot leave a guild I am the owner of."))
            return

        await ctx.send(
            _("Are you sure you want me to leave {}? (yes/no)").format(guild.name)
        )
        pred = MessagePredicate.yes_or_no(ctx)
        try:
            await self.bot.wait_for("message", check=pred, timeout=15)
            if pred.result is True:
                await guild.leave()
                if guild != ctx.guild:
                    await ctx.send(_("Done."))
            else:
                await ctx.send(_("Alright then."))
        except asyncio.TimeoutError:
            await ctx.send(_("Response timed out."))

    # Removing this command from forks is a violation of the AGPLv3 under which it is licensed.
    # Otherwise interfering with the ability for this command to be accessible is also a violation.
    @commands.command(name="licenseinfo", aliases=["license"])
    async def license_info_command(self, ctx: commands.Context):
        """
        Get info about Obsidion's licenses.
        """

        embed = discord.Embed(
            description=_(
                "This bot is an instance of the Obsidion Discord Bot.\n"
                "Obsidion is an open source application made available "
                "to the public and "
                "licensed under the GNU AGPL v3. The full text of this "
                "license is available to you at "
                "<https://github.com/Obsidion-dev/Obsidion/blob/master/LICENSE>"
            ),
            color=self.bot.color,
        )

        await ctx.send(embed=embed)

    @commands.command()
    async def source(self, ctx: commands.Context, *, command: str = None) -> None:
        """Displays my full source code or for a specific command.

        To display the source code of a subcommand you can separate it by
        periods, e.g. account.link for the link subcommand of the account command
        or by spaces.
        """  # noqa: DAR101, DAR201
        source_url = "https://github.com/Obsidion-dev/Obsidion"
        branch = "master"
        if command is None:
            return await ctx.send(source_url)

        if command == "help":
            src = type(self.bot.help_command)
            module = src.__module__
            filename = inspect.getsourcefile(src)
        else:
            obj = self.bot.get_command(command.replace(".", " "))
            if obj is None:
                return await ctx.send("Could not find command.")

            # since we found the command we're looking for, presumably anyway, let's
            # try to access the code itself
            src = obj.callback.__code__
            module = obj.callback.__module__
            filename = src.co_filename

        lines, firstlineno = inspect.getsourcelines(src)
        if not module.startswith("discord"):
            # not a built-in command
            location = os.path.relpath(filename).replace("\\", "/")
        else:
            location = module.replace(".", "/") + ".py"
            source_url = "https://github.com/Rapptz/discord.py"
            branch = "master"

        final_url = (
            f"<{source_url}/blob/{branch}/{location}#L{firstlineno}"
            f"-L{firstlineno + len(lines) - 1}>"
        )
        await ctx.send(final_url)

    @commands.command(name="shutdown")
    @commands.is_owner()
    async def _shutdown(self, ctx: commands.Context, silently: bool = False):
        """Shuts down the bot."""
        wave = "\N{WAVING HAND SIGN}"
        skin = "\N{EMOJI MODIFIER FITZPATRICK TYPE-3}"
        with contextlib.suppress(discord.HTTPException):
            if not silently:
                await ctx.send("Shutting down... " + wave + skin)
        await ctx.bot.shutdown()

    @commands.command(name="restart")
    @commands.is_owner()
    async def _restart(self, ctx: commands.Context, silently: bool = False):
        """Attempts to restart Obsidion.

        Makes [botname] quit with exit code 26.
        The restart is not guaranteed: it must be dealt
        with by the process manager in use."""
        with contextlib.suppress(discord.HTTPException):
            if not silently:
                await ctx.send("Restarting...")
        await ctx.bot.shutdown(restart=True)

    @commands.command()
    @commands.is_owner()
    async def traceback(self, ctx: commands.Context, public: bool = False):
        """Sends to the owner the last command exception that has occurred.

        If public (yes is specified), it will be sent to the chat instead."""
        if not public:
            destination = ctx.author
        else:
            destination = ctx.channel

        if self.bot._last_exception:
            for page in pagify(self.bot._last_exception, shorten_by=10):
                try:
                    await destination.send(box(page, lang="py"))
                except discord.HTTPException:
                    await ctx.channel.send(
                        _(
                            "I couldn't send the traceback message to you in DM. "
                            "Either you blocked me or you disabled DMs in this server."
                        )
                    )
                    return
        else:
            await ctx.send(_("No exception has occurred yet."))

    @commands.group(name="set")
    async def _set(self, ctx: commands.Context):
        """Changes Obsidion's settings."""

    @_set.command(aliases=["color"])
    @commands.is_owner()
    async def colour(self, ctx: commands.Context, *, colour: discord.Colour = None):
        """
        Sets a default colour to be used for the bot's embeds.

        Acceptable values for the colour parameter can be found at:

        https://discordpy.readthedocs.io/en/stable/ext/commands/api.html#discord.ext.commands.ColourConverter
        """
        if colour is None:
            ctx.bot._color = discord.Color.red()
            await ctx.bot._config.color.set(discord.Color.red().value)
            return await ctx.send(_("The color has been reset."))
        ctx.bot._color = colour
        await ctx.bot._config.color.set(colour.value)
        await ctx.send(_("The color has been set."))

    @_set.group(invoke_without_command=True)
    @commands.is_owner()
    async def avatar(self, ctx: commands.Context, url: str = None):
        """Sets [botname]'s avatar

        Supports either an attachment or an image URL."""
        if len(ctx.message.attachments) > 0:  # Attachments take priority
            data = await ctx.message.attachments[0].read()
        elif url is not None:
            if url.startswith("<") and url.endswith(">"):
                url = url[1:-1]

            async with aiohttp.ClientSession() as session:
                try:
                    async with session.get(url) as r:
                        data = await r.read()
                except aiohttp.InvalidURL:
                    return await ctx.send(_("That URL is invalid."))
                except aiohttp.ClientError:
                    return await ctx.send(
                        _("Something went wrong while trying to get the image.")
                    )
        else:
            await ctx.send_help()
            return

        try:
            async with ctx.typing():
                await ctx.bot.user.edit(avatar=data)
        except discord.HTTPException:
            await ctx.send(
                _(
                    "Failed. Remember that you can edit my avatar "
                    "up to two times a hour. The URL or attachment "
                    "must be a valid image in either JPG or PNG format."
                )
            )
        except discord.InvalidArgument:
            await ctx.send(_("JPG / PNG format only."))
        else:
            await ctx.send(_("Done."))

    @avatar.command(name="remove", aliases=["clear"])
    @commands.is_owner()
    async def avatar_remove(self, ctx: commands.Context):
        """Removes [botname]'s avatar."""
        async with ctx.typing():
            await ctx.bot.user.edit(avatar=None)
        await ctx.send(_("Avatar removed."))

    @_set.command(name="playing", aliases=["game"])
    @commands.guild_only()
    @commands.is_owner()
    async def _game(self, ctx: commands.Context, *, game: str = None):
        """Sets [botname]'s playing status."""

        if game:
            if len(game) > 128:
                await ctx.send(
                    "The maximum length of game descriptions is 128 characters."
                )
                return
            game = discord.Game(name=game)
        else:
            game = None
        status = (
            ctx.bot.guilds[0].me.status
            if len(ctx.bot.guilds) > 0
            else discord.Status.online
        )
        await ctx.bot.change_presence(status=status, activity=game)
        if game:
            await ctx.send(
                _("Status set to ``Playing {game.name}``.").format(game=game)
            )
        else:
            await ctx.send(_("Game cleared."))

    @_set.command(name="listening")
    @commands.guild_only()
    @commands.is_owner()
    async def _listening(self, ctx: commands.Context, *, listening: str = None):
        """Sets [botname]'s listening status."""

        status = (
            ctx.bot.guilds[0].me.status
            if len(ctx.bot.guilds) > 0
            else discord.Status.online
        )
        if listening:
            activity = discord.Activity(
                name=listening, type=discord.ActivityType.listening
            )
        else:
            activity = None
        await ctx.bot.change_presence(status=status, activity=activity)
        if activity:
            await ctx.send(
                _("Status set to ``Listening to {listening}``.").format(
                    listening=listening
                )
            )
        else:
            await ctx.send(_("Listening cleared."))

    @_set.command(name="watching")
    @commands.guild_only()
    @commands.is_owner()
    async def _watching(self, ctx: commands.Context, *, watching: str = None):
        """Sets [botname]'s watching status."""

        status = (
            ctx.bot.guilds[0].me.status
            if len(ctx.bot.guilds) > 0
            else discord.Status.online
        )
        if watching:
            activity = discord.Activity(
                name=watching, type=discord.ActivityType.watching
            )
        else:
            activity = None
        await ctx.bot.change_presence(status=status, activity=activity)
        if activity:
            await ctx.send(
                _("Status set to ``Watching {watching}``.").format(watching=watching)
            )
        else:
            await ctx.send(_("Watching cleared."))

    @_set.command(name="competing")
    @commands.guild_only()
    @commands.is_owner()
    async def _competing(self, ctx: commands.Context, *, competing: str = None):
        """Sets [botname]'s competing status."""

        status = (
            ctx.bot.guilds[0].me.status
            if len(ctx.bot.guilds) > 0
            else discord.Status.online
        )
        if competing:
            activity = discord.Activity(
                name=competing, type=discord.ActivityType.competing
            )
        else:
            activity = None
        await ctx.bot.change_presence(status=status, activity=activity)
        if activity:
            await ctx.send(
                _("Status set to ``Competing in {competing}``.").format(
                    competing=competing
                )
            )
        else:
            await ctx.send(_("Competing cleared."))

    @_set.command()
    @commands.guild_only()
    @commands.is_owner()
    async def status(self, ctx: commands.Context, *, status: str):
        """Sets [botname]'s status.

        Available statuses:
            online
            idle
            dnd
            invisible
        """

        statuses = {
            "online": discord.Status.online,
            "idle": discord.Status.idle,
            "dnd": discord.Status.dnd,
            "invisible": discord.Status.invisible,
        }

        game = ctx.bot.guilds[0].me.activity if len(ctx.bot.guilds) > 0 else None
        try:
            status = statuses[status.lower()]
        except KeyError:
            await ctx.send_help()
        else:
            await ctx.bot.change_presence(status=status, activity=game)
            await ctx.send(_("Status changed to {}.").format(status))

    @_set.command(
        name="streaming", aliases=["stream"], usage="[(<streamer> <stream_title>)]"
    )
    @commands.guild_only()
    @commands.is_owner()
    async def stream(self, ctx: commands.Context, streamer=None, *, stream_title=None):
        """Sets [botname]'s streaming status.

        Leaving both streamer and stream_title empty will clear it."""

        status = ctx.bot.guilds[0].me.status if len(ctx.bot.guilds) > 0 else None

        if stream_title:
            stream_title = stream_title.strip()
            if "twitch.tv/" not in streamer:
                streamer = "https://www.twitch.tv/" + streamer
            activity = discord.Streaming(url=streamer, name=stream_title)
            await ctx.bot.change_presence(status=status, activity=activity)
        elif streamer is not None:
            await ctx.send_help()
            return
        else:
            await ctx.bot.change_presence(activity=None, status=status)
        await ctx.send(_("Done."))

    @_set.command(name="nickname")
    @commands.has_guild_permissions(manage_nicknames=True)
    @commands.guild_only()
    async def _nickname(self, ctx: commands.Context, *, nickname: str = None):
        """Sets Obsidion's nickname."""
        try:
            if nickname and len(nickname) > 32:
                await ctx.send(
                    _("Failed to change nickname. Must be 32 characters or fewer.")
                )
                return
            await ctx.guild.me.edit(nick=nickname)
        except discord.Forbidden:
            await ctx.send(_("I lack the permissions to change my own nickname."))
        else:
            await ctx.send(_("Done."))

    @_set.command(aliases=["gprefixes"], require_var_positional=True)
    @commands.is_owner()
    async def globalprefix(self, ctx: commands.Context, *prefixes: str):
        """Sets Obsidion's global prefix(es)."""
        await ctx.bot.set_prefixes(guild=None, prefixes=prefixes)
        await ctx.send(_("Prefix set."))

    @_set.command(aliases=["serverprefixes"])
    @commands.bot_has_guild_permissions(manage_guild=True)
    @commands.guild_only()
    async def prefix(self, ctx: commands.Context, *prefixes: str):
        """Sets Obsidion's server prefix(es)."""
        if not prefixes:
            await ctx.bot.set_prefixes(guild=ctx.guild, prefixes=[])
            await ctx.send(_("Guild prefixes have been reset."))
            return
        prefixes = sorted(prefixes, reverse=True)
        await ctx.bot.set_prefixes(guild=ctx.guild, prefixes=prefixes)
        await ctx.send(_("Prefix set."))

    # @_set.command()
    # @commands.guild_only()
    # @checks.guildowner_or_permissions(manage_guild=True)
    # async def locale(self, ctx: commands.Context, language_code: str):
    #     """
    #     Changes the bot's locale in this server.

    #     `<language_code>` can be any language code with country code included,
    #     e.g. `en-US`, `de-DE`, `fr-FR`, `pl-PL`, etc.

    #     Go to Red's Crowdin page to see locales that are available with translations:
    #     https://translate.discord.red

    #     Use "default" to return to the bot's default set language.
    #     To reset to English, use "en-US".
    #     """
    #     if language_code.lower() == "default":
    #         global_locale = await self.bot._config.locale()
    #         i18n.set_contextual_locale(global_locale)
    #         await self.bot._i18n_cache.set_locale(ctx.guild, None)
    #         await ctx.send(_("Locale has been set to the default."))
    #         return
    #     try:
    #         locale = BabelLocale.parse(language_code, sep="-")
    #     except (ValueError, UnknownLocaleError):
    #         await ctx.send(_("Invalid language code. Use format: `en-US`"))
    #         return
    #     if locale.territory is None:
    #         await ctx.send(
    #             _(
    #                 "Invalid format - language code has to include country code, e.g. `en-US`"
    #             )
    #         )
    #         return
    #     standardized_locale_name = f"{locale.language}-{locale.territory}"
    #     i18n.set_contextual_locale(standardized_locale_name)
    #     await self.bot._i18n_cache.set_locale(ctx.guild, standardized_locale_name)
    #     await ctx.send(_("Locale has been set."))

    # @_set.command(aliases=["region"])
    # @checks.guildowner_or_permissions(manage_guild=True)
    # async def regionalformat(self, ctx: commands.Context, language_code: str = None):
    #     """
    #     Changes bot's regional format in this server. This is used for formatting date, time and numbers.

    #     `<language_code>` can be any language code with country code included,
    #     e.g. `en-US`, `de-DE`, `fr-FR`, `pl-PL`, etc.

    #     Leave `<language_code>` empty to base regional formatting on bot's locale in this server.
    #     """
    #     if language_code is None:
    #         i18n.set_contextual_regional_format(None)
    #         await self.bot._i18n_cache.set_regional_format(ctx.guild, None)
    #         await ctx.send(
    #             _(
    #                 "Regional formatting will now be based on bot's locale in this server."
    #             )
    #         )
    #         return

    #     try:
    #         locale = BabelLocale.parse(language_code, sep="-")
    #     except (ValueError, UnknownLocaleError):
    #         await ctx.send(_("Invalid language code. Use format: `en-US`"))
    #         return
    #     if locale.territory is None:
    #         await ctx.send(
    #             _(
    #                 "Invalid format - language code has to include country code, e.g. `en-US`"
    #             )
    #         )
    #         return
    #     standardized_locale_name = f"{locale.language}-{locale.territory}"
    #     i18n.set_contextual_regional_format(standardized_locale_name)
    #     await self.bot._i18n_cache.set_regional_format(
    #         ctx.guild, standardized_locale_name
    #     )
    #     await ctx.send(
    #         _(
    #             "Regional formatting will now be based on `{language_code}` locale."
    #         ).format(language_code=standardized_locale_name)
    #     )

    @commands.command()
    @commands.is_owner()
    async def dm(self, ctx: commands.Context, user_id: int, *, message: str):
        """Sends a DM to a user.

        This command needs a user ID to work.
        To get a user ID, go to Discord's settings and open the
        'Appearance' tab. Enable 'Developer Mode', then right click
        a user and click on 'Copy ID'.
        """
        destination = self.bot.get_user(user_id)
        if destination is None or destination.bot:
            await ctx.send(
                _(
                    "Invalid ID, user not found, or user is a bot. "
                    "You can only send messages to people I share "
                    "a server with."
                )
            )
            return

        prefixes = await ctx.bot.get_valid_prefixes()
        prefix = re.sub(
            rf"<@!?{ctx.me.id}>", f"@{ctx.me.name}".replace("\\", r"\\"), prefixes[0]
        )
        description = _("Owner of {}").format(ctx.bot.user)
        content = _("You can reply to this message with {}contact").format(prefix)
        if await ctx.embed_requested():
            e = discord.Embed(colour=discord.Colour.red(), description=message)

            e.set_footer(text=content)
            if ctx.bot.user.avatar_url:
                e.set_author(name=description, icon_url=ctx.bot.user.avatar_url)
            else:
                e.set_author(name=description)

            try:
                await destination.send(embed=e)
            except discord.HTTPException:
                await ctx.send(
                    _("Sorry, I couldn't deliver your message to {}").format(
                        destination
                    )
                )
            else:
                await ctx.send(_("Message delivered to {}").format(destination))
        else:
            response = "{}\nMessage:\n\n{}".format(description, message)
            try:
                await destination.send("{}\n{}".format(box(response), content))
            except discord.HTTPException:
                await ctx.send(
                    _("Sorry, I couldn't deliver your message to {}").format(
                        destination
                    )
                )
            else:
                await ctx.send(_("Message delivered to {}").format(destination))