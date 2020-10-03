"""Error handling."""

import logging
import traceback

import discord
from discord.ext.commands import Cog, Context, errors

from obsidion import constants
from obsidion.bot import Obsidion
from ..utils.chat_formatting import text_to_file

log = logging.getLogger(__name__)

# a lot of this is from Pythondiscord community
# discord bot. It can be found here
# https://github.com/python-discord/bot/blob/master/bot/cogs/error_handler.py


class ErrorHandler(Cog):
    """Handles errors emitted from commands."""

    def __init__(self, bot: Obsidion) -> None:
        """Init."""
        self.bot = bot

    @Cog.listener()
    async def on_command_error(self, ctx: Context, e: errors.CommandError) -> None:
        """Error handling for the bot."""
        command = ctx.command

        if hasattr(e, "handled"):
            return

        if isinstance(e, errors.CommandNotFound) and not hasattr(
            ctx, "invoked_from_error_handler"
        ):
            # not deal with command not found
            pass
        elif isinstance(e, errors.UserInputError):
            await self.handle_user_input_error(ctx, e)
        elif isinstance(e, errors.CheckFailure):
            await self.handle_check_failure(ctx, e)
        elif isinstance(e, errors.CommandOnCooldown):
            await ctx.send(
                f"This command is on cooldown, please retry in {e.retry_after:.2f}s"
            )
        elif isinstance(e, errors.CommandInvokeError):
            await self.handle_unexpected_error(ctx, e.original)
        elif not isinstance(e, errors.DisabledCommand):
            # ConversionError, MaxConcurrencyReached, ExtensionError
            await self.handle_unexpected_error(ctx, e)

        log.debug(
            f"Command {command} invoked by {ctx.message.author} with error "
            f"{e.__class__.__name__}: {e}"
        )

    @staticmethod
    def get_help_command(ctx: Context) -> None:
        """Return a prepared `help` command invocation coroutine."""
        if ctx.command:
            return ctx.send_help(ctx.command)

        return ctx.send_help()

    async def handle_user_input_error(
        self, ctx: Context, e: errors.UserInputError
    ) -> None:
        """Send an error message in `ctx` for UserInputError."""
        prepared_help_command = self.get_help_command(ctx)

        if isinstance(e, errors.MissingRequiredArgument):
            await ctx.send(f"Missing required argument `{e.param.name}`.")
            await prepared_help_command  # pytype: disable=bad-return-type
        elif isinstance(e, errors.TooManyArguments):
            # handle this by running the command and ignoring extra input
            # await ctx.send("Too many arguments provided.")
            await prepared_help_command  # pytype: disable=bad-return-type
        elif isinstance(e, errors.BadArgument):
            await ctx.send(f"Bad argument: {e}\n")
            await prepared_help_command  # pytype: disable=bad-return-type
        elif isinstance(e, errors.BadUnionArgument):
            await ctx.send(f"Bad argument: {e}\n```{e.errors[-1]}```")
        elif isinstance(e, errors.ArgumentParsingError):
            await ctx.send(f"Argument parsing error: {e}")
        else:
            await ctx.send("Something about your input seems off. Check the arguments:")
            await prepared_help_command  # pytype: disable=bad-return-type

    @staticmethod
    async def handle_check_failure(ctx: Context, e: errors.CheckFailure) -> None:
        """Send an error message in `ctx` for certain types of CheckFailure.

        Args:
            ctx (Context): Context of message
            e (errors.CheckFailure): [description]error type

        The following types are handled:
        * BotMissingPermissions
        * BotMissingRole
        * BotMissingAnyRole
        * NoPrivateMessage
        * InWhitelistCheckFailure
        """
        bot_missing_errors = (
            errors.BotMissingPermissions,
            errors.BotMissingRole,
            errors.BotMissingAnyRole,
        )

        if isinstance(e, bot_missing_errors):
            missing = [
                perm.replace("_", " ").replace("guild", "server").title()
                for perm in e.missing_perms
            ]
            if len(missing) > 2:
                fmt = f"{'**, **'.join(missing[:-1])}, and {missing[-1]}"
            else:
                fmt = " and ".join(missing)
            await ctx.send(
                (
                    f"Sorry, it looks like I don't have the **{fmt}**permission(s) "
                    "I need to do that."
                )
            )

    @staticmethod
    async def handle_unexpected_error(ctx: Context, e: errors.CommandError) -> None:
        """Send a generic error message in `ctx` and log the exception."""
        await ctx.send(
            (
                "Sorry, an unexpected error occurred. It has been "
                "recorded and should be fixed soon!\n\n"
            )
        )
        log.error(
            (
                f"Error executing command invoked by {ctx.message.author}: ",
                f"{ctx.message.content}",
            ),
            exc_info=e,
        )
        embed = discord.Embed(title="Bug", colour=0x00FF00)
        channel = ctx.bot.get_channel(constants.Channels.stack_trace_channel)

        embed.set_author(name=str(ctx.author), icon_url=ctx.author.avatar_url)
        embed.add_field(name="Command", value=ctx.command)
        if len(f"```{(''.join(traceback.format_tb(e.__traceback__)))}\n{e}```") <= 900:
            embed.add_field(
                name="Traceback",
                value=f"```{(''.join(traceback.format_tb(e.__traceback__)))}\n{e}```",
                inline=False,
            )
            file = None
        else:
            embed.add_field(name="Traceback", value=e, inline=False)
            file = text_to_file(
                f"{''.join(traceback.format_tb(e.__traceback__))}\n{e}", "error.txt"
            )

        embed.timestamp = ctx.message.created_at

        if ctx.guild is not None:
            embed.add_field(
                name="Server",
                value=f"{ctx.guild.name} (ID: {ctx.guild.id})",
                inline=False,
            )

        embed.add_field(
            name="Channel", value=f"{ctx.channel} (ID: {ctx.channel.id})", inline=False
        )
        embed.set_footer(text=f"Author ID: {ctx.author.id}")

        await channel.send(embed=embed)
        if file:
            await channel.send(file=file)


def setup(bot: Obsidion) -> None:
    """Load the ErrorHandler cog."""
    bot.add_cog(ErrorHandler(bot))
