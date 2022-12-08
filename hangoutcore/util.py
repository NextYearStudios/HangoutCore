"""
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    Utility Module for HangoutCore
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

import asyncio
import aiofiles
import aiomysql  # Async MYSQL
import click
import ctypes
import discord
import json
import pymysql.cursors
import os, sys
import shutil
import traceback
import requests

from getpass import getpass
from asyncio import sleep
from colorama import *
from datetime import datetime
from discord.ext import commands
from jproperties import Properties
from typing import Optional
from os import system, name


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ↓ Bot ↓ : WIP
#   › Fill with functions as you need, intended to keep other files clear and let utils do the heavy lifting.
#   › Author: Lino
#   › Date: 15 Nov, 2022
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class Bot():
    def GetIntents(self):
        """Retrieves specified bot intents from config file. If the config file is not able to be loaded this sets intents to false just in case."""
        cfg = Config().load()
        if cfg is not None:
            intents = discord.Intents.default()  # Set Bot Intents
            intents.members = cfg['bot']['intents']['members']
            intents.message_content = cfg['bot']['intents']['message_content']
            intents.typing = cfg['bot']['intents']['typing']
            intents.presences = cfg['bot']['intents']['presences']
            intents.guilds = cfg['bot']['intents']['guilds']
            return intents
        else:
            Terminal().Log().WARNING(f"Could not retrieve intents from Config(). Setting intents to false as a precaution.")
            intents = discord.Intents.default()  # Set Bot Intents
            intents.members = False
            intents.message_content = False
            intents.typing = False
            intents.presences = False
            intents.guilds = False
            return intents

    def GetActivity(self):
        """Retrieves Bot Activity specified in config file. If an activity cannot be loaded from the config then we set it to 'listening to !help'"""
        cfg = Config().load()
        if cfg is not None:
            if cfg["bot"]["status"]["type"] == "listening":  # Set the activity depending on config
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
        else:
            activity = discord.Activity(
                type=discord.ActivityType.listening,
                name="!help"
            )
        return activity

    def GetPrefix(discordBot, message: discord.message):
        """Returns the prefixes specified in the config file. If none can be loaded from config then we set prefix as '!'"""
        cfg = Config().load()
        if cfg is not None:
            prefixes = cfg["bot"]["prefixes"]

            if prefixes is None:
                return '!'
            return commands.when_mentioned_or(prefixes[0])(Bot, message)

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # ↓ Audio Handling ↓ : WIP
    #   › Used for playing music and keeping the audio function clutter out of the main script.
    #   › Author: Lino
    #   › Date: 15 Nov, 2022
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    class audio():
        class guildstate():
            def __init__(self):
                self.now_playing = None
                self.playlist = []
                self.skip_votes = set()
                self.volume = int(Config().load()["music"]["max_volume"]) / 100

        def verify_opus(self):
            """
                Looks for opus throughout the system, Attempts to load if found.
            """
            terminal = Terminal()
            opuslib = ctypes.util.find_library('opus')
            if opuslib is not None:
                try:
                    terminal.Log().INFO(f"Loading Opus.")
                    discord.opus.load_opus('opus')
                except Exception as e:
                    terminal.Log().ERROR(e)
                else:
                    if not discord.opus.is_loaded():
                        terminal.Log().CRITICAL("Opus Failed To Load.")
                    else:
                        terminal.Log().INFO("Successfully loaded opus.")
            else:
                terminal.Log().WARNING("Could not find Opus, You will not be able to play audio without it.")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ↓ Config ↓ : WIP
#   › Used for handling bot configuration file.
#   › Author: Lino
#   › Date: 15 Nov, 2022
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class Config():

    def __init__(self):
        self.WARNED = False
        self.CONFIG = None
        self.CONFIG_VERSION = 5.8
        self.CONFIG_PATH = 'configold.json'  # Path and name of config file.
        self.CONFIG_DIRECTORY_PATH = "configs"  # Name of directory where cogs will be stored.
        self.COG_DIRECTORY_PATH = "cogs"  # Name of directory where cogs will be stored.
        self.LOG_DIRECTORY_PATH = "logs"  # Name of directory where log files will be stored.
        self.EXAMPLE_CONFIG = {  # Changing this will only matter when the bot creates a new Config(). Actual config at CONFIG_PATH
            "bot": {
                "prefixes": ["!"],
                # Bot uses this array for prefixes. Add as many as you want, and keep in mind you can include spaces but be careful not to over complicate your prefixes.
                "token": [""],
                # If you intend on using any token other than the first in the list, change hangoutcore.py to match.
                "intents": {
                    "members": True,
                    "message_content": True,
                    "typing": True,
                    "presences": True,
                    "guilds": True
                },
                "status": {
                    "type": "listening",  # Valid Options are competing, playing, listening, streaming, watching
                    "name": "!help",  # Activity Name
                    "url": ""  # Twitch or Youtube URL if type is Streaming
                },
                "name": "Bot Name",  # Bot name
                "version": "0.0.0",  # Bot version
                "description": "Bot Description would go here.",
                "developer_guild_id": 000000000,  # Developer guild id for  Used for test commands.
                "contributers": [
                    {
                        "name": "Contributer Name",  # Contributer name
                        "discord_id": 000000000,  # Contributer discord id
                        "owner": True  # Set this to true if they're an owner. otherwise set it to false
                    },
                    {
                        "name": "Contributer Name",
                        "discord_id": 000000000,
                        "owner": False
                    }
                ],
                "apis": [
                    {
                        "name": "Api Name",  # API Name for display sake
                        "token": "Api Token",  # API Token for accessing API Data
                        "header": {"Authorization": ""}  # API Header for ease of use
                    }
                ],
                "messages": {
                    # The following section is for specifying various messages the bot will use. 
                    # Instead of having to specify each one in various areas of code it's centralized here so that duplicate situations can easily use the necessary message without having to specify it in multiple areas.
                    # messages with '_user_' in the name are often public messages that get displayed in the channel the command was called in.
                    # messages with '_user_dm_' in the name are private messages that get sent straight to a user's dm. Such as moderation notices, etc. 
                    # messages with '_bot_' in the name are bot specific such as not having necessary roles, etc. This message get's publicly displayed.
                    # messages with neither of the above are private and go to staff logs. Provide information here that you believe is important for guild staff members to know.
                    # Valid references
                    # {user.name} # Target user's name
                    # {user.mention} # Target user's mention
                    # {author.name} # Command author's name
                    # {author.mention} # Command author's mention
                    # {bot.name} # Bot name specified in config file
                    # {bot.mention} # Bot mention (Keep in mind guilds may nickname your bot, This will display whatever they have set.)
                    # {channel} # Channel mention
                    # {command} # Command used
                    # {argument_name} # This can vary depending on the code that uses it. eg; {reason}, {color_chosen}, etc.
                    # {error} # Error encountered
                    "error_user_insufficientpermissions": "You do not have the necessary permissions to use that. This event has been logged and a staff member has been notified.",
                    "error_bot_insufficientpermissions": "I do not have the necessary permissions to perform {command}, Please insure I have the necessary permissions assigned to my role.",
                    "error_insufficientpermissions": "{user.mention} attempted to use {command} in channel {channel}.",
                    "error_user_warn": "{user.mention} has been warned for the following reason: {reason}.",
                    "error_user_dm_warn": "You have been warned for the following reason: {reason}.",
                    "error_warn": "{user.mention} has been warned by {author.mention} for the following reason: {reason}.",
                    "error_user_channelnotjoinable": "I could not join your channel. Please make sure there is space and verify I have the necessary permissions.",
                    "error_user_notinchannel": "You're not currently in a voice channel. Please join a valid voice channel and try again.",
                    "error_user_alreadyconnected": "I'm already connected to a voice channel.",
                    "error_user_channelnotfound": "I could not find the channel specified, please check the spelling and try again.",
                }
            },
            "database": {
                "type": "mysql",
                "host": "localhost",
                "port": 3306,
                "name": "database",  # db name
                "user": "user",
                "password": "pass"
            },
            "music": {
                "vc_timeout": True,
                "vc_timeout_duration": 600,
                "max_volume": 250,  # Max Volume
                "vote_skip": True,  # whether vote skip is enabled or not.
                "vote_skip_ratio": 0.5  # minimum ratio needed for vote skip
            },
            "_info": {  # config info
                "version": self.CONFIG_VERSION,  # config version
                "update_reason": "Initial Creation"
            }
        }

    # def exists(configName: str = None):
    #     if configName is None:
    #         if os.path.exists("hangoutcore.properties") and os.path.isfile("hangoutcore.properties"):
    #             with open("hangoutcore.properties",
    #                       "r+b") as hangoutcore_config:  # Access stored variables to locate config file
    #                 p = Properties()
    #                 p.load(hangoutcore_config, "utf-8")
    #                 botConfig = p.get("botConfig").data
    #                 botConfigDirectory = p.get("botConfigDirectory").data
    #                 Config().CONFIG_PATH = botConfig
    #                 Config().CONFIG_DIRECTORY_PATH = botConfigDirectory
    #                 Config().COG_DIRECTORY_PATH = p.get("botCogDirectory").data
    #                 Config().LOG_DIRECTORY_PATH = p.get("botLogDirectory").data
    #                 if os.path.exists(f"{botConfigDirectory}/{botConfig}") and os.path.isfile(
    #                         f"{botConfigDirectory}/{botConfig}"):
    #                     return True
    #                 else:
    #                     return False
    #         else:
    #             return False
    #     else:
    #         filePath = configName
    #         if not filePath.endswith('.json'):
    #             filePath = filePath + '.json'
    #         if os.path.exists(f"{Config().CONFIG_DIRECTORY_PATH}/{filePath}") and os.path.isfile(
    #                 f"{Config().CONFIG_DIRECTORY_PATH}/{filePath}"):
    #             return True
    #         else:
    #             return False
            
    def appConfigExists(self, DesiredName: str= None):
        ConfigName = "hangoutcore.properties"
        if DesiredName is not None:
            ConfigName = DesiredName
        
        if ".properties" not in ConfigName:
            ConfigName = ConfigName + ".properties"

        if os.path.exists(ConfigName) and os.path.isfile(ConfigName):
            return True
        else:
            return False
            
    def botConfigExists(self, DesiredName: str= None):
        ConfigDirectory = self.CONFIG_DIRECTORY_PATH
        ConfigName = self.CONFIG_PATH
        if DesiredName is not None:
            ConfigName = DesiredName
        
        if ".json" not in ConfigName:
            ConfigName = ConfigName + ".json"

        if os.path.exists(f"{ConfigDirectory}/{ConfigName}") and os.path.isfile(f"{ConfigDirectory}/{ConfigName}"):
            return True
        else:
            return False

    def setConfigPath(self, configPath: str):
        if configPath is not None:
            if configPath.endswith(".json"):
                self.CONFIG_PATH = configPath
    
    def getConfigPath(self):
        return self.CONFIG_PATH

    def setConfigDirectoryPath(self, configDirectoryPath: str):
        if configDirectoryPath is not None:
            self.CONFIG_DIRECTORY_PATH = configDirectoryPath
    
    def getConfigDirectoryPath(self):
        return self.CONFIG_DIRECTORY_PATH
    
    def setCogDirectoryPath(self, cogDirectoryPath: str):
        if cogDirectoryPath is not None:
            self.COG_DIRECTORY_PATH = cogDirectoryPath
    
    def getCogDirectoryPath(self):
        return self.COG_DIRECTORY_PATH
    
    def setLogDirectoryPath(self, logDirectoryPath: str):
        if logDirectoryPath is not None:
            self.LOG_DIRECTORY_PATH = logDirectoryPath
    
    def getLogDirectoryPath(self):
        return self.LOG_DIRECTORY_PATH
        
    def init(self, appConfig: str = "hangoutcore.properties", botConfig: str = None):
        if self.appConfigExists():
            # properties file found. Begin loading info
            if not appConfig.endswith(".properties"):
                appConfig = appConfig + ".properties"
            with open(appConfig, "r+b") as hangoutcore_config:
                p = Properties()
                p.load(hangoutcore_config, "utf-8")
                if botConfig is not None:
                    if not botConfig.endswith(".json"):
                        botConfig = botConfig + ".json"
                    self.setConfigPath(botConfig)
                else:
                    self.setConfigPath(p["botConfig"].data)
                self.setConfigDirectoryPath(p["botConfigDirectory"].data)
                self.setCogDirectoryPath(p["botCogDirectory"].data)
                self.setLogDirectoryPath(p["botLogDirectory"].data)
        else:
            # properties file wasn't found. Assume that this is a fresh install
            print("Not Found")

        # return
        # if configName is None:
        #     with open(f"hangoutcore.properties", "r+b") as hangoutcore_config:
        #         p = Properties()
        #         p.load(hangoutcore_config, "utf-8")
        #         Config().CONFIG_PATH = p["botConfig"].data
        #         Config().CONFIG_DIRECTORY_PATH = p["botConfigDirectory"].data
        #         Config().COG_DIRECTORY_PATH = p["botCogDirectory"].data
        #         Config().LOG_DIRECTORY_PATH = p["botLogDirectory"].data
        # else:
        #     if Config().exists(configName):
        #         with open(f"hangoutcore.properties", "r+b") as hangoutcore_config:
        #             p = Properties()
        #             p.load(hangoutcore_config, "utf-8")
        #             if configName.endswith('.json'):
        #                 Config().CONFIG_PATH = configName
        #                 p["botConfig"] = configName
        #             else:
        #                 Config().CONFIG_PATH = configName + '.json'
        #                 p["botConfig"] = configName + '.json'
        #             Config().CONFIG_DIRECTORY_PATH = p["botConfigDirectory"].data
        #             Config().COG_DIRECTORY_PATH = p["botCogDirectory"].data
        #             Config().LOG_DIRECTORY_PATH = p["botLogDirectory"].data

        #             with open(f"hangoutcore.properties", "wb") as hangoutcore_config:
        #                 p.store(hangoutcore_config,
        #                         encoding="utf-8")  # Store provided information in a properties file.
        #     else:
        #         with open(f"hangoutcore.properties", "r+b") as hangoutcore_config:
        #             p = Properties()
        #             p.load(hangoutcore_config, "utf-8")
        #             Config().CONFIG_PATH = p["botConfig"].data
        #             Config().CONFIG_DIRECTORY_PATH = p["botConfigDirectory"].data
        #             Config().COG_DIRECTORY_PATH = p["botCogDirectory"].data
        #             Config().LOG_DIRECTORY_PATH = p["botLogDirectory"].data
        #         Terminal().Log().ERROR(
        #             f"config: {configName} could not be found. loading config: {p['botConfig'].data} instead.")

    def load(self):
        """
        Attempt to load the config from path provided if none provided uses the config name provided during initiation.
        """
        fileName = self.CONFIG_PATH
        fileDirectory = self.CONFIG_DIRECTORY_PATH

        if self.botConfigExists():
            with open(f"{fileDirectory}/{fileName}") as configFile:
                self.CONFIG = json.load(configFile)
                if "_info" in self.CONFIG:
                    if not self.CONFIG["_info"]["version"] >= self.CONFIG_VERSION:
                        if not self.WARNED:
                            Terminal().Log().WARNING(f"{fileName} is outdated. Please update it to avoid incompatability with HangoutCore.")
                            if click.confirm(f"Attention: Your config version {self.CONFIG['_info']['version']} is outdated. Would you like to update to {self.CONFIG_VERSION} ?",
                                    default=True):
                                new_cfg = self.EXAMPLE_CONFIG
                                new_cfg['_info']['update_reason'] = f"Update To Config Version {self.CONFIG_VERSION}"
                                for key in self.CONFIG['bot'].keys():
                                    new_cfg['bot'][key] = self.CONFIG['bot'][key]
                                for key in self.CONFIG['database'].keys():
                                    new_cfg['database'][key] = self.CONFIG['database'][key]
                                for key in self.CONFIG['music'].keys():
                                    new_cfg['music'][key] = self.CONFIG['music'][key]
                                with open(f"{fileDirectory}/{fileName}", "w") as botConfig:
                                    json.dump(new_cfg, botConfig, indent=4)
                                self.CONFIG = new_cfg
        # OLD
        # if self.exists(fileName):
        #     with open(f"{fileDirectory}/{fileName}") as configFile:
        #         cfg = json.load(configFile)
        #         if '_info' in cfg:
        #             if cfg['_info']['version'] >= self.CONFIG_VERSION:
        #                 return cfg
        #             else:
        #                 if not self.WARNED:  # Config is outdated
        #                     self.WARNED = True
        #                     Terminal().queue("WARNING",
        #                                    f"{fileName} is outdated. Please update it to avoid incompatability")
        #                     if click.confirm(
        #                             f"Attention: Your config version {cfg['_info']['version']} is outdated. Would you like to update to {self.CONFIG_VERSION}",
        #                             default=True):
        #                         new_cfg = self.EXAMPLE_CONFIG
        #                         new_cfg['_info']['update_reason'] = f"Update To Config Version {self.CONFIG_VERSION}"
        #                         for key in cfg['bot'].keys():
        #                             new_cfg['bot'][key] = cfg['bot'][key]
        #                         for key in cfg['database'].keys():
        #                             new_cfg['database'][key] = cfg['database'][key]
        #                         for key in cfg['music'].keys():
        #                             new_cfg['music'][key] = cfg['music'][key]
        #                         with open(f"{fileDirectory}/{fileName}", "w") as botConfig:
        #                             json.dump(new_cfg, botConfig, indent=4)
        #                     else:
        #                         return cfg
        #         else:
        #             if not self.WARNED:  # Couldn't Find version, file probably outdated or corrupted.
        #                 self.WARNED = True
        #                 Terminal().queue("WARNING",
        #                                f"{fileName} is either outdated or corrupt. Please delete the old one and run the bot again to create a new one.")
        #             return cfg

    def setup(self, init_time: str = '{0:%d%b%Y %Hh:%Mm}'.format(datetime.now()), manual: bool = False):
        """
        This function runs through the process of setting up our bot config with the necessary details. such as bot Name, Token, Authorized Users, Etc.
        """
        if not manual:
            print("Oh No! I could not find a config file.")
        if click.confirm("Do you wish to begin the setup process?", default=True):
            #Terminal().initiate(init_time, False, True)  # Clear and prepare terminal for setup process

            def requestBotName():
                setup_botName = input(f"Please Enter The Bot Name: ")
                while setup_botName == "":
                    print("Bot Name cannot be blank, Please Enter again.")
                    setup_botName = input(f"Please Enter The Bot Name: ")
                return setup_botName

            def requestBotPrefix():
                default = "!"
                setup_botPrefix = input(f"Please Enter The Bot Prefex (Default: {default}): ")
                if setup_botPrefix == "":
                    return default
                else:
                    return setup_botPrefix

            def requestBotVersion():
                default = "0.0.0"
                setup_botVersion = input(f"Please Enter The Bot Version (Default: {default}): ")
                if setup_botVersion == "":
                    return default
                else:
                    return setup_botVersion

            def requestBotToken():
                while True:
                    setup_botToken = getpass(f"Please Enter The Bot Token (Input will be blank for your protection)")
                    # get the bot from discord api, so we can verify with the user if it is what they want to use
                    setup_bot = requests.get('https://discord.com/api/v10/users/@me',
                                             headers={'Authorization': f'Bot {setup_botToken}'}).json()
                    if setup_bot.get('message') == '401: Unauthorized':
                        print('It seems that bot doesn\'t exist.')
                        continue
                    else:
                        if click.confirm(f"You want to use bot: {setup_bot.get('username')}. Is That Correct?", default=True):
                            break
                        else:
                            continue
                return setup_botToken

            def requestBotConfigName():
                default = "config.json"
                botConfigName = input(f"Please enter your desired config name. (Default: {default}): ")
                if botConfigName == "":
                    return default
                if not botConfigName.endswith(".json"):
                    botConfigName = botConfigName + ".json"
                return botConfigName

            def requestBotConfigDirectory():
                default = "configs"
                botConfigDirectory = input(
                    f"Please enter where you'd like to store your configs (Default: /{default}): /")
                if botConfigDirectory == "":
                    return default
                else:
                    return botConfigDirectory

            def requestBotLogDirectory():
                default = "logs"
                botLogDirectory = input(f"Please enter where you'd like to store your logs (Default: /{default}): /")
                if botLogDirectory == "":
                    return default
                else:
                    return botLogDirectory

            def requestBotCogDirectory():
                default = "cogs"
                botCogDirectory = input(f"Please enter where you'd like to store your cogs (Default: /{default}): /")
                if botCogDirectory == "":
                   return default
                else:
                    return botCogDirectory

            botName = requestBotName()
            botDescription = input("Please enter your bot description, this can be modified in the config file.:\n")
            botPrefix = requestBotPrefix()
            botVersion = requestBotVersion()
            botToken = requestBotToken()
            botConfigName = requestBotConfigName()
            botConfigDirectory = requestBotConfigDirectory()
            botLogDirectory = requestBotLogDirectory()
            botCogDirectory = requestBotCogDirectory()

            #Terminal().initiate(init_time, False, True)  # refresh terminal
            if click.confirm(
                    f"""Bot Name: {botName}\nBot Description: {botDescription}\nBot Version: ({botVersion})\nBot Token: {"*" * len(botToken)}\nBot Config Name: {botConfigName}\nBot Config Directory: /{botConfigDirectory}\nBot Log Directory: /{botLogDirectory}\nBot Cog Directory: /{botCogDirectory}\nAre the values above accurate?""",
                    default=True):
                Terminal().Log().INFO("Creating a properties file to store hangoutcore variables.")
                p = Properties()
                p["botConfig"] = botConfigName
                p["botConfigDirectory"] = botConfigDirectory
                p["botLogDirectory"] = botLogDirectory
                p["botCogDirectory"] = botCogDirectory

                with open(f"hangoutcore.properties", "wb") as hangoutcore_config:
                    p.store(hangoutcore_config, encoding="utf-8")  # Store provided information in a properties file.

                self.CONFIG_PATH = botConfigName
                self.CONFIG_DIRECTORY_PATH = botConfigDirectory
                self.COG_DIRECTORY_PATH = botCogDirectory
                self.LOG_DIRECTORY_PATH = botLogDirectory

                if not os.path.exists(botConfigDirectory):
                    Terminal().Log().INFO(f"Creating Config Directory: /{botConfigDirectory}")
                    os.mkdir(botConfigDirectory)
                else:
                    Terminal().Log().INFO(f"Config directory already exists, skipping...")
                if not os.path.exists(botCogDirectory):
                    Terminal().Log().INFO(f"Creating Cog Directory: /{botCogDirectory}")
                    os.mkdir(botCogDirectory)
                else:
                    Terminal().Log().INFO(f"Cog directory already exists, skipping...")
                if not os.path.exists(botLogDirectory):
                    Terminal().Log().INFO(f"Creating Log Directory: /{botLogDirectory}")
                    os.mkdir(botLogDirectory)
                else:
                    Terminal().Log().INFO(f"Log directory already exists, skipping...")

                with open(f"{botConfigDirectory}/{botConfigName}", 'w') as file:  # Create initial config file.
                    json.dump(self.EXAMPLE_CONFIG, file, indent=4)

                # return Config().load(path=f"{botConfigDirectory}/Config().json")

                self.write(value=botName, key1="bot", key2="name")
                self.write(value=botDescription, key1="bot", key2="description")
                self.write(value=botPrefix, key1="bot", key2="prefixes", key3=0)
                self.write(value=botVersion, key1="bot", key2="version")
                self.write(value=botToken, key1="bot", key2="token", key3=0)
            else:
                self.setup(init_time)

        else:
            Terminal().Log().ERROR("HangoutCore Setup Canceled.")
            Terminal().EXIT("Exiting...")

    def write(self, value: str = None, key1: str = None, key2=None, key3=None, key4=None):
        """
        Attempt to write to the config from path provided in hangoutcore.properties,
        if one does not exist we warn the terminal. We do not create one in the possibility that
        the user misspelled the path provided.
        ***USE CAUTION UPDATING CONFIG WITH THIS, YOU CAN MODIFY CONFIG VALUES TO UNSAFE VALUES THAT WE DO NOT FILTER THROUGH***
        """
        with open(f"{self.CONFIG_DIRECTORY_PATH}/{self.CONFIG_PATH}", "r") as botConfig:
            configData = json.load(botConfig)

    # There's probably a much better way to do this, but it works so eh.
        if key4 is not None:
            configData[key1][key2][key3][key4] = value
        elif key3 is not None:
            configData[key1][key2][key3] = value
        elif key2 is not None:
            configData[key1][key2] = value
        elif key1 is not None:
            configData[key1] = value

        with open(f"{self.CONFIG_DIRECTORY_PATH}/{self.CONFIG_PATH}", "w") as botConfig:
            json.dump(configData, botConfig, indent=4)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ↓ Database ↓ : WIP
#   › Used to keep the majority of the heavy lifting out of main script, and cog files.
#   › Author: Lino
#   › Date: 15 Nov, 2022
#   › TODO: Add support for SQLITE, POSTGRES, MYSQL and more. to make it easier for first time programmers.
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class database():
    def __init__(self):
        pass

    async def RegisterGuild(loop, guild: discord.Guild):
        cfg = Config().load()
        if cfg is not None:
            pool = await aiomysql.create_pool(
                db=cfg["database"]["name"],
                host=cfg["database"]["host"],
                port=cfg["database"]["port"],
                user=cfg["database"]["user"],
                password=cfg["database"]["password"]

            )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ↓ Local ↓ : WIP
#   › Handles providing local files such as images, video, cogs, py files, etc.
#   › Fill with functions as you need, intended to keep other files clear and let utils do the heavy lifting.
#   › Author: Lino
#   › Date: 15 Nov, 2022
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class Local():
    def __init__(self):
        pass

    def GetCogs(self):
        valid_files = []
        disabled_files = []
        invalid_files = []
        for file in os.listdir(Config().COG_DIRECTORY_PATH):
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

    async def load_extensions(self, discordBot: discord.Client, debug_mode: bool = False):
        """
        Scans for files in the cog directory specified in the Config(). Loads the file if it ends in '.py', and registers files ending in '.disabled' as disabled cogs.
        """
        cogs = local().GetCogs()

        for cog in cogs["valid_files"]:
            Terminal().Log().INFO(f" └ Found {cog}")
            try:
                await discordBot.load_extension(f'{Config().COG_DIRECTORY_PATH}.{cog[:-3]}')
            except Exception as e:
                Terminal().errorprocessing.CogLoadError(cog, e, debug_mode)
            else:
                Terminal().Log().INFO(f"  └ successfully loaded {cog}.")
        for cog in cogs["disabled_files"]:
            Terminal().Log().INFO(f" └ Found Disabled file {cog}, Skipping.")
        for cog in cogs["invalid_files"]:
            if cog == "__pycache__" or "__init__":
                pass
            else:
                Terminal().Log().INFO(f" └ Found invalid file {cog}, Skipping.")
        Terminal().Log().INFO(f"Successfully loaded {len(cogs['valid_files'])} extension(s).")
        if len(cogs["invalid_files"]) > 0:
            Terminal().Log().WARNING(
                f"Found {len(cogs['invalid_files'])} invalid extension(s) in the 'cogs' directory. If you believe this is an error please verify each .py file and make sure it is set up as a cog properly, Otherwise you can ignore this message.")

    async def GetTicketTranscript(ticketid: str):
        transcriptDirectory = (f"transcripts\\")
        if os.path.exists(f"{transcriptDirectory}{ticketid}.md"):
            with open(f"{transcriptDirectory}{ticketid}.md", 'rb') as transcriptFile:
                return transcriptFile

    def GetTicketTranscriptPath(ticketid: str):
        transcriptDirectory = (f"transcripts\\")
        if os.path.exists(f"{transcriptDirectory}{ticketid}.md"):
            return os.path.abspath(f"{transcriptDirectory}{ticketid}.md")

    async def CreateTicketTranscript(ticketid: str, discordChannel: discord.channel, ticketAuthor: discord.User):
        transcriptDirectory = (f"transcripts\\")
        if not os.path.exists(f"{transcriptDirectory}{ticketid}.md"):
            ticketTranscript: discord.File
            async with aiofiles.open(f"{transcriptDirectory}{ticketid}.md", 'a', encoding="utf-8") as transcriptFile:
                await transcriptFile.write(f"# Official Transcript for Ticket ID: {ticketid}:\n")
                await transcriptFile.write(f"---\n")
                await transcriptFile.write(f"## **BEGIN TRANSCRIPT** \n\n")
                async for message in discordChannel.history(limit=None, oldest_first=True):
                    created = datetime.strftime(message.created_at, "%m/%d/%Y at %H:%M:%S")
                    if message.edited_at:
                        edited = datetime.strftime(message.edited_at, "%m/%d/%Y at %H:%M:%S")
                        await transcriptFile.write(
                            f"**{message.author} on {created}**: > {message.clean_content} (Edited at {edited})\n")
                        if len(message.embeds) > 0:
                            for embed in message.embeds:
                                await transcriptFile.write(f"- Embed: {str(embed)}\n")
                        if len(message.attachments) > 0:
                            for attachment in message.attachments:
                                await transcriptFile.write(
                                    f"- File Type: {attachment.content_type} [{attachment.filename}]({attachment.url})\n")
                    else:
                        await transcriptFile.write(f"**{message.author} on {created}**: > {message.clean_content}\n")
                        if len(message.embeds) > 0:
                            for embed in message.embeds:
                                embed_text = ""
                                embed_text = embed_text + f"Title: *{embed.title}*\n"
                                embed_text = embed_text + f"Description: *{embed.description}*\n"
                                for field in embed.fields:
                                    embed_text = embed_text + f"Field Name: *{field.name}*\n"
                                    embed_text = embed_text + f"Field Value: *{field.value}*\n"
                                embed_text = embed_text + f"Footer: *{embed.footer.text}*\n"
                                await transcriptFile.write(f"- Embed: \n{embed_text}\n")
                        if len(message.attachments) > 0:
                            await transcriptFile.write(f"*Message Attachments*\n")
                            for attachment in message.attachments:
                                await transcriptFile.write(
                                    f"- File: \nType: {attachment.content_type}\nURL: [{attachment.filename}]({attachment.url})\n")
                await transcriptFile.write(f"\n## **END TRANSCRIPT** \n")
                await transcriptFile.write(f"---\n")
                generated = datetime.now().strftime("%m/%d/%Y at %H:%M:%S")
                await transcriptFile.write(
                    f"*Generated at {generated} by {ticketAuthor.name}#{ticketAuthor.discriminator} AKA {ticketAuthor.display_name}*\n*Date Formatting: MM/DD/YY*\n*Time Zone: UTC*")
                ticketTranscript = discord.File(fp=local().GetTicketTranscriptPath(ticketid=ticketid),
                                                filename=f"{discordChannel.name}.md")
                # os.close(transcriptFile)
                # ticketTranscript.close()
                await transcriptFile.close()
                return ticketTranscript

    def DeleteTicketTranscript(ticketid: str):
        transcriptDirectory = (f"transcripts\\")
        if os.path.exists(f"{transcriptDirectory}{ticketid}.md"):
            try:
                os.remove(f"{transcriptDirectory}{ticketid}.md")
            except Exception as e:
                Terminal().Log().ERROR(f"{e}")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ↓ Terminal ↓ : WIP
#   › Used to optimize terminal handling
#   › Author: Lino
#   › Date: 15 Nov, 2022
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class Terminal():
    log_Queue = []

    def print_center(self, s: str):
        """Print on the center of the terminal. Used primarily for decorative purposes."""
        print(s.center(shutil.get_terminal_size().columns))

    def print_hr(self):
        """Print a horizontal line across the terminal. Used primarily for decorative purposes."""
        print('━'.center(shutil.get_terminal_size().columns, '━'))

    def clear(self):
        """Clears the terminal."""
        if name == 'nt':
            _ = system('cls')
        else:
            _ = system('clear')

    def initiate(self):# start_time: str, debug: bool = False, bot_setup: bool = False
        """
        Clear's and prepares terminal for bot output.
        """
        # work on a way to share config instance with util classes.
        # potentially by setting a variable?
        
        # cfg = Config().load()
        # if cfg is not None:
        #     if bot_setup:
        #         Terminal().clear()
        #         if debug:
        #             print(Style.BRIGHT + Back.RED, end="\r")
        #         else:
        #             print(Style.NORMAL + Fore.BLACK + Back.WHITE, end="\r")
        #         Terminal().print_center("Bot Setup")
        #         Terminal().print_center("")
        #         Terminal().print_center(str(start_time))
        #         if debug:
        #             Terminal().print_center(f'// Debug Mode Enabled \\\ ')
        #             Terminal().print_center('SYS Version ' + str(sys.version))
        #             Terminal().print_center('API Version ' + str(sys.api_version))
        #             Terminal().print_center('Discord Version ' + str(discord.__version__))
        #         print(Style.RESET_ALL + Back.RESET, end="\r")
        #         Terminal().print_hr()
        #         Terminal().print_center("██╗░░██╗░█████╗░███╗░░██╗░██████╗░░█████╗░██╗░░░██╗████████╗░█████╗░░█████╗░██████╗░███████╗")
        #         Terminal().print_center("██║░░██║██╔══██╗████╗░██║██╔════╝░██╔══██╗██║░░░██║╚══██╔══╝██╔══██╗██╔══██╗██╔══██╗██╔════╝")
        #         Terminal().print_center("███████║███████║██╔██╗██║██║░░██╗░██║░░██║██║░░░██║░░░██║░░░██║░░╚═╝██║░░██║██████╔╝█████╗░░")
        #         Terminal().print_center("██╔══██║██╔══██║██║╚████║██║░░╚██╗██║░░██║██║░░░██║░░░██║░░░██║░░██╗██║░░██║██╔══██╗██╔══╝░░")
        #         Terminal().print_center("██║░░██║██║░░██║██║░╚███║╚██████╔╝╚█████╔╝╚██████╔╝░░░██║░░░╚█████╔╝╚█████╔╝██║░░██║███████╗")
        #         Terminal().print_center("╚═╝░░╚═╝╚═╝░░╚═╝╚═╝░░╚══╝░╚═════╝░░╚════╝░░╚═════╝░░░░╚═╝░░░░╚════╝░░╚════╝░╚═╝░░╚═╝╚══════╝")
        #         Terminal().print_center("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        #     elif not bot_setup:
        #         Terminal().clear()
        #         if debug:
        #             print(Style.BRIGHT + Back.RED, end="\r")
        #         else:
        #             print(Style.NORMAL + Fore.BLACK + Back.WHITE, end="\r")
        #         Terminal().print_center(str(cfg["bot"]["name"]))
        #         Terminal().print_center(str(cfg["bot"]["version"]))
        #         Terminal().print_center(str(start_time))
        #         if debug:
        #             Terminal().print_center(f'// Debug Mode Enabled \\\ ')
        #             Terminal().print_center('SYS Version ' + str(sys.version))
        #             Terminal().print_center('API Version ' + str(sys.api_version))
        #             Terminal().print_center('Discord Version ' + str(discord.__version__))
        #         print(Style.RESET_ALL + Back.RESET, end="\r")
        #         Terminal().print_hr()

    class Log():
        def DEBUG(self, log: str):
            print(f"[{Fore.BLUE}DEBUG{Fore.RESET}] {log}")

        def INFO(self, log: str):
            print(f"[{Fore.GREEN}INFO{Fore.RESET}] {log}")

        def WARNING(self, log: str):
            print(f"[{Fore.YELLOW}WARNING{Fore.RESET}] {log}")

        def ERROR(self, log: str):
            print(f"[{Fore.RED}ERROR{Fore.RESET}] {log}")

        def CRITICAL(self, log: str):
            print(f"{Style.BRIGHT}{Back.RED}[CRITICAL] {log}{Style.RESET_ALL}{Back.RESET}")

    def queue(self, level, log):
        if level is not None:
            Terminal().log_Queue.append(f"{level}|{log}")

    def EXIT(self, log: str):
        """Closes script with preset formatting for output message."""
        exit(f"{Style.BRIGHT}{Back.RED}[SYSTEM]{Back.RESET}{Fore.RED} {log}{Fore.RESET}{Style.RESET_ALL}")

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # ↓ Custom Error Processing ↓ : WIP
    #   › Intended for when you only need specific data from an error.
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    class errorprocessing():
        def __init__(self):
            pass

        def CogLoadError(self, file, error, debug_mode):
            """ Error Processing tailored to display the specific error when loading a cog, 
                designed to minimise clutter and lines not relevant."""
            ErrorTraceback = traceback.format_exception(type(error), error, error.__traceback__)
            if debug_mode:
                Terminal().Log().ERROR(f"  └ Failed to load {file}\n" + "".join(ErrorTraceback))
            else:

                Terminal().Log().ERROR(f"""  └ Failed to load {file}.
                {Back.RED}{error}{Back.RESET}""")

        class CommandError:

            def InsufficientPerms(self, NotifyGuild: bool, command: commands.Command, member: discord.Member):
                ErrorMessage = f"""{member.name} attempted to execute command: {command.name} however they do not have sufficient permissions."""
                Terminal().Log().ERROR(ErrorMessage)
                return ErrorMessage

        async def NotifyGuildStaff(self, guild: discord.Guild, color=discord.Color.from_rgb(47, 49, 54),
                                   title: str = "Notification Title", message: str = "Notification Message"):
            NotificationChannel = await database.RetrieveGuildNotificationChannel(guild=guild)
            if NotificationChannel is not None:
                GuildNotificationEmbed = discord.Embed(
                    title=f"{title}",
                    description=f"{message}",
                    timestamp=datetime.now(),
                    color=color
                )
                GuildNotificationEmbed.set_footer(text=f"Staff Notification")
                await NotificationChannel.send(embed=GuildNotificationEmbed)
                return None
            else:
                Terminal().Log().CRITICAL(
                    f"{guild.name} does not have a Notification Channel set up. They will not be able to recieve Notifications.")
                return f"This Guild does not have a notification channel registered in our database. Please utilize the **/setup** command and try again"


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ↓ Terminal ↓ : WIP
#   › Used to optimize terminal handling
#   › Author: Lino
#   › Date: 15 Nov, 2022
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class CustomViews():
    # class autoroleView(discord.ui.View):
    #     def __init__(self):
    #         super().__init__(timeout=None)

    #     @discord.ui.button(label='Game Development', style=discord.ButtonStyle.grey, custom_id='persistent_autorole:gameDev')
    #     async def green(self, button: discord.ui.Button, interaction: discord.Interaction):
    #         role = interaction.guild.get_role(868692760524365875)
    #         user = interaction.user
    #         if role in user.roles:
    #             confirmation = bot.CustomViews.confirmationView()
    #             await interaction.response.send_message(f"Are you sure you'd like to remove {role.mention} from your roles?",view=confirmation, ephemeral=True)
    #             await confirmation.wait()
    #             if confirmation.value is None:
    #                 await interaction.response.send_message(f"Timed out.", ephemeral=True)
    #             elif confirmation.value:
    #                 await user.remove_roles(role, reason="User removed via AutoRole.")
    #                 await interaction.response.send_message(f"You've successfully been unassigned {role.mention}.", ephemeral=True)
    #             else:
    #                 return      
    #         else:
    #             await user.add_roles(role, reason="User added via AutoRole.")
    #             await interaction.response.send_message(f"You've successfully been assigned {role.mention}.", ephemeral=True)  # Remnants of old personal bot

    # @discord.ui.button(label='Bot Development', style=discord.ButtonStyle.grey, custom_id='persistent_autorole:botDev')
    # async def grey(self, button: discord.ui.Button, interaction: discord.Interaction):
    #     role = interaction.guild.get_role(868692545490804746)
    #     user = interaction.user
    #     if role in user.roles:
    #         confirmation = bot.CustomViews.confirmationView()
    #         await interaction.response.send_message(f"Are you sure you'd like to remove {role.mention} from your roles?",view=confirmation, ephemeral=True)
    #         await confirmation.wait()
    #         if confirmation.value is None:
    #             await interaction.response.send_message(f"Timed out.", ephemeral=True)
    #         elif confirmation.value:
    #             await user.remove_roles(role, reason="User removed via AutoRole.")
    #             await interaction.response.send_message(f"You've successfully been unassigned {role.mention}.", ephemeral=True)
    #         else:
    #             return
    #     else:
    #         await user.add_roles(role, reason="User added via AutoRole.")
    #         await interaction.response.send_message(f"You've successfully been assigned {role.mention}.", ephemeral=True)

    class Confirm(discord.ui.View):
        def __init__(self):
            super().__init__()
            self.value = None

        # When the confirm button is pressed, set the inner value to `True` and
        # stop the View from listening to more input.
        # We also send the user an ephemeral message that we're confirming their choice.
        @discord.ui.button(label='Confirm', style=discord.ButtonStyle.green)
        async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.send_message('Confirming', ephemeral=True)
            self.value = True
            self.stop()

        # This one is similar to the confirmation button except sets the inner value to `False`
        @discord.ui.button(label='Cancel', style=discord.ButtonStyle.grey)
        async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.send_message('Cancelling', ephemeral=True)
            self.value = False
            self.stop()

    class CustomButtons():
        def __init__(self):
            pass