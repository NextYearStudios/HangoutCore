"""
    HangoutCore's Main Script.
    ----------
    Last Updated: Jan 21, 2024
    Last Updated by: Lino
    License: Refer to LICENSE.md
    Notes:
        None
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    This script handles the following:
    ----------
    Starting/Stopping Discord Bot
    Starting/Stopping Database
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    WARNING: This is a Core Script
    ----------
        › Please do not modify any of the following content unless you know what you're doing. Modifying the following code and not updating the rest of the bot 
            code to match can/will cause issues.
        › If you do decide to modify the following code please understand that HangoutCore's Dev team, Discord.py's Dev Team nor Python's Dev team are obligated
            to help you.
        › By Modifying the following code you acknowledge and agree to the text above.
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Section Title: Dependencies

import asyncio
import discord
import hangoutcore
import aiomysql
import logging
import logging.handlers
import os
import requests
import shutil
import sys

from aiohttp import ClientSession
from datetime import datetime
from discord.ext import commands
from multiprocessing import Pool, Process
from pathlib import Path

# from rich import print
import rich
from rich.columns import Columns
from rich.console import Console, Group
from rich.layout import Layout
from rich.live import Live
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Confirm, IntPrompt, InvalidResponse
from rich.table import Table

# from hangoutcore.util import *
from hangoutcore.bot import HangoutCoreBot
from hangoutcore.utils import *
from hangoutcore.app import HangoutCoreApp
# from questionnaire import Questionnaire

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Section Title: Functions

async def main():
    sys.path.append(os.getcwd()) # This expands package finding to our working directory 
    hangoutcore.INIT_TIME = '{0:%d%b%Y %Hh:%Mm}'.format(datetime.now())
    console = terminal.console
    
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # Section Title: Argument parsing

    async def invalid_arg(r:int):
        hangoutcore.INVALID_ARGS = True
        terminal.print_center("━", "━")
        terminal.print_center("Warning:")
        terminal.print_center("━", "━")

        if r == 0:
            terminal.log.ERROR("You've provided an incorrect argument. Please double check your input and try again.")
        elif r == 1:
            terminal.log.ERROR("You're missing an argument. Please double check your input and try again.")
        elif r == 2:
            terminal.log.ERROR("The argument you provided requires a numeric value. Please double check your input and try again.")
        elif r == 3:
            terminal.log.ERROR("The argument you provided requires a string value. Please double check your input and try again.")
        elif r == 4:
            terminal.log.ERROR("The argument you provided requires a bool value. Please double check your input and try again.")

        print(f"Provided arguments: {sys.argv[1:]}")

    async def process_arguments(argv:list[str]):
        if '--help' in argv or '-h' in argv:
            terminal.print_center("━", "━")
            terminal.print_center("Help")
            terminal.print_center("━", "━")
            terminal.print_logo()
            print(hangoutcore.responses.help)
            sys.exit(0)

        if '--silent' in argv or '-s' in argv:
            _position = None
            if '--silent' in argv:
                _position = argv.index('--silent')
            elif '-s' in argv:
                _position = argv.index('-s')

            if _position is not None:
                try:
                    if argv[_position + 1].lower() == "true":
                        hangoutcore.SILENT = True
                    else:
                        hangoutcore.SILENT = False
                except IndexError:
                    await invalid_arg(1)
                else:
                    argv.pop(_position + 1)
                    argv.pop(_position)

        if '--debug' in argv or '-d' in argv:
            _position = None
            if '--debug' in argv:
                _position = argv.index('--debug')
            elif '-d' in argv:
                _position = argv.index('-d')

            if _position is not None:
                try:
                    if argv[_position + 1].lower() == "true":
                        hangoutcore.DEBUG = True
                    else:
                        hangoutcore.DEBUG = False
                except IndexError:
                    await invalid_arg(1)
                else:
                    argv.pop(_position + 1)
                    argv.pop(_position)

        if '--new' in argv or '-n' in argv:
            _position = None
            if '--new' in argv:
                _position = argv.index('--new')
            elif '-n' in argv:
                _position = argv.index('-n')

            if _position is not None:
                try:
                    if argv[_position + 1].lower() == "true":
                        hangoutcore.FRESH_INSTALL = True
                    else:
                        hangoutcore.FRESH_INSTALL = False
                except IndexError:
                    await invalid_arg(1)
                else:
                    argv.pop(_position + 1)
                    argv.pop(_position)

        if '--token' in argv or '-t' in argv:
            _position = None
            if '--token' in argv:
                _position = argv.index('--token')
            elif '-t' in argv:
                _position = argv.index('-t')

            if _position is not None:
                try:
                    if argv[_position + 1].isnumeric():
                        hangoutcore.TOKEN = argv[_position + 1]
                    else:
                        raise TypeError
                except IndexError:
                    await invalid_arg(1)
                except TypeError:
                    await invalid_arg(2)
                else:
                    argv.pop(_position + 1)
                    argv.pop(_position)

        if '--config-app' in argv or '-c-a' in argv:
            _position = None
            if '--config' in argv:
                _position = argv.index('--config')
            elif '-c' in argv:
                _position = argv.index('-c')

            if _position is not None:
                try:
                    hangoutcore.CONFIG_APP_NAME = argv[_position + 1]
                except IndexError:
                    await invalid_arg(1)
                else:
                    argv.pop(_position + 1)
                    argv.pop(_position)

        if '--config-bot' in argv or '-c-b' in argv:
            _position = None
            if '--config' in argv:
                _position = argv.index('--config')
            elif '-c' in argv:
                _position = argv.index('-c')

            if _position is not None:
                try:
                    hangoutcore.CONFIG_BOT_NAME = argv[_position + 1]
                except IndexError:
                    await invalid_arg(1)
                else:
                    argv.pop(_position + 1)
                    argv.pop(_position)

        if '--system-cogs' in argv or '-s-c' in argv:
            _position = None
            if '--system-cogs' in argv:
                _position = argv.index('--system-cogs')
            elif '-s-c' in argv:
                _position = argv.index('-s-c')
                
            if _position is not None:
                try:
                    if argv[_position + 1].lower() == "true":
                        hangoutcore.SYSTEM_COGS = True
                    else:
                        hangoutcore.SYSTEM_COGS = False
                        await invalid_arg(4)
                except IndexError:
                    await invalid_arg(1)
                else:
                    argv.pop(_position + 1)
                    argv.pop(_position)
            
        # Finally, check if we missed any arguments. 
        # If an argument was provided that we missed we handle it and close out the program while warning the user.
        if len(argv) > 0:
            await invalid_arg(0)

        if hangoutcore.INVALID_ARGS:
            if not terminal.confirm(f"You have provided invalid arguments, would you like to continue loading the bot?"):
                sys.exit(0)

    # process arguments in order of priority.
    if len(sys.argv[1:]) > 0:
        await process_arguments(sys.argv[1:])

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # Section Title: Logging setup, Config Setup

    terminal.clear()
    # await terminal.print_header()

    # Locate app config, load bot config based on app config variables
    if await local.appConfig.exists():
        appConfig = await local.appConfig.get()
        if appConfig is not None:
            hangoutcore.CONFIG_APP_NAME = appConfig[0]
            hangoutcore.CONFIG_APP = appConfig[1]
            hangoutcore.CONFIG_BOT_NAME = hangoutcore.CONFIG_APP["botConfig"].data
            hangoutcore.DIRECTORY_CONFIGS = hangoutcore.CONFIG_APP["botConfigDirectory"].data
            hangoutcore.DIRECTORY_COGS = hangoutcore.CONFIG_APP["botCogDirectory"].data
            hangoutcore.DIRECTORY_LOGS = hangoutcore.CONFIG_APP["botLogDirectory"].data
            # load bot config
            if await local.botConfig.exists():
                hangoutcore.CONFIG_BOT = await local.botConfig.get()
                
                if hangoutcore.CONFIG_BOT is not None:
                    if hangoutcore.CONFIG_BOT['_info']['version'] < local.botConfig.CONFIG_VERSION:
                        hangoutcore.CONFIG_BOT_OUTDATED = True
                        terminal.log.WARNING(f"Bot config located at ({Path(hangoutcore.DIRECTORY_CONFIGS).joinpath(hangoutcore.CONFIG_BOT_NAME).absolute()}) is outdated.")
            else:
                # file doesnt exist prompt user to create new one
                pass
        else:
            pass # prompt user to initiate new install or exit
    else:
        print("False")

    logName = fr"{hangoutcore.DIRECTORY_LOGS}/log_{hangoutcore.INIT_TIME.replace(' ', '_').replace(':', '')}.log" # We clear any spaces in our log name to avoid incompatabilities
    date_format = "%m/%d/%Y %I:%M:%S %p"

    fileHandler = logging.FileHandler(
        filename = fr"{hangoutcore.DIRECTORY_LOGS}/log_{hangoutcore.INIT_TIME.replace(' ', '_').replace(':', '')}.log",
        mode = "a",
        encoding = "utf-8",
        delay = False,
        errors = None
    )
    consoleHandler = logging.StreamHandler()

    logFormatter = logging.Formatter("""[%(asctime)s][%(name)s][%(levelname)s] %(message)s""", date_format)
    fileHandler.setFormatter(logFormatter)
    consoleHandler.setFormatter(logFormatter)
    
    # hangoutcore.loggerRoot.addHandler(fileHandler)
    hangoutcore.loggerDiscord.addHandler(fileHandler)
    hangoutcore.loggerHangoutCore.addHandler(fileHandler)
    
    # hangoutcore.loggerDiscord.addHandler(consoleHandler)
    # hangoutcore.loggerHangoutCore.addHandler(consoleHandler)
    
    logFiles = os.listdir(hangoutcore.DIRECTORY_LOGS)
    
    # Sort log files by date and trim to max of 5
    while len(logFiles) > 5:
        logFiles = os.listdir(hangoutcore.DIRECTORY_LOGS)
        oldest_file = sorted([ f"{hangoutcore.DIRECTORY_LOGS}/{f}" for f in os.listdir(hangoutcore.DIRECTORY_LOGS)], key=os.path.getctime)[0]

        if len(logFiles) > 5:
            os.remove(oldest_file)
        else:
            break

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # Section Title: Logger Setup

    # Logging Levels(
        # 0 : NOTSET,
        # 10 : DEBUG,
        # 20 : INFO,
        # 30 : WARNING,
        # 40 : ERROR,
        # 50 : CRITICAL)

    if hangoutcore.DEBUG:
        terminal.log.DEBUG(f"Debug Mode!")
        hangoutcore.loggerDiscord.setLevel(logging.DEBUG)
        hangoutcore.loggerHangoutCore.setLevel(logging.DEBUG)
    else:
        hangoutcore.loggerDiscord.setLevel(logging.INFO)
        hangoutcore.loggerHangoutCore.setLevel(logging.INFO)
        
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # Section Title: Main

    if not hangoutcore.SILENT:
        terminal.print_hr()
        terminal.print_center(" ")

        terminal.print_logo()

        if await local.is_latest("discord"):
            _discord_version = f"Discord.py Version [green]{discord.__version__}"
        else:
            _discord_version = f"[red reverse]Discord.py Version {discord.__version__} (Outdated)"

        if await local.is_latest("hangoutcore"):
            _hangoutcore_version = f"HangoutCore Version [green]{hangoutcore.__version__}"
        else:
            _hangoutcore_version = f"[red reverse]HangoutCore Version {hangoutcore.__version__} (Outdated)"

        if hangoutcore.CONFIG_BOT_OUTDATED:
            _configOutdated = f"[red reverse]Bot Config Version: {hangoutcore.CONFIG_BOT['_info']['version']} (Outdated)"
        else:
            _configOutdated = f"Bot Config Version:  [green]{hangoutcore.CONFIG_BOT['_info']['version']}"
        
        if hangoutcore.DEBUG:
            if hangoutcore.CONFIG_BOT is not None:
                console.print(
                    Panel(
                        title = r"[red reverse]// Debug Mode Enabled \\\\[/red reverse] ", # Why I need 4 /'s is beyond me. I'll keep messing with this later but for now it works.
                        subtitle =  '{0:%d%b%Y %Hh:%Mm}'.format(datetime.now()),
                        renderable = Group(
                            "",
                            f"Bot Name: [b]{hangoutcore.CONFIG_BOT['bot']['name']}[/b]",
                            f"Bot Version: [green]{hangoutcore.CONFIG_BOT['bot']['version']}",
                            _configOutdated,
                            f"SYS Version [green]{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
                            f"API Version [green]{sys.api_version}",
                            f"{_discord_version}",
                            f"{_hangoutcore_version}",
                            ""
                        ),
                        style = f"red on {terminal.colorBG}"
                    )
                )
        else:
            if hangoutcore.CONFIG_BOT is not None:
                console.print(
                    Panel(
                        subtitle= '{0:%d%b%Y %Hh:%Mm}'.format(datetime.now()),
                        renderable = Group(
                            f"Bot Name: [b]{hangoutcore.CONFIG_BOT['bot']['name']}[/b]",
                            f"Bot Version: [green]{hangoutcore.CONFIG_BOT['bot']['version']}",
                            f"{_discord_version}",
                            f"{_hangoutcore_version}",
                            ""
                        )
                    ), 
                    style=f"on {terminal.colorBG}", 
                    justify="center"
                )
        
        terminal.print_hr(title="Pre-Load Output")
    else:
        terminal.log.DEBUG(f"Running in Silent Mode!")
    
    terminal.log.DEBUG(f"Fresh Install: {hangoutcore.FRESH_INSTALL}")
    terminal.log.DEBUG(f"Silent: {hangoutcore.SILENT}")
    terminal.log.DEBUG(f"Debug: {hangoutcore.DEBUG}")
    terminal.log.DEBUG(f"Token: {hangoutcore.TOKEN}")
    terminal.log.DEBUG(f"App Config Name: {hangoutcore.CONFIG_APP_NAME}")
    terminal.log.DEBUG(f"App Config: {type(hangoutcore.CONFIG_APP)}")
    if hangoutcore.CONFIG_BOT_OUTDATED:
        terminal.log.DEBUG(f"Warning: Bot Config Is Outdated")
    terminal.log.DEBUG(f"Bot Config Name: {hangoutcore.CONFIG_BOT_NAME}")
    terminal.log.DEBUG(f"Bot Config: {type(hangoutcore.CONFIG_BOT)}")
    terminal.log.DEBUG(f"Bot Config Directory: {hangoutcore.DIRECTORY_CONFIGS}")
    terminal.log.DEBUG(f"Bot Cog Directory: {hangoutcore.DIRECTORY_COGS}")
    terminal.log.DEBUG(f"Bot Log Directory: {hangoutcore.DIRECTORY_LOGS}")
    
    terminal.log.DEBUG(f"Bot Using System Cogs: {hangoutcore.SYSTEM_COGS}")

    if hangoutcore.CONFIG_BOT is not None:
        configTokens = hangoutcore.CONFIG_BOT["bot"]["token"]
        botToken = ""

        if type(configTokens) == str:
            terminal.log.DEBUG(f"Token entry in config file is a string.")
            botToken = configTokens
        elif type(configTokens) == list:
            terminal.log.DEBUG(f"Token entry in config file is a list.")
            if hangoutcore.TOKEN == -1:
                if hangoutcore.SILENT or len(configTokens) == 1:
                    terminal.log.DEBUG(f"Found 1 token or silent mode is enabled. Using Token 0.")
                    botToken = configTokens[0] # Default to the first token
                else:
                    filteredTokens = []
                    for token in configTokens:
                        filteredTokens.append(terminal.obfuscateString(token, 6, '*'))
                    
                    terminal.log.INFO(f"Tokens listed in {hangoutcore.CONFIG_BOT_NAME}:")

                    for i, token in enumerate(filteredTokens):
                        console.print(f"[{i}] [green]{token}")
                    while True:
                        desiredToken = IntPrompt.ask("Which token would you like to use?")
                        if (desiredToken + 1) > len(filteredTokens):
                            terminal.log.ERROR(f"The Integer you've provided is out of range.")
                            # raise InvalidResponse(f"The integer you've provided is out of limits.")
                            continue
                        else:
                            if Confirm.ask(f"Are you sure you'd like to use token: {desiredToken}"):
                                break
                            else:
                                continue

                    botToken = configTokens[desiredToken]
            else:
                botToken = configTokens[int(hangoutcore.TOKEN)]

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        # Section Title: Launch Bot
        async def getBotActivity() -> discord.Activity:
            """
            Retrieves Bot Activity specified in our loaded bot config. Returns activity type 'listening' if none is found.
            """
            if hangoutcore.CONFIG_BOT is not None: # make sure our config exists in the first place
                terminal.log.DEBUG(f"Found Config Activity Type Entry: {hangoutcore.CONFIG_BOT['bot']['status']['type']}")
                if hangoutcore.CONFIG_BOT['bot']['status']['type'] == 'listening':
                    return discord.Activity(
                        type = discord.ActivityType.listening,
                        name = hangoutcore.CONFIG_BOT['bot']['status']['name']
                    )
                if hangoutcore.CONFIG_BOT['bot']['status']['type'] == 'streaming':
                    return discord.Activity(
                        type = discord.ActivityType.streaming,
                        name = hangoutcore.CONFIG_BOT['bot']['status']['name'],
                        game = hangoutcore.CONFIG_BOT['bot']['status']['url']
                    )
                if hangoutcore.CONFIG_BOT['bot']['status']['type'] == 'watching':
                    return discord.Activity(
                        type = discord.ActivityType.watching,
                        name = hangoutcore.CONFIG_BOT['bot']['status']['name']
                    )
                if hangoutcore.CONFIG_BOT['bot']['status']['type'] == 'playing':
                    return discord.Activity(
                        type = discord.ActivityType.playing,
                        name = hangoutcore.CONFIG_BOT['bot']['status']['name'],
                        game = hangoutcore.CONFIG_BOT['bot']['status']['game']
                    )
                # Assume that we got here because the entry in our config either doesn't exists, or is simply not one of the above.
                terminal.log.ERROR(f"Config Activity Type Entry: {hangoutcore.CONFIG_BOT['bot']['status']['type']} is not valid. Please check your spelling and try again.")
                return discord.Activity(
                    type = discord.ActivityType.listening,
                    name= "!help"
                )
            else:
                terminal.log.DEBUG(f"Config is None. Returning Activity Type: 'listening'")
                return discord.Activity(
                    type = discord.ActivityType.listening,
                    name= "!help"
                )

        async def getBotIntents():
            """Retrieves specified bot intents from config file. If the config file is not able to be loaded this sets intents to False just in case."""
            if hangoutcore.CONFIG_BOT is not None:
                # terminal.log.DEBUG(f"Loading Bot Intents from config. Intents: {str(hangoutcore.CONFIG_BOT['bot']['intents']).replace(',', _tmp)}")
                terminal.log.DEBUG(f"Loading Bot Intents from config.")
                terminal.log.DEBUG(str(hangoutcore.CONFIG_BOT['bot']['intents']).replace(',', ',\n').replace('{', '{ ').replace('}', ' }'))
                intents = discord.Intents.default()  # Set Bot Intents
                intents.members         = hangoutcore.CONFIG_BOT['bot']['intents']['members']
                intents.message_content = hangoutcore.CONFIG_BOT['bot']['intents']['message_content']
                intents.typing          = hangoutcore.CONFIG_BOT['bot']['intents']['typing']
                intents.presences       = hangoutcore.CONFIG_BOT['bot']['intents']['presences']
                intents.guilds          = hangoutcore.CONFIG_BOT['bot']['intents']['guilds']
                return intents
            else:
                terminal.log.WARNING(f"Could not retrieve intents from Config(). Setting intents to False as a precaution.")
                intents = discord.Intents.default()  # Set Bot Intents
                intents.members = False
                intents.message_content = False
                intents.typing = False
                intents.presences = False
                intents.guilds = False
                return intents

        async def getBotPrefix(): # Since we're moving to slash commands this will eventually get removed.
            if hangoutcore.CONFIG_BOT is not None:
                if hangoutcore.CONFIG_BOT['bot']['prefixes'] is not None:
                    if type(hangoutcore.CONFIG_BOT['bot']['prefixes']) == str:
                        return list(hangoutcore.CONFIG_BOT['bot']['prefixes'])
                    else:
                        return hangoutcore.CONFIG_BOT['bot']['prefixes']
                else:
                    return ['!']

        async with ClientSession() as our_client:
            _activity = await getBotActivity()
            _intents = await getBotIntents()
            _prefixes = await getBotPrefix() # Legacy
            _db_type = str(hangoutcore.CONFIG_BOT['database']['type'])
            
            _DeveloperGuild_ID = None
            if type(hangoutcore.CONFIG_BOT['bot']['developer_guild_id']) is None and hangoutcore.CONFIG_BOT['bot']['developer_guild_id'] != 0:
                _DeveloperGuild_ID = hangoutcore.CONFIG_BOT['bot']['developer_guild_id']
            
            terminal.log.DEBUG(f"Database Type: {_db_type}")
            if _db_type.lower() == "mysql": # mysql section
                if hangoutcore.CONFIG_BOT["database"]["host"] is not None:
                    try:
                        terminal.log.INFO(f"{_db_type}: Attempting to connect to server.")
                        
                        terminal.log.DEBUG(f"Database Name: {hangoutcore.CONFIG_BOT['database']['name']}")
                        terminal.log.DEBUG(f"Database Host: {hangoutcore.CONFIG_BOT['database']['host']}")
                        terminal.log.DEBUG(f"Database Port: {hangoutcore.CONFIG_BOT['database']['port']}")
                        terminal.log.DEBUG(f"Database User: {hangoutcore.CONFIG_BOT['database']['user']}")
                        terminal.log.DEBUG(f"Database Password: {terminal.obfuscateString(hangoutcore.CONFIG_BOT['database']['password'], 0, '*')}")
                        
                        _Temp_Pool = await aiomysql.create_pool(
                                db       = hangoutcore.CONFIG_BOT["database"]["name"],
                                host     = hangoutcore.CONFIG_BOT["database"]["host"],
                                port     = hangoutcore.CONFIG_BOT["database"]["port"],
                                user     = hangoutcore.CONFIG_BOT["database"]["user"],
                                password = hangoutcore.CONFIG_BOT["database"]["password"]
                            )
                    except aiomysql.MySQLError as err:
                        terminal.log.ERROR(f"{_db_type}: {err.args[1]} | Error No. {err.args[0]}")
                        terminal.log.DEBUG(f"Continuing with no database")
                    else:
                        terminal.log.INFO(f"Successfully connected to: {hangoutcore.CONFIG_BOT['database']['host']}:{hangoutcore.CONFIG_BOT['database']['port']} with user: {hangoutcore.CONFIG_BOT['database']['user']}")
                        hangoutcore.DB_POOL = _Temp_Pool
                else:
                    terminal.log.ERROR(f"{_db_type}: Database Config Invalid. Please check your bot config.")
                    terminal.log.WARNING(f"{_db_type}: Skipping...")
            # elif db_type.lower() == "sql":
            else:
                terminal.log.ERROR(f"Database Type Invalid. Please check config.\nIf you believe this is wrong please check/update '__main__.py'")
            async with HangoutCoreBot(
                commands.when_mentioned,
                intents = _intents,
                activity = _activity,
                web_client = our_client,
                db_pool = hangoutcore.DB_POOL,
                init_time = hangoutcore.INIT_TIME,
                DeveloperGuild_ID = _DeveloperGuild_ID
            ) as HangoutCore:
                hangoutcore.bot = HangoutCore
                await HangoutCore.start(botToken)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Section Title: Main Function Loading

from textual import events
from textual.app import App, ComposeResult
from textual.widgets import Label, Button, RichLog, Log, LoadingIndicator
# TEXT = """I must not fear.
# Fear is the mind-killer.
# Fear is the little-death that brings total obliteration.
# I will face my fear.
# I will permit it to pass over me and through me.
# And when it has gone past, I will turn the inner eye to see its path.
# Where the fear has gone there will be nothing. Only I will remain."""
# class hangoutcoreApp(App):
#     """App to display key events."""

#     def compose(self) -> ComposeResult:
#         yield LoadingIndicator()
#         yield RichLog()
    
#     def on_ready(self) -> None:
#         self.query_one(LoadingIndicator).display = False
#         log = self.query_one(RichLog)
#         log.write("Hello, World!")
#         for _ in range(10):
#             log.write(TEXT)
            
#     def on_key(self, event: events.Key) -> None:
#         self.query_one(RichLog).write(event.key)

def init():
    try:
        asyncio.run(main())
        # app = HangoutCoreApp()
        # app.run()
    except KeyboardInterrupt:
        try:
            terminal.log.WARNING(f"Please refrain from using CTRL+C to shutdown bot.")
            # Here we'd make sure database exited/saved gracefully as well as any other essential process that may suffer from stopping abruptly.
            # terminal.log.INFO(f"Saving...")
            # terminal.console.save_svg(path = Path("test.svg").absolute())
            terminal.EXIT(f"Shutting Down...")
        except:
            pass
    except SystemExit:
        try:
            terminal.EXIT(f"Exiting...")
        except:
            pass

if __name__ == "__main__":
    init()