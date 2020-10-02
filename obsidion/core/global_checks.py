"""Checks to run on every command."""

from discord.ext.commands import Context


def init_global_checks(bot) -> None:
    """Global checks to run."""

    @bot.check_once
    def minimum_bot_perms(ctx: Context) -> bool:
        """Too many 403, 401, and 429 Errors can cause bots to get global'd.

        Args:
            ctx (Context): Message context

        Returns:
            bool: wether has perms
        """
        return ctx.channel.permissions_for(ctx.me).send_messages

    @bot.check_once
    def bots(ctx: Context) -> bool:
        """Check the user is not a bot.

        Args:
            ctx (Context): Message context

        Returns:
            bool: wether the author is a bot
        """
        return not ctx.author.bot
