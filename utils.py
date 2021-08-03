"""
    Utility Module for HangoutCore
    › Please do not modify any of the following content unless you know what you're doing. Modifying the following code and not updating the rest of the bot code to match can/will cause issues.
    › If you do decide to modify the following code please understand that HangoutCore's Dev team, Discord.py's Dev Team nor Python's Dev team are obligated to help you.
    › By Modifying the following code you acknowledge and agree to the text above.
    Module Last Updated: August 3rd, 2021
    Module Last Updated by: Lino
    Notes:
        None
"""

import aiofiles
import discord
import json
import logging
import os, sys
import shutil
import sqlite3
import traceback

from asyncio import sleep
from colorama import *
from discord.ext import commands
from os import system, name

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ↓ Terminal ↓ : WIP
#   › Used for clearing/setting up terminal as well as logging.
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class terminal():
    log_Q = []
    def __init__(self):
        pass
   
    def print_center(s):
        print(s.center(shutil.get_terminal_size().columns))

    def print_hr():
        print('━'.center(shutil.get_terminal_size().columns, '━'))

    def clear():
        if name =='nt':
            _ = system('cls')    
        else: 
            _ = system('clear')

    def initiate(start_time, debug:bool=False):
        terminal.clear()
        if debug:
            print(Style.BRIGHT + Back.RED,end="\r")
        else:
            print(Style.NORMAL + Fore.BLACK + Back.WHITE,end="\r")
        terminal.print_center(str(cfg["bot"]["name"]))
        terminal.print_center(str(cfg["bot"]["version"]))
        terminal.print_center(str(start_time))
        if debug:
            terminal.print_center(f'// Debug Mode Enabled \\\ ')
            terminal.print_center('SYS Version ' + str(sys.version))
            terminal.print_center('API Version ' + str(sys.api_version))
            terminal.print_center('Discord Version ' + str(discord.__version__))
        print(Style.RESET_ALL + Back.RESET,end="\r")
        terminal.print_hr()

    def refresh(start_time, debug:bool=False):
        terminal.clear()
        if debug:
            print(Style.BRIGHT + Back.RED,end="\r")
        else:
            print(Style.NORMAL + Fore.BLACK + Back.WHITE,end="\r")
        terminal.print_center(str(cfg["bot"]["name"]))
        terminal.print_center(str(cfg["bot"]["version"]))
        terminal.print_center(str(start_time))
        if debug:
            terminal.print_center(f'// Debug Mode Enabled \\\ ')
            terminal.print_center('SYS Version ' + str(sys.version))
            terminal.print_center('API Version ' + str(sys.api_version))
            terminal.print_center('Discord Version ' + str(discord.__version__))
        print(Style.RESET_ALL + Back.RESET,end="\r")
        terminal.print_hr()

    def log(level:str, log):                                                                                                        # More Logging functionality
        if level == "DEBUG":                                                                                                        #
            logging.debug(log)                                                                                                      #
            print(f"[{Fore.BLUE}DEBUG{Fore.RESET}] {log}")                                                                          #

        if level == "INFO":                                                                                                         #
            logging.info(log)                                                                                                       #
            print(f"[{Fore.GREEN}INFO{Fore.RESET}] {log}")                                                                          #

        if level == "WARNING":                                                                                                      #
            logging.warning(log)                                                                                                    #
            print(f"[{Fore.YELLOW}WARNING{Fore.RESET}] {log}")                                                                      #
            
        if level == "ERROR":                                                                                                        #
            logging.error(log)                                                                                                      #
            print(f"[{Fore.RED}ERROR{Fore.RESET}] {log}")                                                                           #

        if level == "CRITICAL":                                                                                                     #
            logging.critical(log)                                                                                                   #
            print(f"{Style.BRIGHT}{Back.RED}[CRITICAL] {log}{Style.RESET_ALL}{Back.RESET}") 

    def queue(level:str, log):
        terminal.log_Q.append([level,log])
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ↓ Config ↓ : WIP
#   › Handles bot config loading, writing as well as the initial creation of config.json.
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class config():
    warned = False
    CONFIG_PATH = 'config.json' # Path and name of config file.
    CONFIG_VERSION = 3.3
    COG_DIRECTORY_PATH = "cogs" # Name of directory where cogs will be stored.
    LOG_DIRECTORY_PATH = "logs" # Name of directory where log files will be stored.
    CONFIG_PATH = "config.json" # Name of config file.
    EXAMPLE_CONFIG = { # Changing this will only matter when the bot creates a new config. Actual config at CONFIG_PATH
        "bot" : {
            "prefixes" : ["!"], #Bot uses this array for prefixes. Add as many as you want, and keep in mind you can include spaces but be careful not to over complicate your prefixes.
            "token" : [""], # If you intend on using any token other than the first in the list, change hangoutcore.py to match.
            "status" : {
                "type" : "listening", # Valid Options are competing, playing, listening, streaming, watching
                "name" : "!help", # Activity Name
                "url" : "" # Twitch or Youtube URL if type is Streaming
            },
            "name" : "Bot Name", # Bot name
            "version" : "0.0.0", # Bot version
            "description" : "Bot Description would go here.",
            "developer_guild_id" : 000000000, # Developer guild id for bot. Used for test commands.
            "contributers" : [
                {
                    "name":"Contributer Name", # Contributer name
                    "discord_id": 000000000, # Contributer discord id
                    "owner" : True # Set this to true if they're an owner. otherwise set it to false
                },
                {
                    "name":"Contributer Name",
                    "discord_id": 000000000,
                    "owner" : False
                }
                ],
            "apis" : [
                {
                    "name" : "Api Name", # API Name for display sake
                    "token" : "Api Token", # API Token for accessing API Data
                    "header" : {"Authorization": ""} # API Header for ease of use
                }
            ]
        },
        "database" : {
            "name" : "database.sqlite", # db name
            "user" : "user",
            "password" : "pass"
        },
        "music" : {
            "max_volume" : 250, # Max Volume
            "vote_skip" : True, # whether vote skip is enabled or not.
            "vote_skip_ratio" : 0.5 # minimum ratio needed for vote skip
        },
        "_info" : { # config info
            "version" : CONFIG_VERSION # config version
        }
    }

    def __init__(self):
        pass
    
    def load(path=CONFIG_PATH):
        """
        Attempt to load the config from path provided if none provided use CONFIG_PATH,
        if one does not exist then create a new file at CONFIG_PATH and
        copy EXAMPLE_CONFIG into it.
        """
        if os.path.exists(path) and os.path.isfile(path):
            with open(path) as file:
                cfg = json.load(file)
                if '_info' in cfg:
                    if cfg['_info']['version'] >= config.CONFIG_VERSION:
                        return cfg
                    else:
                        if not config.warned: # Config is outdated
                            config.warned = True
                            terminal.queue("WARNING",f"{config.CONFIG_PATH} is outdated. Please update it to match the example config provided in config.py")
                        return cfg
                else:
                    if not config.warned: # Couldn't Find version, file probably outdated or corrupted.
                        config.warned = True
                        terminal.queue("WARNING",f"{config.CONFIG_PATH} is either outdated or corrupt. Please delete the old one and run the bot again to create a new one.")
                    return cfg
        else: #file doesn't exist, create new one.
            terminal.log("CRITICAL", f"Config could not be found. Creating a new one.")
            with open(path, 'w') as file:
                json.dump(config.EXAMPLE_CONFIG, file, indent=4)
                
            if not os.path.exists(config.COG_DIRECTORY_PATH):
                os.mkdir(config.COG_DIRECTORY_PATH)
            if not os.path.exists(config.LOG_DIRECTORY_PATH):
                os.mkdir(config.LOG_DIRECTORY_PATH)
            return config.load(path=path)

    def write(self, path=CONFIG_PATH):
        """
        Attempt to write to the config from path provided if none provided use CONFIG_PATH,
        if one does not exist we warn the terminal. We do not create one in the possibility that
        the user misspelled the path provided.
        """
        pass

