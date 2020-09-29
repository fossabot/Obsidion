#!/usr/bin/env python

import logging

import discord
from discord.ext.commands import when_mentioned_or

# Set the event loop policies here so any subsequent `new_event_loop()`
# calls, in particular those as a result of the following imports,
# return the correct loop object.
from obsidion import _update_event_loop_policy, constants
from obsidion.bot import Obsidion

_update_event_loop_policy()


log = logging.getLogger("obsidion.main")

# set activity
activity = discord.Activity(
    name=constants.Bot.status,
    type=discord.ActivityType.watching,
)

mentions = discord.AllowedMentions(
    everyone=False,
)

bot = Obsidion(
    case_insensitive=True,
    activity=activity,
    command_prefix=when_mentioned_or(constants.Bot.default_prefix),
    allowed_mentions=mentions,
)

# Load all required cogs

# core cogs
bot.load_extension("obsidion.core.development")
bot.load_extension("obsidion.core.help")
bot.load_extension("obsidion.core.error_handler")

# extensions and main features
bot.load_extension("obsidion.cogs.fun")
bot.load_extension("obsidion.cogs.hypixel")
bot.load_extension("obsidion.cogs.images")
bot.load_extension("obsidion.cogs.info")
bot.load_extension("obsidion.cogs.misc")
# bot.load_extension("obsidion.cogs.rcon")
bot.load_extension("obsidion.cogs.redstone")
bot.load_extension("obsidion.cogs.servers")
bot.load_extension("obsidion.cogs.events")
bot.load_extension("obsidion.cogs.config")
# bot.load_extension("obsidion.cogs.minecraft")

if constants.Discord_bot_list.voting_enabled:
    bot.load_extension("cogs.botlist")

# run bot
bot.run(constants.Bot.discord_token)
