"""
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    Bot Module for HangoutCore
        › Please do not modify any of the following content unless you know what you're doing. Modifying the following code and not updating the rest of the bot code to match can/will cause issues.
        › If you do decide to modify the following code please understand that HangoutCore's Dev team, Discord.py's Dev Team nor Python's Dev team are obligated to help you.
        › By Modifying the following code you acknowledge and agree to the text above.
    Module Last Updated: December 7, 2022
    Module Last Updated by: Lino
    License: Refer to LICENSE.md
    Notes:
        None
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import discord

from hangoutcore.util import Audio, Config, Local, Terminal
from aiohttp import ClientSession
from datetime import datetime
from discord.ext import commands
from typing import List, Optional

class HangoutCoreBot(commands.Bot):  # Sub class bot so we can have more customizability
    def __init__(
            self,
            *args,
            test_Guild_ID: Optional[int] = None,
            web_client,
            debug_mode: Optional[bool] = False,
            config,
            terminal,
            **kwargs):
        super().__init__(*args, **kwargs)

        # Setup variables that we may need later on

        self.start_time = None  # Add the start_time variable so that we may access it for debugging or information display purposes.
        self.test_Guild_ID : int = test_Guild_ID # This is for testing slash commands. That way we don't sync globally every time we run
        self.debug_mode = debug_mode

        self.web_client = web_client
        self.config = config
        self.terminal = terminal


        self.BotSynced = False
        # BotSynced = False
        # ViewsAdded = False
        self.local = Local()
        self.local.setConfig(self.config)
        self.local.setTerminal(self.terminal)

    async def setup_hook(self) -> None:

        # here, we are loading extensions prior to sync to ensure we are syncing interactions defined in those extensions.
        self.start_time = '{0:%d%b%Y %Hh:%Mm}'.format(datetime.now())
        self.terminal.Log().INFO(f"Checking for preloaded bot modules...")

        for cog in self.cogs.keys():
            self.terminal.Log().INFO(f"Found {cog}")

        self.terminal.Log().INFO(f"Looking for bot modules in '/{self.config.COG_DIRECTORY_PATH}'...")
        await self.local.load_extensions(self, self.debug_mode)  # Scan cog directory and enable cogs.

        Audio().verify_opus()  # Looks for opus and loads it if found.

        if self.debug_mode or self.test_Guild_ID is not None:
            self.tree.sync(guild=self.test_Guild_ID)
        else:
            if not self.BotSynced:
                await self.tree.sync()
                self.BotSynced = True
        

        self.terminal.Log().INFO(f"Logged in as {self.user} (ID: {self.user.id}).")

    async def on_ready(self):
        # self.add_view(utils.bot.CustomViews.autoroleView())
        await self.wait_until_ready()
        
        self.terminal.print_hr()
        self.terminal.print_center("Bot Is Online")
        self.terminal.print_hr()
        self.terminal.Log().WARNING("Updating Guild Database")
        for guild in self.guilds:
            # await bot.database.RegisterGuild(guild)
            self.terminal.Log().INFO(f"Registered {guild.name}:{guild.id}")