cfg = config.load()

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ↓ Bot ↓ : WIP
#   › Fill with functions as you need, intended to keep other files clear and let utils do the heavy lifting.
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class bot():
    def __init__(self):
        pass
    
    def GetIntents():
        intents = discord.Intents.default() # Set Bot Intents
        intents.members = True  
        intents.typing = True
        intents.presences = True
        intents.guilds = True
        return intents

    def GetActivity():
        if cfg["bot"]["status"]["type"] == "listening": # Set the activity depending on config
            activity = discord.Activity(
                type=discord.ActivityType.listening,
                name=cfg["bot"]["status"]["name"]
                )
        elif cfg["bot"]["status"]["type"] == "streaming":
            activity = discord.Activity(
                type=discord.ActivityType.streaming,
                name=cfg["bot"]["status"]["name"],
                url=cfg["bot"]["status"]["url"]
                )
        elif cfg["bot"]["status"]["type"] == "watching":
            activity = discord.Activity(
                type=discord.ActivityType.watching,
                name=cfg["bot"]["status"]["name"]
                )
        elif cfg["bot"]["status"]["type"] == "playing":
            activity = discord.Activity(
                type=discord.ActivityType.playing,
                name=cfg["bot"]["status"]["name"],
                game=cfg["bot"]["status"]["game"]
                )
        return activity

    def GetPrefix(bot, message):
        prefixes = cfg["bot"]["prefixes"]

        # Check to see if we are outside of a guild. e.g DM's etc.
        if not message.guild or prefixes is None:
            # Only allow ! to be used in DMs or if no prefix is specified.
            return '!'

        return commands.when_mentioned_or(*prefixes)(bot, message)
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ↓ Local ↓ : WIP
#   › Handles providing local files such as images, video, cogs, py files, etc.
#   › Fill with functions as you need, intended to keep other files clear and let utils do the heavy lifting.
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class local():
    def __init__(self):
        pass

    def GetCogs():
        valid_files = []
        disabled_files = []
        invalid_files = []
        for file in os.listdir(config.COG_DIRECTORY_PATH):
            if file.endswith('.py'):
                valid_files.append(file)
            elif file.endswith('.disabled'):
                disabled_files.append(file)
            else:
                if file == "__pycache__" or "__init__":
                    pass
                else:
                    invalid_files.append(file)
        package = {
            "valid_files": valid_files,
            "invalid_files": invalid_files,
            "disabled_files": disabled_files
        }
        return package

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ↓ Custom Error Processing ↓ : WIP
#   › Intended for when you only need specific data from an error.
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class errorprocessing():
    def __init__(self):
        pass

    def CogLoadError(file, error, debug_mode):
        """ Error Processing tailored to display the specific error when loading a cog, 
            designed to minimise clutter and lines not relevant."""
        ErrorTraceback = traceback.format_exception(type(error), error, error.__traceback__)
        if debug_mode:
            terminal.log("ERROR", f"  └ Failed to load {file}\n" + "".join(ErrorTraceback))
        else:
            
            terminal.log("ERROR", f"""  └ Failed to load {file}.
            {Back.RED}{error}{Back.RESET}""")

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ↓ Guild Audio State ↓ : WIP
#   › Used during music/audio commands
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class guildstate():
    def __init__(self):
        self.now_playing = None
        self.playlist = []
        self.skip_votes = set()
        self.volume = 1.0 # volume is config max_volume / 100

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ↓ Database Handling ↓ : WIP
#   › Used to create/modify databases for guilds/users
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class database():
    def __init__(self):
        pass

    def GuildRegistered(guild_id):
        pass
