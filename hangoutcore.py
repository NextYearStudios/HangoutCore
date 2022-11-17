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
import os
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

    async def setup_hook(self) -> None:

        # here, we are loading extensions prior to sync to ensure we are syncing interactions defined in those extensions.
        self.start_time = '{0:%d%b%Y %Hh:%Mm}'.format(datetime.now())
        terminal.initiate(self.start_time, self.debug_mode)
        terminal.log.INFO(f"Checking for preloaded bot modules...")
        for cog in self.cogs.keys():
            terminal.log.INFO(f"Found {cog}")

        terminal.log.INFO (f"Looking for bot modules in '/{config.COG_DIRECTORY_PATH}'...")
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

class SystemCog(commands.Cog): # We'll register system commands here just in case they need to be toggled seperately from the bot.
    def __init__(self, bot: commands.Bot):
        self.client = bot

    @app_commands.CommandTree.command
    async def system(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Test", ephemeral=True)

    @commands.is_owner()
    @app_commands.command(name="load", description=f"Load a bot cog")
    async def loadCog(self, interaction: discord.Interaction, cog: str):
        cog = str(cog).lower()
        if not cog.endswith('.py'):
            cog = cog + '.py'
        if cog in os.listdir(config.COG_DIRECTORY_PATH):
            if f"{config.COG_DIRECTORY_PATH}.{cog[:-3]}" in self.bot.extensions:
                await interaction.response.send_message(f"Sorry. That cog has already been loaded.", ephemeral=True)
            else:
                try:
                    await self.bot.load_extension(f"{config.COG_DIRECTORY_PATH}.{cog[:-3]}")
                except Exception as e:
                    print(e)
                else:
                    embed = discord.Embed(
                            title=f"Successfully Loaded {cog}",
                            colour=discord.Colour.dark_theme(),
                            timestamp=datetime.now()
                    )
                    embed.set_footer(
                        text=f'Automatic Notification | Category: System',
                        icon_url=f'{self.bot.user.avatar.url}'
                    )
                    await interaction.response.send_message(embed=embed, ephemeral=True)

    @commands.is_owner()
    @app_commands.command(name="unload", description=f"Unload a bot cog.")
    async def unloadCog(self, interaction: discord.Interaction, cog: str):
        cog = str(cog).lower()
        cogs = local.GetCogs()
        if not cog.endswith('.py'):
            cog = cog + '.py'

        if cog in cogs["valid_files"]:
            if f"{config.COG_DIRECTORY_PATH}.{cog[:-3]}" not in self.bot.extensions:
                await interaction.response.send_message(f"Sorry. That cog has already been unloaded.", ephemeral=True)
            else:
                try:
                    await self.bot.unload_extension(f"{config.COG_DIRECTORY_PATH}.{cog[:-3]}")
                except Exception as e:
                    print(e)
                else:
                    embed = discord.Embed(
                            title=f"Successfully Unloaded {cog}",
                            colour=discord.Colour.dark_theme(),
                            timestamp=datetime.now()
                    )
                    embed.set_footer(
                        text=f'Automatic Notification | Category: System',
                        icon_url=f'{self.bot.user.avatar.url}'
                    )
                    await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            await interaction.response.send_message(f"Sorry, that cog is not valid. Please check your spelling and try again.", ephemeral=True)

    @app_commands.command(description=f"Retrieve bot extensions.")
    async def extensions(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title=f"Enabled Bot Modules",
            colour=discord.Colour.dark_theme(),
            description=f"",
            timestamp=datetime.now()
        )
        embed.set_footer(
            text=f'Automatic Notification | Category: System',
            icon_url=f'{self.client.user.avatar.url}'
        )
        for key in self.client.cogs.keys():
            embed.description = embed.description + f"{key}\n"
        await interaction.response.send_message(embed=embed, ephemeral=True)


async def main():
    if '-h' in sys.argv[1:] or '-help' in sys.argv[1:]:
        print(f"""
[-c, -config : string] Load the specified config, Also sets as default. If the specified config cannot be found, return to previous config as a precaution.

[-d, -debug : True/False] Enable debug mode for more information to be displayed in the terminal. Changes log mode to DEBUG.

[-n, -new] Manually put HangoutCore in a setup state in order to create a new configuration. Sets the new config as default.

[-s, -silent : True/False] Enable/Disable to have information sent to log only, or terminal and log. Useful for running as a service since there's no access to terminal.

[-t, -token : integer] Specify which token to use if you're using multiple. Allows user to skip token choice prompt.

        """)
    else:
        init_time = '{0:%d%b%Y %Hh:%Mm}'.format(datetime.now()) # This time is used for bot reference
        if '-c' in sys.argv[1:]:
            config.init(sys.argv[1:][sys.argv[1:].index('-c') + 1])
        elif '-config' in sys.argv[1:]:
            config.init(sys.argv[1:][sys.argv[1:].index('-config') + 1])

        if not config.exists() or '-n' in sys.argv[1:] or '-new' in sys.argv[1:]: # If the config does not exist
            config.setup(init_time, True) # Begin Config Setup process like taking in bot token, name, etc.
            config.init()
        else:
            config.init()

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
        terminalArgs = sys.argv[1:]

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
                    testing_guild_id=514091020535857155,
                    terminal_args = terminalArgs,
                    web_client = our_client) as HangoutCore:
                    if isinstance(cfg["bot"]["token"], str) and cfg["bot"]["token"] != "":
                        await HangoutCore.add_cog(SystemCog(HangoutCore))
                        await HangoutCore.start(cfg["bot"]["token"])

                    elif isinstance(cfg["bot"]["token"], list) and not all(token == "" for token in cfg["bot"]["token"]):
                        if '-t' in terminalArgs:
                            await HangoutCore.add_cog(SystemCog(HangoutCore))
                            await HangoutCore.start(cfg['bot']['token'][int(terminalArgs[terminalArgs.index('-t') + 1])])
                        elif '-token' in terminalArgs:
                            await HangoutCore.add_cog(SystemCog(HangoutCore))
                            await HangoutCore.start(cfg['bot']['token'][int(terminalArgs[terminalArgs.index('-token') + 1])])
                        else:
                            tokens = [token for token in cfg["bot"]["token"]]
                            q = Questionnaire()
                            q.one(f"token",*tokens, prompt=f"Current config loaded: {config.COG_DIRECTORY_PATH}/{config.CONFIG_PATH}.\nWhich token would you like to use?")
                            q.run()
                            await HangoutCore.add_cog(SystemCog(HangoutCore))
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