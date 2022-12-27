"""
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    Bot Module for HangoutCore
        › Please do not modify any of the following content unless you know what you're doing. Modifying the following code and not updating the rest of the bot code to match can/will cause issues.
        › If you do decide to modify the following code please understand that HangoutCore's Dev team, Discord.py's Dev Team nor Python's Dev team are obligated to help you.
        › By Modifying the following code you acknowledge and agree to the text above.
    Module Last Updated: December 26, 2022
    Module Last Updated by: Lino
    License: Refer to LICENSE.md
    Notes:
        None
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import discord

from hangoutcore.util import Audio, Config, Database, Local, Terminal
from aiohttp import ClientSession
from datetime import datetime
from discord.ext import commands
from typing import List, Optional

class HangoutCoreBot(commands.Bot):  # Sub class bot so we can have more customizability
    def __init__(
            self,
            *args,
            activity,
            test_Guild_ID: Optional[int] = None,
            web_client,
            db_pool = None,
            debug_mode: Optional[bool] = False,
            config,
            terminal,
            **kwargs):
        super().__init__(*args, **kwargs)

        # Setup variables that we may need later on

        self.start_time = None  # Add the start_time variable so that we may access it for debugging or information display purposes.
        self.debug_mode = debug_mode

        self.web_client = web_client
        self.db_pool = db_pool
        self.config: Config = config
        self.terminal: Terminal = terminal
        self.log: Terminal.Log = terminal.Log()

        self.audio: Audio = Audio()
        self.database: Database = Database()
        self.local: Local = Local()
        self.activity = activity


        self.BotSynced = False
        # BotSynced = False
        # ViewsAdded = False

    async def syncBot(self):
        if self.debug_mode:
            devGuildID = int(self.config.CONFIG['bot']['developer_guild_id'])
            devGuild = discord.Object(devGuildID)
            if int(devGuildID) != 0:
                await self.log.DEBUG(f"Syncing to guild ID: {devGuildID}")
                # We'll copy in the global commands to test with:
                self.tree.copy_global_to(guild=devGuild)
                await self.tree.sync(guild=devGuild)
            else:
                await self.log.ERROR(f"Unable to sync to developer guild. Please provide your Guild ID in your config file.")
        else:
            await self.tree.sync()

    async def setup_hook(self) -> None:

        # here, we are loading extensions prior to sync to ensure we are syncing interactions defined in those extensions.
        self.start_time = '{0:%d%b%Y %Hh:%Mm}'.format(datetime.now())

        
        await self.audio.setConfig(self.config)
        await self.audio.setTerminal(self.terminal)
        await self.database.setConfig(self.config)
        await self.database.setTerminal(self.terminal)
        await self.database.setPool(self.db_pool)
        await self.local.setConfig(self.config)
        await self.local.setTerminal(self.terminal)

        await self.log.INFO(f"Checking for preloaded bot modules...")

        for cog in self.cogs.keys():
            await self.log.INFO(f"Found {cog}")

        await self.log.INFO(f"Looking for bot modules in '/{self.config.COG_DIRECTORY_PATH}'...")
        await self.local.load_extensions(self, self.debug_mode, False)  # Scan cog directory and enable cogs.
        await self.log.INFO(f"Looking for system bot modules")
        await self.local.load_extensions(self, self.debug_mode, True)
        await self.audio.verify_opus()  # Looks for opus and loads it if found.

        await self.syncBot()
        

        await self.log.INFO(f"Logged in as {self.user} (ID: {self.user.id}).")

    async def on_ready(self):
        # self.add_view(utils.bot.CustomViews.autoroleView())
        await self.wait_until_ready()
        
        await self.terminal.print_hr()
        await self.terminal.print_center("Bot Is Online")
        await self.terminal.print_hr()

        await self.log.WARNING("Updating Guild Database")

        for guild in self.guilds:
            await self.database.registerGuild(guild)