import datetime
from io import BytesIO
from typing import List, Optional, Sequence, SupportsInt

import discord


def error(text: str) -> str:
    """Create an Error sign to the start of the message.

    Args:
        text (str): Text to go in the message.

    Returns:
        str: Updated Message
    """
    return f"\N{NO ENTRY SIGN} {text}"


def warning(text: str) -> str:
    """Create an Warning sign to the start of the message.

    Args:
        text (str): Text to go in the message.

    Returns:
        str: Updated Message
    """
    return f"\N{WARNING SIGN} {text}"


def info(text: str) -> str:
    """Create an Info sign to the start of the message.

    Args:
        text (str): Text to go in the message.

    Returns:
        str: Updated Message
    """
    return f"\N{INFORMATION SOURCE} {text}"


def question(text: str) -> str:
    """Create an Question sign to the start of the message.

    Args:
        text (str): Text to go in the message.

    Returns:
        str: Updated Message
    """
    return f"\N{BLACK QUESTION MARK ORNAMENT} {text}"


def bold(text: str, escape_formatting: bool = True) -> str:
    """Turns the text to bold.

    Args:
        text (str): Text to go in the message.

    Returns:
        str: Updated Message
    """
    text = escape(text, formatting=escape_formatting)
    return f"**{text}**"


def box(text: str, lang: str = "") -> str:
    """Get the given text in a code block.

    Args:
        text (str): Text to go in the message.

    Returns:
        str: Updated Message
    """
    ret = f"```{lang}\n{text}\n```"
    return ret


def inline(text: str) -> str:
    """Get the given text as inline code.

    Args:
        text (str): Text to go in the message.

    Returns:
        str: Updated Message
    """
    if "`" in text:
        return f"``{text}``"
    return f"`{text}`"


def italics(text: str, escape_formatting: bool = True) -> str:
    """Convert text into italics

    Args:
        text (str): Text to convert
        escape_formatting (bool, optional): Wether to escape formatting. Defaults to True.

    Returns:
        str: italic text
    """
    text = escape(text, formatting=escape_formatting)
    return f"*{text}*"


def underline(text: str, escape_formatting: bool = True) -> str:
    """
    Get the given text with an underline.

    Args:
        text (str): text to underline
        escape_formatting (bool, optional): Wether to escape formatting. Defaults to True.

    Returns:
        str: Underlined text.
    """
    text = escape(text, formatting=escape_formatting)
    return f"__{text}__"


def strikethrough(text: str, escape_formatting: bool = True) -> str:
    """Get the given text with a strikethrough.

    Note: By default, this function will escape ``text`` prior to applying a strikethrough.
    Args:
        text (str): text to underline
        escape_formatting (bool, optional): Wether to escape formatting. Defaults to True.

    Returns:
        str: underlined text
    """
    text = escape(text, formatting=escape_formatting)
    return f"~~{text}~~"


def escape(text: str, *, mass_mentions: bool = False, formatting: bool = False) -> str:
    """Escape text with markdown or mass mentions removed

    Args:
        text (str): text to escape
        mass_mentions (bool, optional): Wether to espace mass mentions. Defaults to False.
        formatting (bool, optional): Wether to escape markdown. Defaults to False.

    Returns:
        str: escaped text
    """
    if mass_mentions:
        text = text.replace("@everyone", "@\u200beveryone")
        text = text.replace("@here", "@\u200bhere")
    if formatting:
        text = discord.utils.escape_markdown(text)
    return text


def humanize_list(items: Sequence[str]) -> str:
    """Get comma-separted list, with the last element joined with *and*.
    This uses an Oxford comma, because without one, items containing
    the word *and* would make the output difficult to interpret.

    Args:
        items (Sequence[str]): list to humanize

    Raises:
        IndexError: Empty sequence provided

    Returns:
        str: humanized list
    """
    if len(items) == 1:
        return items[0]
    try:
        return ", ".join(items[:-1]) + ", and " + items[-1]
    except IndexError:
        raise IndexError("Cannot humanize empty sequence") from None


def format_perms_list(perms: discord.Permissions) -> str:
    """Format a list of permission names.
    This will return a humanized list of the names of all enabled
    permissions in the provided `discord.Permissions` object.

    Args:
        perms (discord.Permissions): [description]

    Returns:
        str: [description]
    """
    perm_names: List[str] = []
    for perm, value in perms:
        if value is True:
            perm_name = '"' + perm.replace("_", " ").title() + '"'
            perm_names.append(perm_name)
    return humanize_list(perm_names).replace("Guild", "Server")


def humanize_timedelta(
    *,
    timedelta: Optional[datetime.timedelta] = None,
    seconds: Optional[SupportsInt] = None,
) -> str:
    """Get a locale aware human timedelta representation.
    This works with either a timedelta object or a number of seconds.
    Fractional values will be omitted, and values less than 1 second
    an empty string.

    Args:
        timedelta (Optional[datetime.timedelta], optional): Timedelta to convert. Defaults to None.
        seconds (Optional[SupportsInt], optional): Seconds to convert. Defaults to None.

    Raises:
        ValueError: Not a valid timedelta

    Returns:
        str: String of the timedelta.
    """

    try:
        obj = seconds if seconds is not None else timedelta.total_seconds()
    except AttributeError:
        raise ValueError("You must provide either a timedelta or a number of seconds")

    seconds = int(obj)
    periods = [
        ("year", "years", 60 * 60 * 24 * 365),
        ("month", "months", 60 * 60 * 24 * 30),
        ("day", "days", 60 * 60 * 24),
        ("hour", "hours", 60 * 60),
        ("minute", "minutes", 60),
        ("second", "seconds", 1),
    ]

    strings = []
    for period_name, plural_period_name, period_seconds in periods:
        if seconds >= period_seconds:
            period_value, seconds = divmod(seconds, period_seconds)
            if period_value == 0:
                continue
            unit = plural_period_name if period_value > 1 else period_name
            strings.append(f"{period_value} {unit}")

    return ", ".join(strings)


def text_to_file(
    text: str,
    filename: str = "file.txt",
    *,
    spoiler: bool = False,
    encoding: str = "utf-8",
) -> discord.File:
    """Prepares text to be sent as a file on Discord, without character limit.
    This writes text into a bytes object that can be used for the ``file`` or
    ``files`` parameters of :meth:`discord.abc.Messageable.send`.

    Args:
        text (str): Contents of file.
        filename (str, optional): Name of the file. Defaults to "file.txt".
        spoiler (bool, optional): Wether the file will have a spoiler. Defaults to False.
        encoding (str, optional): Encoding which the file will use. Defaults to "utf-8".

    Returns:
        discord.File: File ready to be sent into discord
    """
    file = BytesIO(text.encode(encoding))
    return discord.File(file, filename, spoiler=spoiler)
