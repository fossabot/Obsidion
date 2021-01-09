import logging
from datetime import datetime
import traceback

from discord.ext import commands

from .utils.chat_formatting import humanize_timedelta, inline, format_perms_list


log = logging.getLogger("obsidion")


class Events(commands.Cog):
    """Important bot events."""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener("on_connect")
    async def on_connect(self):
        if self.bot.uptime is None:
            log.info("Connected to Discord. Getting ready...")

    @commands.Cog.listener("on_ready")
    async def on_ready(self):
        if self.bot.uptime is not None:
            return

        self.bot.uptime = datetime.utcnow()

    @commands.Cog.listener("on_command_error")
    async def on_command_error(self, ctx, error, unhandled_by_cog=False):

        if not unhandled_by_cog:
            if hasattr(ctx.command, "on_error"):
                return

            if ctx.cog:
                if (
                    commands.Cog._get_overridden_method(ctx.cog.cog_command_error)
                    is not None
                ):
                    return

        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send_help(ctx.command)
        elif isinstance(error, commands.ArgumentParsingError):
            msg = "`{user_input}` is not a valid value for `{command}`".format(
                user_input=error.user_input, command=error.cmd
            )
            if error.custom_help_msg:
                msg += f"\n{error.custom_help_msg}"
            await ctx.send(msg)
            if error.send_cmd_help:
                await ctx.send_help(ctx.command)
        elif isinstance(error, commands.ConversionError):
            if error.args:
                await ctx.send(error.args[0])
            else:
                await ctx.send_help(ctx.command)
        elif isinstance(error, commands.UserInputError):
            await ctx.send_help(ctx.command)
        elif isinstance(error, commands.CommandInvokeError):
            log.exception(
                "Exception in command '{}'".format(ctx.command.qualified_name),
                exc_info=error.original,
            )

            message = (
                "Error in command '{command}'. It has been recorded and should be fixed soon."
            ).format(command=ctx.command.qualified_name)
            exception_log = "Exception in command '{}'\n" "".format(
                ctx.command.qualified_name
            )
            exception_log += "".join(
                traceback.format_exception(type(error), error, error.__traceback__)
            )
            self.bot._last_exception = exception_log
            await ctx.send(inline(message))
        # elif isinstance(error, commands.CommandNotFound):
        #     help_settings = await HelpSettings.from_context(ctx)
        #     fuzzy_commands = await fuzzy_command_search(
        #         ctx,
        #         commands=RedHelpFormatter.help_filter_func(
        #             ctx, self.bot.walk_commands(), help_settings=help_settings
        #         ),
        #     )
        #     if not fuzzy_commands:
        #         pass
        #     elif await ctx.embed_requested():
        #         await ctx.send(
        #             embed=await format_fuzzy_results(ctx, fuzzy_commands, embed=True)
        #         )
        #     else:
        #         await ctx.send(
        #             await format_fuzzy_results(ctx, fuzzy_commands, embed=False)
        #         )
        elif isinstance(error, commands.BotMissingPermissions):
            if bin(error.missing.value).count("1") == 1:  # Only one perm missing
                msg = (
                    "I require the {permission} permission to execute that command."
                ).format(permission=format_perms_list(error.missing))
            else:
                msg = (
                    "I require {permission_list} permissions to execute that command."
                ).format(permission_list=format_perms_list(error.missing))
            await ctx.send(msg)
        elif isinstance(error, commands.UserFeedbackCheckFailure):
            if error.message:
                await ctx.send(error.message)
        elif isinstance(error, commands.NoPrivateMessage):
            await ctx.send(("That command is not available in DMs."))
        elif isinstance(error, commands.PrivateMessageOnly):
            await ctx.send(("That command is only available in DMs."))
        elif isinstance(error, commands.CheckFailure):
            pass
        elif isinstance(error, commands.CommandOnCooldown):
            if self.bot._bypass_cooldowns and ctx.author.id in self.bot.owner_ids:
                ctx.command.reset_cooldown(ctx)
                new_ctx = await self.bot.get_context(ctx.message)
                await self.bot.invoke(new_ctx)
                return
            if delay := humanize_timedelta(seconds=error.retry_after):
                msg = ("This command is on cooldown. Try again in {delay}.").format(
                    delay=delay
                )
            else:
                msg = "This command is on cooldown. Try again in 1 second."
            await ctx.send(msg, delete_after=error.retry_after)
        elif isinstance(error, commands.MaxConcurrencyReached):
            if error.per is commands.BucketType.default:
                if error.number > 1:
                    msg = (
                        "Too many people using this command."
                        " It can only be used {number} times concurrently."
                    ).format(number=error.number)
                else:
                    msg = (
                        "Too many people using this command."
                        " It can only be used once concurrently."
                    )
            elif error.per in (commands.BucketType.user, commands.BucketType.member):
                if error.number > 1:
                    msg = (
                        "That command is still completing,"
                        " it can only be used {number} times per {type} concurrently."
                    ).format(number=error.number, type=error.per.name)
                else:
                    msg = (
                        "That command is still completing,"
                        " it can only be used once per {type} concurrently."
                    ).format(type=error.per.name)
            else:
                if error.number > 1:
                    msg = (
                        "Too many people using this command."
                        " It can only be used {number} times per {type} concurrently."
                    ).format(number=error.number, type=error.per.name)
                else:
                    msg = (
                        "Too many people using this command."
                        " It can only be used once per {type} concurrently."
                    ).format(type=error.per.name)
            await ctx.send(msg)
        else:
            log.exception(type(error).__name__, exc_info=error)
