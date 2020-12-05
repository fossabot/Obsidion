"""Hypixel related commands."""

from asyncpixel import Client
import discord
from discord.ext import commands
from dpymenus import Page, PaginatedMenu

from obsidion import constants
from obsidion.utils.utils import usernameToUUID
from obsidion.utils.utils import UUIDToUsername
from obsidion.utils.utils import divide_array
from obsidion.utils.chat_formatting import humanize_timedelta
import datetime


class hypixel(commands.Cog):
    """Hypixel cog."""

    def __init__(self, bot) -> None:
        """Init."""
        self.bot = bot
        self.session = bot.http_session

        self.hypixel_session = Client(api_key=str(constants.Bot.hypixelapi_token))

    @commands.command()
    async def watchdogstats(self, ctx: commands.Context) -> None:
        """Get the current watchdog statistics."""
        await ctx.channel.trigger_typing()
        data = await self.hypixel_session.get_watchdog_stats()
        embed = discord.Embed(title="Watchdog Stats", colour=0x00FF00)
        embed.add_field(
            name="Total Bans", value=f"{(data.watchdog_total + data.staff_total):,}"
        )
        embed.add_field(
            name="Watchdog Rolling Daily", value=f"{data.watchdog_rollingDaily:,}"
        )
        # embed.add_field(name="Last Minute", value=f"{data.last_minute:,}")
        embed.add_field(name="Staff Total", value=f"{data.staff_total:,}")
        embed.add_field(
            name="Staff Rolling Daily", value=f"{data.staff_rollingDaily:,}"
        )
        embed.timestamp = ctx.message.created_at
        await ctx.send(embed=embed)

    @commands.command()
    async def boosters(self, ctx: commands.Context) -> None:
        """Get the current boosters online."""
        await ctx.channel.trigger_typing()
        data = await self.hypixel_session.get_boosters()
        # it is a tuple of a list of all the different boosters
        embed = discord.Embed(
            title="Boosters",
            description=f"Total Boosters online: {len(data.boosters):,}",
            colour=0x00FF00,
        )
        embed.set_author(
            name="Hypixel",
            url="https://hypixel.net/forums/skyblock.157/",
            icon_url="https://hypixel.net/favicon-32x32.png",
        )
        embed.set_thumbnail(
            url="https://hypixel.net/styles/hypixel-v2/images/header-logo.png"
        )
        embed.timestamp = ctx.message.created_at
        await ctx.send(embed=embed)

    @commands.command()
    async def playercount(self, ctx: commands.Context) -> None:
        """Get the current players online."""
        await ctx.channel.trigger_typing()
        data = await self.hypixel_session.get_player_count()
        embed = discord.Embed(
            title="Players Online",
            description=f"Total Players online: {data}",            
            colour=0x00FF00,
        )
        embed.set_author(
            name="Hypixel",
            url="https://hypixel.net/forums/skyblock.157/",
            icon_url="https://hypixel.net/favicon-32x32.png",
        )
        embed.set_thumbnail(
            url="https://hypixel.net/styles/hypixel-v2/images/header-logo.png"
        )
        embed.timestamp = ctx.message.created_at
        await ctx.send(embed=embed)

    @commands.command()
    async def skyblocknews(self, ctx: commands.Context) -> None:
        """Get current Skyblock News."""
        await ctx.channel.trigger_typing()
        data = await self.hypixel_session.get_news()

        embed = discord.Embed(
                title="Skyblock News",
                description=f"There are currently {len(data)} news articles.",
                colour=0x00FF00,
            )
        embed.set_author(
            name="Hypixel",
            url="https://hypixel.net/forums/skyblock.157/",
            icon_url="https://hypixel.net/favicon-32x32.png",
        )
        embed.set_thumbnail(
            url="https://hypixel.net/styles/hypixel-v2/images/header-logo.png"
        )
        for i in range(len(data)):
            embed.add_field(name=f"{data[i].title}", value=f"[{data[i].text}]({data[i].link})")

        embed.timestamp = ctx.message.created_at
        await ctx.send(embed=embed)
            
    @commands.command()
    async def playerstatus(self, ctx: commands.Context, username: str) -> None:
        """Get the current Status of Players."""
        await ctx.channel.trigger_typing()
        UUID = await usernameToUUID(username, ctx.bot.http_session)
        if UUID == False:
            await ctx.send("Sorry, we could not find that player. Please try a different username.")
            return
        else:
            data = await self.hypixel_session.get_player_status(uuid=UUID)

        if data.online == False:
            await ctx.send("That player is not currently online.")
            return
        else:
            embed = discord.Embed(
                title="Player Status",
                description=f"Current Status of Player {username}",            
                colour=0x00FF00,
            )
            embed.set_author(
                name="Hypixel",
                icon_url="https://hypixel.net/favicon-32x32.png",
            )
            embed.set_thumbnail(
                url=f"https://visage.surgeplay.com/bust/{UUID}"
            )
            embed.add_field(
                name="Current Game: ", value=f"{data.gameType}"
            )
            embed.add_field(
                name="Current Game Mode: ", value=f"{data.mode}"
            )
            embed.timestamp = ctx.message.created_at
        
        await ctx.send(embed=embed)

    @commands.command()
    async def playerfriends(self, ctx: commands.Context, username: str) -> None:
        """Get the current friends of a player"""
        await ctx.channel.trigger_typing()
        UUID = await usernameToUUID(username, ctx.bot.http_session)
        if UUID == False:
            await ctx.send("Sorry, we could not find that player. Please try a different username.")
            return
        else:
            data = await self.hypixel_session.get_player_friends(uuid=UUID)

        embed = discord.Embed(
            title=f"Current Friends for {username}",            
            colour=0x00FF00,
        )
        embed.set_author(
            name="Hypixel",
            icon_url="https://hypixel.net/favicon-32x32.png",
        )
        embed.set_thumbnail(
            url=f"https://visage.surgeplay.com/bust/{UUID}"
        )
        embed.timestamp = ctx.message.created_at

        for i in range(len(data)):
            if data[i].uuidReceiver == UUID:
                friendUsername = await UUIDToUsername(data[i].uuidSender, ctx.bot.http_session)
            else:
                friendUsername = await UUIDToUsername(data[i].uuidReceiver, ctx.bot.http_session)
            
            delta = datetime.datetime.utcnow() - data[i].started
            friendStarted = humanize_timedelta(timedelta=delta)
            friendStartedSplit = friendStarted.split(", ")
            friendStarted = friendStartedSplit[0] + ", " + friendStartedSplit[1]
            embed.add_field(
                name=f"{friendUsername}", value=f"Been friends for: {friendStarted}"
            )
            
        await ctx.send(embed=embed)

    @commands.command()
    async def bazaar(self, ctx: commands.Context) -> None:
        """Get Bazaar NPC Stats."""
        await ctx.channel.trigger_typing()

        menu = PaginatedMenu(ctx)
        data = await self.hypixel_session.get_bazaar()
        split = list(divide_array(data.bazaar_items, 15))
        pagesend = []

        for bazaarloop in range(len(split)):
            pagebazaar = Page(title='Bazaar NPC Stats', description=f'Page {bazaarloop + 1} of {len(split) + 1}', color=0x00FF00)
            pagebazaar.set_author(
                name="Hypixel",
                icon_url="https://hypixel.net/favicon-32x32.png",
            )
            for item in range(len(split[bazaarloop])):
                name = split[bazaarloop][item].name.replace('_', ' ').title()
                sellprice = round(split[bazaarloop][item].quick_status.sellPrice)
                buyprice = round(split[bazaarloop][item].quick_status.buyPrice)
                pagebazaar.add_field(name=name, value=f'Sell Price: {sellprice} \n Buy Price: {buyprice}')
            pagesend.append(pagebazaar)

        menu.add_pages(pagesend)

        await menu.open()

    @commands.command()
    async def auctions(self, ctx: commands.Context) -> None:
        """Shows the first 1000 auctions"""
        await ctx.channel.trigger_typing()

        menu = PaginatedMenu(ctx)
        data = await self.hypixel_session.auctions()
        split = list(divide_array(data.auctions, 15))
        pagesend = []

        for auctionsloop in range(len(split)):
            pageauctions = Page(title=f'Hypixel Auctions', description=f'Page {auctionsloop + 1} of {len(split) + 1}', color=0x00FF00)
            pageauctions.set_author(name='Hypixel', icon_url='https://hypixel.net/favicon-32x32.png')
            for item in range(len(split[auctionsloop])):
                name = split[auctionsloop][item].item_name
                startingBid = split[auctionsloop][item].starting_bid
                highestBid = split[auctionsloop][item].highest_bid_amount
                bids = split[auctionsloop][item].bids
                pageauctions.add_field(name=name, value=f'Starting Bid: {startingBid} \n Highest Bid: {highestBid} \n Current Bids: {len(bids)}')
            pagesend.append(pageauctions)

        menu.add_pages(pagesend)

        await menu.open()

        
