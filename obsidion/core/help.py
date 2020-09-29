import logging

import discord
from discord.ext import commands
from discord.ext.commands import Command
from obsidion import constants
from obsidion.bot import Obsidion
from fuzzywuzzy import fuzz, process

log = logging.getLogger(__name__)


class HelpQueryNotFound(ValueError):
    """
    Raised when a HelpSession Query doesn't match a command or cog.
    Contains the custom attribute of ``possible_matches``.
    Instances of this object contain a dictionary of any command(s) that were close to matching the
    query, where keys are the possible matched command names and values are the likeness match scores.
    """

    def __init__(self, arg: str, possible_matches: dict = None):
        super().__init__(arg)
        self.possible_matches = possible_matches


class MyHelpCommand(commands.HelpCommand):
    def __init__(self):
        super().__init__(
            command_attrs={
                "help": "Shows help about the bot, a command, or a category",
                "hidden": True,
            }
        )

    async def get_all_help_choices(self) -> set:
        """
        Get all the possible options for getting help in the bot.
        This will only display commands the author has permission to run.
        These include:
        - Category names
        - Cog names
        - Group command names (and aliases)
        - Command names (and aliases)
        - Subcommand names (with parent group and aliases for subcommand, but not including aliases for group)
        Options and choices are case sensitive.
        """
        # first get all commands including subcommands and full command name aliases
        choices = set()
        for command in await self.filter_commands(self.context.bot.walk_commands()):
            # the the command or group name
            choices.add(str(command))

            if isinstance(command, Command):
                # all aliases if it's just a command
                choices.update(command.aliases)
            else:
                # otherwise we need to add the parent name in
                choices.update(
                    f"{command.full_parent_name} {alias}" for alias in command.aliases
                )

        # all cog names
        choices.update(self.context.bot.cogs)

        # all category names
        choices.update(
            cog.category
            for cog in self.context.bot.cogs.values()
            if hasattr(cog, "category")
        )
        return choices

    async def subcommand_not_found(
        self, command: Command, string: str
    ) -> "HelpQueryNotFound":
        """
        Redirects the error to `command_not_found`.
        `command_not_found` deals with searching and getting best choices for both commands and subcommands.
        """
        return await self.command_not_found(f"{command.qualified_name} {string}")

    async def send_error_message(self, error: HelpQueryNotFound) -> None:
        """Send the error message to the channel."""
        embed = discord.Embed(colour=discord.Colour.red(), title=str(error))

        if getattr(error, "possible_matches", None):
            matches = "\n".join(f"`{match}`" for match in error.possible_matches)
            embed.description = f"**Did you mean:**\n{matches}"

            await self.context.send(embed=embed)

    async def command_not_found(self, string: str) -> "HelpQueryNotFound":
        """
        Handles when a query does not match a valid command, group, cog or category.
        Will return an instance of the `HelpQueryNotFound` exception with the error message and possible matches.
        """
        choices = await self.get_all_help_choices()
        result = process.extractBests(
            string, choices, scorer=fuzz.ratio, score_cutoff=60
        )

        return HelpQueryNotFound(f'Query "{string}" not found.', dict(result))

    @staticmethod
    def get_command_signature(command):
        parent = command.full_parent_name
        if len(command.aliases) > 0:
            aliases = "|".join(command.aliases)
            fmt = f"[{command.name}|{aliases}]"
            if parent:
                fmt = f"{parent} {fmt}"
            alias = fmt
        else:
            alias = command.name if not parent else f"{parent} {command.name}"
        return f"{alias} {command.signature}"

    async def generate_embed(self, ctx, prefix=None):
        embed = discord.Embed(color=0x00FF00)
        if not prefix:
            prefix = ctx.prefix
        embed.set_author(name="Obsidion Help", icon_url=ctx.me.avatar_url)
        embed.set_footer(
            text=f"Type {prefix}help <command> for more info on a command. You can also type {prefix}help <category> for more info on a category."
        )
        return embed

    async def send_bot_help(self, mapping):
        bot = self.context.bot
        if "@" in str(self.context.prefix):
            prefix = f"@{self.context.bot.user.name}"
        else:
            prefix = self.context.prefix
        embed = await self.generate_embed(self.context, prefix)
        embed.title = "Bot Help"
        embed.description = "Categories and commands enabled on the bot."

        for cog in bot.cogs:
            cog_commands = bot.get_cog(cog).get_commands()
            if self.context.author in bot.owner_ids:
                # allow owner to see all the commands
                cogs = [c.name for c in cog_commands]
            else:
                cogs = [c.name for c in cog_commands if not c.hidden]

            if len(cogs) > 0:
                embed.add_field(name=cog, value=f"`{'`, `'.join(cogs)}`", inline=False)

        embed.add_field(
            inline=False,
            name="Support",
            value=f"**[ADD TO SERVER](https://discord.com/oauth2/authorize?client_id={constants.Bot.clientid}&scope=bot&permissions=314448) | [SUPPORT SERVER](https://discord.gg/invite/7BRD7s6)** | **[GITHUB](https://github.com/Darkflame72/Obsidion/)** | **[WEBSITE](http://obsidion.bowie-co.nz)** | **[PATREON](https://www.patreon.com/obsidion)**",
        )
        await self.context.send(embed=embed)

    async def send_cog_help(self, cog):
        if "@" in str(self.context.prefix):
            prefix = f"@{self.context.bot.user.name}"
        else:
            prefix = self.context.prefix
        embed = await self.generate_embed(self.context, prefix)
        embed.title = f"{cog.qualified_name.capitalize()} Help"

        cog_commands = cog.get_commands()
        command_list = [(c.name, c.help, c.hidden) for c in cog_commands]

        for command in command_list:
            if command[2] and self.context.author in self.context.bot.owner_ids:
                # allows owner to view commands that are not normally visible
                embed.add_field(name=command[0], value=f"`{command[1]}`", inline=False)
            elif not command[2]:
                embed.add_field(name=command[0], value=f"`{command[1]}`", inline=False)

        embed.add_field(
            inline=False,
            name="Support",
            value=f"**[ADD TO SERVER](https://discord.com/oauth2/authorize?client_id={constants.Bot.clientid}&scope=bot&permissions=314448) | [SUPPORT SERVER](https://discord.gg/invite/7BRD7s6)** | **[GITHUB](https://github.com/Darkflame72/Obsidion/)** | **[WEBSITE](http://obsidion.bowie-co.nz)** | **[PATREON](https://www.patreon.com/obsidion)**",
        )

        await self.context.send(embed=embed)

    async def send_command_help(self, command):
        if "@" in str(self.context.prefix):
            prefix = f"@{self.context.bot.user.name}"
        else:
            prefix = self.context.prefix
        embed = await self.generate_embed(self.context, prefix)
        embed.title = f"{command.qualified_name.capitalize()} Help"
        embed.description = f"`Syntax: {prefix}{command.qualified_name} {command.signature}`\n\n{command.help}"
        if len(command.aliases) > 0:
            embed.add_field(
                name=command.name,
                value=f"""
            Name: `{command.name}`
            Aliases: `{', '.join(command.aliases)}`
            Category: `{command.cog_name}`""",
            )
        else:
            embed.add_field(
                name="Info",
                value=f"Name: `{command.name}`\nCategory: `{command.cog_name}`",
            )
        await self.context.send(embed=embed)

    async def send_group_help(self, group):
        embed = discord.Embed(colour=0x00FF00)

        subcommands = group.commands
        if len(subcommands) == 0:
            return await self.send_command_help(group)

        entries = await self.filter_commands(subcommands, sort=True)

        sub = ""
        for entry in entries:
            sub += f"`{self.context.prefix}{group.name} {entry.name}` {entry.help}.\n"
        embed.add_field(name="Sub Commands:", value=sub)

        embed.add_field(
            name="Usage",
            value=f"`{self.context.prefix}{self.get_command_signature(group)}`",
            inline=False,
        )
        if len(group.aliases) > 0:
            embed.add_field(
                name=group.name,
                value=f"""
            Name: `{group.name}`
            Aliases: `{', '.join(group.aliases)}`
            Category: `{group.cog_name}`""",
            )
        else:
            embed.add_field(
                name=group.name,
                value=f"""
            Name: `{group.name}`
            Category: `{group.cog_name}`""",
            )
        embed.set_footer(
            text=f"Type {self.context.prefix}help <command> for more info on a command. You can also type {self.context.prefix}help <category> for more info on a category."
        )

        await self.context.send(embed=embed)


class Help(commands.Cog):
    """Custom Embed Pagination Help feature."""

    def __init__(self, bot: Obsidion) -> None:
        self.bot = bot
        self._original_help_command = bot.help_command
        bot.help_command = MyHelpCommand()
        bot.help_command.cog = self
        self.bot = bot

    def cog_unload(self):
        self.bot.help_command = self._original_help_command


def setup(bot) -> None:
    """Load the Help cog."""
    bot.add_cog(Help(bot))
    log.info("Cog loaded: Help")
