"""
    HangoutCore Main File
    › Please do not modify any of the following content unless you know what you're doing. Modifying the following code and not updating the rest of the bot code to match can/will cause issues.
    › If you do decide to modify the following code please understand that HangoutCore's Dev team, Discord.py's Dev Team nor Python's Dev team are obligated to help you.
    › By Modifying the following code you acknowledge and agree to the text above.
    Last Updated: August 3rd, 2021
    Last Updated by: Lino
    Notes:
        None
"""
import asyncio
import asqlite
import ctypes,  ctypes.util
import datetime
import discord
import logging
import os, sys
import utils

from discord.ext import commands
from discord.utils import get
from utils import config, terminal

cfg = config.load() # Get Config before bot starts

class HangoutCoreBot(commands.Bot): # Sub class bot so we can have more customizability
    date = '{0:%d%b%Y_%Hh-%Mm}'.format(datetime.datetime.now())
    logging.basicConfig( # Setup logging configuration
        filename=f'{config.LOG_DIRECTORY_PATH}/log_{date}.log',
        encoding='utf-8',
        level=logging.NOTSET,
        format='[%(asctime)s][%(levelname)s] %(message)s',
        datefmt='%m/%d/%Y %I:%M:%S %p'
        )
    
    intents = utils.bot.GetIntents()
    activity = utils.bot.GetActivity()
    def __init__(self, command_prefix, terminal_args, **options):
        super().__init__(
            command_prefix,
            activity= self.activity,
            description=cfg["bot"]["description"],
            intents=self.intents, 
            **options
            )
        self.loop.create_task(self.startup())
    
        self.start_time = "" # Add the start_time variable so that we may access it for debuging or information display purposes.
        self.debug_mode = False
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

    async def startup(self):
        await self.wait_until_ready()
        self.start_time = '{0:%d%b%Y %Hh:%Mm}'.format(datetime.datetime.now())
        terminal.initiate(self.start_time, self.debug_mode)
        terminal.log("INFO", f"Looking for Bot Modules in the 'cogs' Directory.")
        cogs = utils.local.GetCogs()
        for file in cogs["valid_files"]:
            terminal.log("INFO", f" └ Found {file}")
            try:
                bot.load_extension(f'{config.COG_DIRECTORY_PATH}.{file[:-3]}')
            except Exception as e:
                utils.errorprocessing.CogLoadError(file, e, self.debug_mode)
            else:
                terminal.log("INFO", f"  └ successfully loaded {file}.")
        for file in cogs["disabled_files"]:
            terminal.log("INFO", f" └ Found Disabled file {file}, Skipping.")
        for file in cogs["invalid_files"]:
            if file == "__pycache__" or "__init__":
                pass
            else:
                terminal.log("INFO", f" └ Found invalid file {file}, Skipping.")
        terminal.log("INFO", f"Successfully loaded {len(cogs['valid_files'])} extension(s).")
        terminal.log("INFO", f"Logged in as {self.user} (ID: {self.user.id}).")
        if len(cogs["invalid_files"]) > 0:
            terminal.log("WARNING", f"Found {len(cogs['invalid_files'])} invalid extension(s) in the 'cogs' directory. If you believe this is an error please verify each .py file and make sure it is set up as a cog properly, Otherwise you can ignore this message.")
        
        opuslib = ctypes.util.find_library('opus')
        if opuslib is not None:
            try:
                terminal.log("INFO", f"Loading Opus.")
                discord.opus.load_opus('opus')
            except Exception as e:
                terminal.log("ERROR", e)
            else:
                if not discord.opus.is_loaded():
                    terminal.log("CRITICAL", "Opus Failed To Load.")
                else:
                    terminal.log("INFO", "Successfully loaded opus.")
        else:
            terminal.log("WARNING", "Could not find Opus, You will not be able to play audio without it.")
        if len(terminal.log_Q) > 0: # Display any logs that happened while we were botting up
            for q in terminal.log_Q:
                terminal.log(q[0], q[1])
                del q

        terminal.log("WARNING", "Creating a database for every guild.")
        for guild in bot.guilds:
            await utils.database.RegisterGuild(guild)
            terminal.log("INFO",f"Registered {guild.name}:{guild.id}")

    async def on_ready(self):
        self.add_view(utils.bot.CustomViews.autoroleView())
        pass

