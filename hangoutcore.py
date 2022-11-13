"""
    HangoutCore Main File
    › Please do not modify any of the following content unless you know what you're doing. Modifying the following code and not updating the rest of the bot code to match can/will cause issues.
    › If you do decide to modify the following code please understand that HangoutCore's Dev team, Discord.py's Dev Team nor Python's Dev team are obligated to help you.
    › By Modifying the following code you acknowledge and agree to the text above.
    Last Updated: November 13, 2022
    Last Updated by: Lino
    Notes:
        None
"""

import asyncio
import ctypes,  ctypes.util
import discord
import logging
import logging.handlers
import util
import sys

from aiohttp import ClientSession
from datetime import datetime
from discord import app_commands, ui, utils
from discord.ext import commands
from discord.utils import get
from typing import List, Optional
from util import bot

cfg = util.bot.config.load()

class HangoutCoreBot(commands.Bot): # Sub class bot so we can have more customizability
    date = '{0:%d%b%Y_%Hh-%Mm}'.format(datetime.now())
    BotSynced = False
    ViewsAdded = False
    intents = bot.GetIntents()
    activity = bot.GetActivity()
    def __init__(
        self,
        *args,
        command_prefix, 
        terminal_args,
        initial_extensions: List[str],
        web_client: ClientSession,
        testing_guild_id: Optional[int] = None,
        **kwargs):
        super().__init__(command_prefix, activity= self.activity, description=cfg["bot"]["description"], intents=self.intents, **kwargs)
        self.web_client = web_client
        self.testing_guild_id = testing_guild_id
        self.initial_extensions = initial_extensions
    
        self.start_time = "" # Add the start_time variable so that we may access it for debuging or information display purposes.
        self.debug_mode = False
        self.ticket_mod = 760151284098793519
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
        bot.terminal.initiate(self.start_time, self.debug_mode)
        bot.terminal.log.INFO (f"Looking for Bot Modules in the 'cogs' Directory.")

        for file in self.initial_extensions["valid_files"]:
            bot.terminal.log.INFO(f" └ Found {file}")
            try:
                await self.load_extension(f'{bot.config.COG_DIRECTORY_PATH}.{file[:-3]}')
            except Exception as e:
                bot.errorprocessing.CogLoadError(file, e, self.debug_mode)
            else:
                bot.terminal.log.INFO(f"  └ successfully loaded {file}.")
        for file in self.initial_extensions["disabled_files"]:
            bot.terminal.log.INFO(f" └ Found Disabled file {file}, Skipping.")
        for file in self.initial_extensions["invalid_files"]:
            if file == "__pycache__" or "__init__":
                pass
            else:
                bot.terminal.log.INFO(f" └ Found invalid file {file}, Skipping.")
        bot.terminal.log.INFO(f"Successfully loaded {len(self.initial_extensions['valid_files'])} extension(s).")
        bot.terminal.log.INFO(f"Logged in as {self.user} (ID: {self.user.id}).")
        if len(self.initial_extensions["invalid_files"]) > 0:
            bot.terminal.log.WARNING(f"Found {len(self.initial_extensions['invalid_files'])} invalid extension(s) in the 'cogs' directory. If you believe this is an error please verify each .py file and make sure it is set up as a cog properly, Otherwise you can ignore this message.")
        
        opuslib = ctypes.util.find_library('opus')
        if opuslib is not None:
            try:
                bot.terminal.log.INFO(f"Loading Opus.")
                discord.opus.load_opus('opus')
            except Exception as e:
                bot.terminal.log.ERROR(e)
            else:
                if not discord.opus.is_loaded():
                    bot.terminal.log.CRITICAL("Opus Failed To Load. It's corn! A big lump with knobs. It's got the juice!")
                else:
                    bot.terminal.log.INFO("Successfully loaded opus.")
        else:
            bot.terminal.log.WARNING("Could not find Opus, You will not be able to play audio without it.")
        
        #if len(terminal.log_Q) > 0: # Display any logs that happened while we were botting up
        #    for q in terminal.log_Q:
        #        terminal.log(q[0], q[1])
        #        del q

        # In overriding setup hook,
        # we can do things that require a bot prior to starting to process events from the websocket.
        # In this case, we are using this to ensure that once we are connected, we sync for the testing guild.
        # You should not do this for every guild or for global sync, those should only be synced when changes happen.
        if self.testing_guild_id:
            guild = discord.Object(self.testing_guild_id)
            # We'll copy in the global commands to test with:
            self.tree.copy_global_to(guild=guild)
            # followed by syncing to the testing guild.
            await self.tree.sync(guild=guild)
        await self.tree.sync()

        # This would also be a good place to connect to our database and
        # load anything that should be in memory prior to handling events.

    async def on_ready(self):
        #self.add_view(utils.bot.CustomViews.autoroleView())
        await self.wait_until_ready()
        bot.terminal.print_hr()
        bot.terminal.print_center("Bot Is Online")
        bot.terminal.print_hr()
        bot.terminal.log.WARNING("Updating Guild Database")
        for guild in self.guilds:
            #await bot.database.RegisterGuild(guild)
            bot.terminal.log.INFO(f"Registered {guild.name}:{guild.id}")

async def main():
    init_time = '{0:%d%b%Y %Hh:%Mm}'.format(datetime.now()) # This time is used for bot reference
    if not util.bot.config.exists(): # If the config does not exist
        util.bot.config.setup(init_time) # Begin Config Setup process like taking in bot token, name, etc.

    
    logger = logging.getLogger('discord')
    logger.setLevel(logging.NOTSET)

    handler = logging.handlers.RotatingFileHandler(
        filename=f'{util.bot.config.LOG_DIRECTORY_PATH}/log_{init_logtime.replace(" ","_")}.log',
        encoding='utf-8',
        maxBytes=32 * 1024 * 1024,  # 32 MiB
        backupCount=5,  # Rotate through 5 files
    )
    dt_fmt = '%m/%d/%Y %I:%M:%S %p'
    formatter = logging.Formatter("""[%(asctime)s][%(levelname)s] %(message)s""", dt_fmt)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    discord.utils.setup_logging(handler=handler, root=False)# level=logging.NOTSET,

    # Alternatively, you could use:
    # discord.utils.setup_logging(handler=handler, root=False)

    # One of the reasons to take over more of the process though
    # is to ensure use with other libraries or tools which also require their own cleanup.

    # Here we have a web client and a database pool, both of which do cleanup at exit.
    # We also have our bot, which depends on both of these.

    

    async with ClientSession() as our_client:
        # 2. We become responsible for starting the bot.

        cogs = util.bot.local.GetCogs()
        async with HangoutCoreBot(command_prefix=util.bot.GetPrefix, web_client=our_client,testing_guild_id=cfg["bot"]["developer_guild_id"], initial_extensions=cogs,terminal_args=sys.argv[1:]) as bot:
            if isinstance(cfg["bot"]["token"], str) and cfg["bot"]["token"] != "":
                await bot.start(cfg["bot"]["token"])
            elif isinstance(cfg["bot"]["token"], list) and not all(token == "" for token in cfg["bot"]["token"]):
                def first_token():
                    for t in cfg["bot"]["token"]:
                        if t != "":
                            return t
                await bot.start(first_token())
            else:
                util.bot.terminal.log.CRITICAL(f"No token was provided in '{bot.config.CONFIG_PATH}'")

        
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("") # Clear line just incase user closes while inputting
        bot.terminal.log.CRITICAL(f"Please refrain from using CTRL+C to shutdown bot.")
        bot.terminal.log.CRITICAL(f"Shutting Down...")
        sys.exit(0)
