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

from datetime import datetime
from discord import commands

class HangoutCoreBot(commands.Bot):  # Sub class bot so we can have more customizability
    def __init__(
            self,
            *args,
            terminal_args,
            testing_guild_id: Optional[int] = None,
            web_client: ClientSession,
            debug_mode: bool,
            **kwargs):
        super().__init__(*args, **kwargs)

        self.web_client = web_client
        self.testing_guild_id = testing_guild_id

        self.start_time = ""  # Add the start_time variable so that we may access it for debugging or information display purposes.
        self.debug_mode = debug_mode

        # BotSynced = False
        # ViewsAdded = False

    async def setup_hook(self) -> None:

        # here, we are loading extensions prior to sync to ensure we are syncing interactions defined in those extensions.
        self.start_time = '{0:%d%b%Y %Hh:%Mm}'.format(datetime.now())
        Terminal().initiate(self.start_time, self.debug_mode)
        Terminal().Log().INFO(f"Checking for preloaded bot modules...")
        for cog in self.cogs.keys():
            Terminal().Log().INFO(f"Found {cog}")

        Terminal().Log().INFO(f"Looking for bot modules in '/{config.COG_DIRECTORY_PATH}'...")
        await local().load_extensions(self, self.debug_mode)  # Scan cog directory and enable cogs.

        Bot().audio().verify_opus()  # Looks for opus and loads it if found.

        await self.tree.sync()  # sync globally 

        Terminal().Log().INFO(f"Logged in as {self.user} (ID: {self.user.id}).")

    async def on_ready(self):
        # self.add_view(utils.bot.CustomViews.autoroleView())
        await self.wait_until_ready()
        terminal = Terminal()
        terminal.print_hr()
        terminal.print_center("Bot Is Online")
        terminal.print_hr()
        terminal.Log().WARNING("Updating Guild Database")
        for guild in self.guilds:
            # await bot.database.RegisterGuild(guild)
            Terminal().Log().INFO(f"Registered {guild.name}:{guild.id}")
