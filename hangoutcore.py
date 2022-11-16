"""
    HangoutCore Main File
    › Please do not modify any of the following content unless you know what you're doing. Modifying the following code and not updating the rest of the bot code to match can/will cause issues.
    › If you do decide to modify the following code please understand that HangoutCore's Dev team, Discord.py's Dev Team nor Python's Dev team are obligated to help you.
    › By Modifying the following code you acknowledge and agree to the text above.
    Last Updated: November 15, 2022
    Last Updated by: Lino
    Notes:
        None
"""

import asyncio
import ctypes,  ctypes.util
import discord
import logging
import logging.handlers
import sys

from aiohttp import ClientSession
from datetime import datetime
from discord import app_commands, ui, utils
from discord.ext import commands
from discord.utils import get
from questionnaire import Questionnaire
from typing import List, Optional
# Local modules
from util import bot,config,database,local,terminal

class HangoutCoreBot(commands.Bot): # Sub class bot so we can have more customizability
    def __init__(
        self,
        *args,
        terminal_args,
        testing_guild_id: Optional[int] = None,
        web_client: ClientSession,
        **kwargs):
        super().__init__(*args, **kwargs)

        self.web_client = web_client
        self.testing_guild_id = testing_guild_id
    
        self.start_time = "" # Add the start_time variable so that we may access it for debuging or information display purposes.
        self.debug_mode = False
        
        # BotSynced = False
        # ViewsAdded = False
        # intents = bot.GetIntents()
        # activity = bot.GetActivity()

        if len(terminal_args) > 0:
            if terminal_args[0] == "-h":
                print("\nhangoutcore.py -debug <True/False>\n")
                sys.exit(2)
            elif terminal_args[0] == "-d" or terminal_args == "-debug":
                
                if terminal_args[1] == "True":
                    self.debug_mode = True
                else:
                    self.debug_mode = False
        else:
            self.debug_mode = False

    async def setup_hook(self) -> None:

        # here, we are loading extensions prior to sync to ensure we are syncing interactions defined in those extensions.
        self.start_time = '{0:%d%b%Y %Hh:%Mm}'.format(datetime.now())
        terminal.initiate(self.start_time, self.debug_mode)
        terminal.log.INFO (f"Looking for Bot Modules in the 'cogs' Directory.")
        await local.load_extensions(self, self.debug_mode) # Scan cog directory and enable cogs.
        bot.audio.verify_opus() # Looks for opus and loads it if found.

        if self.testing_guild_id: # if a guild was passed in under testing_guild_id then we only sync with that guild.
            guild = discord.Object(self.testing_guild_id)
            # We'll copy in the global commands to test with:
            self.tree.copy_global_to(guild=guild)
            # followed by syncing to the testing guild.
            await self.tree.sync(guild=guild)
        #await self.tree.sync() # otherwise we sync globally

        terminal.log.INFO(f"Logged in as {self.user} (ID: {self.user.id}).")
        

    async def on_ready(self):
        #self.add_view(utils.bot.CustomViews.autoroleView())
        await self.wait_until_ready()
        terminal.print_hr()
        terminal.print_center("Bot Is Online")
        terminal.print_hr()
        terminal.log.WARNING("Updating Guild Database")
        for guild in self.guilds:
            #await bot.database.RegisterGuild(guild)
            terminal.log.INFO(f"Registered {guild.name}:{guild.id}")

async def main():
    init_time = '{0:%d%b%Y %Hh:%Mm}'.format(datetime.now()) # This time is used for bot reference
    if not config.exists(): # If the config does not exist
        config.setup() # Begin Config Setup process like taking in bot token, name, etc.

    logger = logging.getLogger('discord')
    logger.setLevel(logging.INFO)

    handler = logging.handlers.RotatingFileHandler(
        filename=f'{config.LOG_DIRECTORY_PATH}/log_{init_time.replace(" ","_")}.log',
        encoding='utf-8',
        maxBytes=32 * 1024 * 1024,  # 32 MiB
        backupCount=5,  # Rotate through 5 files
    )
    dt_fmt = '%m/%d/%Y %I:%M:%S %p'
    formatter = logging.Formatter("""[%(asctime)s][%(levelname)s] %(message)s""", dt_fmt)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.addHandler(handler)

    # Alternatively, you could use:
    # discord.utils.setup_logging(handler=handler, root=False)


    async with ClientSession() as our_client:

        cfg = config.load()
        activity = bot.GetActivity()
        intents = bot.GetIntents()
        #cogs = local.GetCogs()
        if cfg is not None:
                
            async with HangoutCoreBot(
                # activity = activity,
                commands.when_mentioned,
                intents = intents,
                # description = cfg["bot"]["description"],
                terminal_args = sys.argv[1:],
                web_client = our_client) as HangoutCore:
                if isinstance(cfg["bot"]["token"], str) and cfg["bot"]["token"] != "":
                    await HangoutCore.start(cfg["bot"]["token"])
                elif isinstance(cfg["bot"]["token"], list) and not all(token == "" for token in cfg["bot"]["token"]):
                    tokens = [token for token in cfg["bot"]["token"]]
                    q = Questionnaire()
                    q.one(f"token",*tokens, prompt="Which token would you like to use?")
                    q.run()
                    await HangoutCore.start(q.answers.get('token'))
                else:
                    terminal.log.CRITICAL(f"No token was provided in '{config.CONFIG_PATH}'")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("") # Clear line just incase user closes while inputting
        terminal.log.CRITICAL(f"Please refrain from using CTRL+C to shutdown bot.")
        terminal.log.CRITICAL(f"Shutting Down...")
        sys.exit(0)