if __name__ == "__main__":
    bot = HangoutCoreBot(command_prefix=utils.bot.GetPrefix, terminal_args=sys.argv[1:])

@commands.is_owner()
@bot.command(name="load")
async def loadCog(ctx: commands.Context, cog:str):
    await ctx.message.delete()
    if not cog.endswith('.py'):
        cog = cog + '.py'
    cog = str(cog).lower()
    if cog in os.listdir(config.COG_DIRECTORY_PATH):
        if f"{config.COG_DIRECTORY_PATH}.{cog[:-3]}" in bot.extensions:
            await ctx.send(f"Sorry. That cog has already been loaded.", delete_after=15)
        else:
            try:
                bot.load_extension(f"{config.COG_DIRECTORY_PATH}.{cog[:-3]}")
            except Exception as e:
                print(e)
            else:
                embed = discord.Embed(
                        title=f"Successfully Loaded {cog}",
                        colour=discord.Colour.dark_theme(),
                        timestamp=datetime.datetime.now()
                )
                embed.set_footer(
                    text=f'Automatic Notification | Category: System',
                    icon_url=f'{bot.user.avatar.url}'
                )
                await ctx.send(embed=embed,delete_after=15)

@commands.is_owner()
@bot.command(name="unload")
async def unloadCog(ctx: commands.Context, cog:str):
    await ctx.message.delete()
    if not cog.endswith('.py'):
        cog = cog + '.py'
    cog = str(cog).lower()
    cogs = utils.local.GetCogs()
    if cog in cogs["valid_files"]:
        if f"{config.COG_DIRECTORY_PATH}.{cog[:-3]}" not in bot.extensions:
            await ctx.send(f"Sorry. That cog has already been unloaded.", delete_after=15)
        else:
            try:
                bot.unload_extension(f"{config.COG_DIRECTORY_PATH}.{cog[:-3]}")
            except Exception as e:
                print(e)
            else:
                embed = discord.Embed(
                        title=f"Successfully Unloaded {cog}",
                        colour=discord.Colour.dark_theme(),
                        timestamp=datetime.datetime.now()
                )
                embed.set_footer(
                    text=f'Automatic Notification | Category: System',
                    icon_url=f'{bot.user.avatar.url}'
                )
                await ctx.send(embed=embed,delete_after=15)
    else:
        await ctx.send(f"Sorry, that cog is not valid. Please check your spelling and try again.")

@bot.command()
async def extensions(ctx: commands.Context):
    await ctx.message.delete()
    embed = discord.Embed(
        title=f"Extensions",
        colour=discord.Colour.dark_theme(),
        timestamp=datetime.datetime.now()
    )
    embed.set_footer(
        text=f'Automatic Notification | Category: System',
        icon_url=f'{bot.user.avatar.url}'
    )
    if len(bot.extensions) > 0:
        for cog in bot.extensions:
            embed.description = bot.description +f'\n{cog}'
    else:
        embed.description = 'None'
    await ctx.send(embed=embed)
        
if isinstance(cfg["bot"]["token"], str) and cfg["bot"]["token"] != "":
    bot.run(cfg["bot"]["token"])
elif isinstance(cfg["bot"]["token"], list) and not all(token == "" for token in cfg["bot"]["token"]):
    def first_token():
        for t in cfg["bot"]["token"]:
            if t != "":
                return t
    bot.run(first_token())
else:
    terminal.log("CRITICAL", f"No token was provided in '{utils.config.CONFIG_PATH}'")
