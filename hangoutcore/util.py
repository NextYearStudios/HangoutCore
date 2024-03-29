"""
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    Utility Module for HangoutCore
        › Please do not modify any of the following content unless you know what you're doing. Modifying the following code and not updating the rest of the bot code to match can/will cause issues.
        › If you do decide to modify the following code please understand that HangoutCore's Dev team, Discord.py's Dev Team nor Python's Dev team are obligated to help you.
        › By Modifying the following code you acknowledge and agree to the text above.
    Module Last Updated: January 7, 2023
    Module Last Updated by: Lino
    License: Refer to LICENSE.md
    Notes:
        None
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import asyncio
import aiofiles
import click
import ctypes
import discord
import hangoutcore
import json
import logging
import os, sys
import shutil
import traceback
import requests

from getpass import getpass
from asyncio import sleep
from colorama import *
from dataclasses import dataclass
from datetime import datetime
from discord.ext import commands
from jproperties import Properties
from typing import Optional
from os import system, name

init(strip=not sys.stdout.isatty()) # Strip color if stdout is redirected.


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ↓ Audio Handling ↓ : WIP
#   › Used for playing music and keeping the audio function clutter out of the main script.
#   › Author: Lino
#   › Date: 15 Nov, 2022
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class Audio():
    def __init__(self):
        self.config = None
        self.terminal = None

    async def setConfig(self, config = None):
        if config is not None:
            self.config = config

    async def setTerminal(self, terminal = None):
        if terminal is not None:
            self.terminal = terminal
    
    class guildstate():
        def __init__(self):
            self.now_playing = None
            self.playlist = []
            self.skip_votes = set()
            self.volume = int(Config().load()["music"]["max_volume"]) / 100
    
    async def verify_opus(self):
        """
            Looks for opus throughout the system, Attempts to load if found.
        """
        opuslib = ctypes.util.find_library('opus')
        if opuslib is not None:
            try:
                await self.terminal.Log().INFO(f"Loading Opus.")
                discord.opus.load_opus('opus')
            except Exception as e:
                await self.terminal.Log().ERROR(e)
            else:
                if not discord.opus.is_loaded():
                    await self.terminal.Log().CRITICAL("Opus Failed To Load.")
                else:
                    await self.terminal.Log().INFO("Successfully loaded opus.")
        else:
            await self.terminal.Log().WARNING("Could not find Opus, You will not be able to play audio without it.")
            await self.terminal.Log().WARNING("To download opus codec source code follow this link: https://opus-codec.org/downloads/")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ↓ Config ↓ : WIP
#   › Used for handling bot configuration file.
#   › Author: Lino
#   › Date: 15 Dec, 2022
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class Config():

    def __init__(self):
        self.WARNED = False
        self.CONFIG = None
        self.CONFIG_VERSION = 6.0
        self.CONFIG_PATH = 'config.json'  # Path and name of config file.
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
                    "guilds": False,
                    "members": False,
                    "bans": False,
                    "emojis": False,
                    "emojis_and_stickers": False,
                    "integrations": False,
                    "webhooks": False,
                    "invites": False,
                    "voice_states": False,
                    "presences": False,
                    "messages": False,
                    "guild_messages": False,
                    "dm_messages": False,
                    "reactions": False,
                    "guild_reactions": False,
                    "dm_reactions": False,
                    "typing": False,
                    "guild_typing": False,
                    "dm_typing": False,
                    "message_content": False,
                    "guild_scheduled_events": False,
                    "auto_moderation": False,
                    "auto_moderation_configuration": False,
                    "auto_moderation_execution": False
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
                        "owner": True  # Set this to true if they're an owner. otherwise set it to False
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
                    "error_dev_runningextensionname": "The Extension name you provided matches an already loaded extension. Please check your spelling and try again.",
                    "error_dev_invalidextensionname": "The Extension name you provided does not match any valid or existing extensions. Please check your spelling and try again.",
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
        self.terminal = Terminal() # Just incase we don't set, we need to have a backup
            
    async def appConfigExists(self, DesiredName: str= None):
        ConfigName = "hangoutcore.properties"
        if DesiredName is not None:
            ConfigName = DesiredName
        
        if ".properties" not in ConfigName:
            ConfigName = ConfigName + ".properties"

        if os.path.exists(ConfigName) and os.path.isfile(ConfigName):
            return True
        else:
            return False
            
    async def botConfigExists(self, DesiredName: str= None):
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

    async def getConfig(self):
        return self.CONFIG

    async def setConfigPath(self, configPath: str):
        if configPath is not None:
            if configPath.endswith(".json"):
                self.CONFIG_PATH = configPath
    
    async def getConfigPath(self):
        return self.CONFIG_PATH

    async def setConfigDirectoryPath(self, configDirectoryPath: str):
        if configDirectoryPath is not None:
            self.CONFIG_DIRECTORY_PATH = configDirectoryPath
    
    async def getConfigDirectoryPath(self):
        return self.CONFIG_DIRECTORY_PATH
    
    async def setCogDirectoryPath(self, cogDirectoryPath: str):
        if cogDirectoryPath is not None:
            self.COG_DIRECTORY_PATH = cogDirectoryPath
    
    async def getCogDirectoryPath(self):
        return self.COG_DIRECTORY_PATH
    
    async def setLogDirectoryPath(self, logDirectoryPath: str):
        if logDirectoryPath is not None:
            self.LOG_DIRECTORY_PATH = logDirectoryPath
    
    async def getLogDirectoryPath(self):
        return self.LOG_DIRECTORY_PATH

    async def setConfigTerminal(self, terminal = None):
        if terminal is not None:
            self.terminal = terminal
        
    # The following functions are not really necessary
    # However they do reduce clutter in other scripts so eh, We'll leave them for now.
    async def getBotActivity(self) -> discord.Activity():
        """
        Retrieves Bot Activity specified in our loaded bot config. Returns activity type 'listening' if none is found.
        """
        if self.CONFIG is not None: # make sure our config exists in the first place
            await self.terminal.Log().DEBUG(f"Found Config Activity Type Entry: {self.CONFIG['bot']['status']['type']}")
            if self.CONFIG['bot']['status']['type'] == 'listening':
                return discord.Activity(
                    type = discord.ActivityType.listening,
                    name = self.CONFIG['bot']['status']['name']
                )
            if self.CONFIG['bot']['status']['type'] == 'streaming':
                return discord.Activity(
                    type = discord.ActivityType.streaming,
                    name = self.CONFIG['bot']['status']['name'],
                    game = self.CONFIG['bot']['status']['url']
                )
            if self.CONFIG['bot']['status']['type'] == 'watching':
                return discord.Activity(
                    type = discord.ActivityType.watching,
                    name = self.CONFIG['bot']['status']['name']
                )
            if self.CONFIG['bot']['status']['type'] == 'playing':
                return discord.Activity(
                    type = discord.ActivityType.playing,
                    name = self.CONFIG['bot']['status']['name'],
                    game = self.CONFIG['bot']['status']['game']
                )
            # Assume that we got here because the entry in our config either doesn't exists, or is simply not one of the above.
            await self.terminal.Log().ERROR(f"Config Activity Type Entry: {self.CONFIG['bot']['status']['type']} is not valid. Please check your spelling and try again.")
            return discord.Activity(
                type = discord.ActivityType.listening,
                name= "!help"
            )
        else:
            await self.terminal.Log().DEBUG(f"Config is None. Returning Activity Type: 'listening'")
            return discord.Activity(
                type = discord.ActivityType.listening,
                name= "!help"
            )

    async def getBotIntents(self):
        """Retrieves specified bot intents from config file. If the config file is not able to be loaded this sets intents to False just in case."""
        if self.CONFIG is not None:
            await self.terminal.Log().DEBUG(f"Loading Bot Intents from config. Intents: {self.CONFIG['bot']['intents']}")
            intents = discord.Intents.default()  # Set Bot Intents
            intents.members         = self.CONFIG['bot']['intents']['members']
            intents.message_content = self.CONFIG['bot']['intents']['message_content']
            intents.typing          = self.CONFIG['bot']['intents']['typing']
            intents.presences       = self.CONFIG['bot']['intents']['presences']
            intents.guilds          = self.CONFIG['bot']['intents']['guilds']
            return intents
        else:
            await self.terminal.Log().WARNING(f"Could not retrieve intents from Config(). Setting intents to False as a precaution.")
            intents = discord.Intents.default()  # Set Bot Intents
            intents.members = False
            intents.message_content = False
            intents.typing = False
            intents.presences = False
            intents.guilds = False
            return intents

    async def getBotPrefix(self): # Since we're moving to slash commands this will eventually get removed.
        if self.CONFIG is not None:
            if self.CONFIG['bot']['prefixes'] is not None:
                if type(self.CONFIG['bot']['prefixes']) == str:
                    return list(self.CONFIG['bot']['prefixes'])
                else:
                    return self.CONFIG['bot']['prefixes']
            else:
                return ['!']

    async def init(self, appConfig: str = "hangoutcore.properties", botConfig: str = None):
        await self.terminal.Log().DEBUG(f"Attempting to locate properties file {appConfig}.")
        if await self.appConfigExists(appConfig):
            await self.terminal.Log().DEBUG(f"Found {appConfig}, Loading data.")
            # properties file found. Begin loading info
            with open(appConfig, "r+b") as hangoutcore_config:
                p = Properties()
                p.load(hangoutcore_config, "utf-8")
                if botConfig is not None:
                    if not botConfig.endswith(".json"):
                        botConfig = botConfig + ".json"
                    await self.setConfigPath(botConfig)
                else:
                    await self.setConfigPath(p["botConfig"].data)
                await self.setConfigDirectoryPath(p["botConfigDirectory"].data)
                await self.setCogDirectoryPath(p["botCogDirectory"].data)
                await self.setLogDirectoryPath(p["botLogDirectory"].data)
                return True
        else:
            # properties file wasn't found. Assume that this is a fresh install
            await self.terminal.Log().DEBUG(f"Attempted to locate properties file {appConfig}, Nothing was found.")
            return False

    async def load(self, desiredConfig = None):
        """
        Attempt to load the config from path provided if none provided uses the config name provided during initiation.
        """
        fileName = self.CONFIG_PATH
        fileDirectory = self.CONFIG_DIRECTORY_PATH

        if desiredConfig is not None:
            if await self.botConfigExists(desiredConfig):
                filename = desiredConfig
            else:
                await self.terminal.Log().WARNING(f"Bot Config: {fileDirectory}/{desiredConfig} does not exists. Defaulting to {fileDirectory}{fileName}")

        if await self.botConfigExists(fileName):
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
                                    if key != "intents" and key != "messages":
                                        new_cfg['bot'][key] = self.CONFIG['bot'][key]
                                # for key in self.CONFIG['database'].keys():
                                #     new_cfg['database'][key] = self.CONFIG['database'][key]
                                # for key in self.CONFIG['music'].keys():
                                #     new_cfg['music'][key] = self.CONFIG['music'][key]
                                with open(f"{fileDirectory}/{fileName}", "w") as botConfig:
                                    json.dump(new_cfg, botConfig, indent=4)
                                self.CONFIG = new_cfg
                            
    async def setup(self, init_time: str = '{0:%d%b%Y %Hh:%Mm}'.format(datetime.now()), manual: bool = False):
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
                await self.terminal.Log().INFO("Creating a properties file to store hangoutcore variables.")
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
                    await self.terminal.Log().INFO(f"Creating Config Directory: /{botConfigDirectory}")
                    os.mkdir(botConfigDirectory)
                else:
                    await self.terminal.Log().INFO(f"Config directory already exists, skipping...")
                if not os.path.exists(botCogDirectory):
                    await self.terminal.Log().INFO(f"Creating Cog Directory: /{botCogDirectory}")
                    os.mkdir(botCogDirectory)
                else:
                    await self.terminal.Log().INFO(f"Cog directory already exists, skipping...")
                if not os.path.exists(botLogDirectory):
                    await self.terminal.Log().INFO(f"Creating Log Directory: /{botLogDirectory}")
                    os.mkdir(botLogDirectory)
                else:
                    await self.terminal.Log().INFO(f"Log directory already exists, skipping...")

                with open(f"{botConfigDirectory}/{botConfigName}", 'w') as file:  # Create initial config file.
                    json.dump(self.EXAMPLE_CONFIG, file, indent=4)

                # return Config().load(path=f"{botConfigDirectory}/Config().json")

                await self.write(value=botName, key1="bot", key2="name")
                await self.write(value=botDescription, key1="bot", key2="description")
                await self.write(value=botPrefix, key1="bot", key2="prefixes", key3=0)
                await self.write(value=botVersion, key1="bot", key2="version")
                await self.write(value=botToken, key1="bot", key2="token", key3=0)
            else:
                await self.setup(init_time)

        else:
            Terminal().Log().ERROR("HangoutCore Setup Canceled.")
            Terminal().EXIT("Exiting...")

    async def write(self, value: str = None, key1: str = None, key2=None, key3=None, key4=None):
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

class Database():
    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.config = None
        self.terminal = None
        self.pool = None
        self.guildTemplate = {
        "roles": {
            "guild_muted": 0,
            "guild_trial_moderator": 0,
            "guild_moderator": 0,
            "guild_administrator": 0,
            "guild_owner": 0
        },
        "channels": {
            "guild_announcements": 0
        },
        "extras": {
            "guild_announcements": {
            "member_join": {
                "enabled": False,
                "message": ""
            },
            "member_rejoin": {
                "enabled": False,
                "message": ""
            },
            "member_left": {
                "enabled": False,
                "message": ""
            },
            "member_banned": {
                "enabled": False,
                "message": ""
            },
            "member_kicked": {
                "enabled": False,
                "message": ""
            }
            },
            "guild_applications": {
            "enabled": False,
            "channel": 0,
            "roles": [
                {
                "role_name": "",
                "role_id": 0
                }
            ]
            },
            "guild_autoroles": {
            "enabled": False,
            "roles": []
            },
            "guild_bot_announcements": {
            "enabled": False,
            "channel": 0
            },
            "guild_economy": {
            "enabled": False,
            "name": "",
            "currency": "",
            "channel": 0,
            "message": 0,
            "balance_start": 1000
            },
            "guild_level": {
            "enabled": False,
            "announce": False,
            "channel": 0
            },
            "guild_selfroles": {
            "enabled": False,
            "channel": 0,
            "message": 0,
            "roles": []
            },
            "guild_stats": {
            "enabled": False,
            "channel": 0,
            "display": {
                "active_members": False,
                "total_members": False,
                "bots": False
            }
            },
            "guild_staff_announcements": {
            "enabled": False,
            "channel": 0,
            "variables": {
                "user_ban": False,
                "user_kick": False,
                "user_mute": False,
                "user_reported": False,
                "user_warn": False
            }
            },
            "guild_suggestions": {
            "enabled": False,
            "channel": 0,
            "allow_vote": False
            },
            "guild_tickets": {
            "enabled": False,
            "channel": 0,
            "role_staff": 0
            },
            "guild_verification": {
            "enabled": False,
            "channel": 0,
            "role": 0
            },
            "guild_voice_lobby": {
            "enabled": False,
            "channel": 0
            }
        }
        }
        self.userTemplate = {
        "rank": {
            "guild": []
        },
        "inventory": [],
        "economy": {
            "guild": []
        },
        "bot": {
            "blacklisted": False,
            "reason": "",
            "reports": [],
            "bans": [],
            "kicks": [],
            "command_stats": {}
        }
        }

    async def setConfig(self, config = None):
        if config is not None:
            self.config = config

    async def setTerminal(self, terminal = None):
        if terminal is not None:
            self.terminal = terminal
            
    async def setPool(self, pool = None):
        if pool is not None:
            self.pool = pool

    # Mysql Section
    async def registerGuild(self, guild: discord.Guild):
        if self.config is not None and self.pool is not None:
            async with self.pool.get() as conn:
                async with conn.cursor() as cursor:
                    
                    try:
                        await cursor.execute('''\
                            CREATE TABLE IF NOT EXISTS guilds 
                            (id BIGINT PRIMARY KEY UNIQUE NOT NULL, name text, data JSON)''')
                    except Exception as e:
                        await self.terminal.Log().WARNING(f"{e}")

                    try:
                        await cursor.execute(f"""\
                            SELECT * FROM guilds 
                            WHERE id = (%s)
                            """,(guild.id))
                    except Exception as e:
                        await self.terminal.Log().WARNING(f"{e}")
                    result = await cursor.fetchone()
                    if result is None:
                        try:
                            result = await cursor.execute(f"""\
                                    INSERT INTO guilds
                                    (id, name, data)
                                    VALUES( %s, %s, %s)
                                    """, (int(guild.id), guild.name, json.dumps(self.guildTemplate)))
                        except Exception as e:
                            await self.terminal.Log().WARNING(f"{e}")
                        finally:
                            await self.terminal.Log().INFO(f"Successfully created a database entry for guild: {guild.name}")
                    await conn.commit()

    async def retrieveTableColumn(self, table, column):
        if self.config is not None and self.pool is not None:
            async with self.pool.get() as conn:
                async with conn.cursor() as cursor:
                    try:
                        await cursor.execute(f"SELECT {column} FROM {table}")
                    except Exception as e:
                        await self.terminal.Log().WARNING(f"{e}")
                        return None
                    result = await cursor.fetchall()
                    data = []
                    if result is not None:
                        for entry in result:
                            data.append(entry[0])
                        return data
                    else:
                        return None

    async def retrieveGuild(self, guild: discord.Guild):
        if self.config is not None and self.pool is not None:
            async with self.pool.get() as conn:
                async with conn.cursor() as cursor:
                    try:
                        await cursor.execute(f"""\
                            SELECT * FROM guilds 
                            WHERE id = (%s)
                            """,(guild.id))
                    except Exception as e:
                        await self.terminal.Log().WARNING(f"{e}")
                    result = await cursor.fetchone()
                    if result is not None:
                        data = [int(result[0]), str(result[1]), json.loads(result[2])]
                        return data
                    else:
                        return None
                           
    async def updateGuild(self, guild: discord.Guild, data: str):
        if self.config is not None and self.pool is not None:
            async with self.pool.get() as conn:
                async with conn.cursor() as cursor:
                    try:
                        await cursor.execute(f"""\
                            SELECT * FROM guilds 
                            WHERE id = (%s)
                            """,(guild.id))
                    except Exception as e:
                        await self.terminal.Log().WARNING(f"{e}")
                    result = await cursor.fetchone()
                    if result is None:
                        try:
                            result = await cursor.execute(f"""\
                                    INSERT INTO guilds
                                    (id, name, data)
                                    VALUES( %s, %s, %s)
                                    """, (int(guild.id), guild.name, json.dumps(data)))
                        except Exception as e:
                            await self.terminal.Log().WARNING(f"{e}")
                        finally:
                            await self.terminal.Log().INFO(f"Successfully created a database entry for guild: {guild.name}")
                        
                    else:
                        try:
                            result = await cursor.execute(f"""\
                                    UPDATE guilds SET name = %s, data = %s
                                    WHERE id = %s"""
                                    , (guild.name, json.dumps(data), guild.id))
                        except Exception as e:
                            await self.terminal.Log().WARNING(f"{e}")
                        finally:
                            await self.terminal.Log().INFO(f"Successfully updated database entry for guild: {guild.name}")

                    await conn.commit()

    async def registerUser(self, user):
        if self.config is not None and self.pool is not None:
            async with self.pool.get() as conn:
                async with conn.cursor() as cursor:
                    
                    try:
                        await cursor.execute('''\
                            CREATE TABLE IF NOT EXISTS users 
                            (id BIGINT PRIMARY KEY UNIQUE NOT NULL, name text, data JSON)''')
                    except Exception as e:
                        await self.terminal.Log().WARNING(f"{e}")

                    try:
                        await cursor.execute(f"""\
                            SELECT * FROM users 
                            WHERE id = (%s)
                            """,(user.id))
                    except Exception as e:
                        await self.terminal.Log().WARNING(f"{e}")
                    result = await cursor.fetchone()
                    if result is None:
                        try:
                            result = await cursor.execute(f"""\
                                    INSERT INTO users
                                    (id, name, data)
                                    VALUES( %s, %s, %s)
                                    """, (int(user.id), user.name, json.dumps(self.userTemplate)))
                        except Exception as e:
                            await self.terminal.Log().WARNING(f"{e}")
                        finally:
                            await self.terminal.Log().INFO(f"Successfully created a database entry for member: {user.name}")
                    await conn.commit()

    async def retrieveUser(self, user):
        if self.config is not None and self.pool is not None:
            async with self.pool.get() as conn:
                async with conn.cursor() as cursor:
                    try:
                        await cursor.execute(f"""\
                            SELECT * FROM users 
                            WHERE id = (%s)
                            """,(user.id))
                    except Exception as e:
                        await self.terminal.Log().WARNING(f"{e}")
                    result = await cursor.fetchone()
                    if result is not None:
                        data = [int(result[0]), str(result[1]), json.loads(result[2])]
                        return data
                    else:
                        return None
                           
    async def updateUser(self, user, data: str):
        if self.config is not None and self.pool is not None:
            async with self.pool.get() as conn:
                async with conn.cursor() as cursor:
                    try:
                        await cursor.execute(f"""\
                            SELECT * FROM users 
                            WHERE id = (%s)
                            """,(user.id))
                    except Exception as e:
                        await self.terminal.Log().WARNING(f"{e}")
                    result = await cursor.fetchone()
                    if result is None:
                        try:
                            result = await cursor.execute(f"""\
                                    INSERT INTO users
                                    (id, name, data)
                                    VALUES( %s, %s, %s)
                                    """, (int(user.id), user.name, json.dumps(data)))
                        except Exception as e:
                            await self.terminal.Log().WARNING(f"{e}")
                        finally:
                            await self.terminal.Log().INFO(f"Successfully created a database entry for user: {user.name}")
                        
                    else:
                        try:
                            result = await cursor.execute(f"""\
                                    UPDATE users SET name = %s, data = %s
                                    WHERE id = %s"""
                                    , (user.name, json.dumps(data), user.id))
                        except Exception as e:
                            await self.terminal.Log().WARNING(f"{e}")
                        finally:
                            await self.terminal.Log().INFO(f"Successfully updated database entry for user: {user.name}")

                    await conn.commit()

    async def updateCommandUse(self, user, cog:str, command:str):
        userData = await self.retrieveUser(user)
        _userData = None

        if userData is not None:
            _userData = userData[2]
        
        if _userData is not None:
            _cog = None
            _command = None
            try:
                _cog = _userData['bot']['command_stats'][f'{cog}']
                # _userData['bot']['command_stats'][f'{cog}'][f'{command}'] += 1
            except Exception as e:
                print(e)
                # _userData['bot']['command_stats'][f'{cog}'][f'{command}'] = 1
            if _cog is None:
                _userData['bot']['command_stats'][f'{cog}'] = {}
            try:
                _command = _userData['bot']['command_stats'][f'{cog}'][f'{command}']
            except Exception as e:
                print(e)

            if _command is None:
                try:
                    addition = {f"{command}": 1}
                    _userData['bot']['command_stats'][f'{cog}'].update(addition)
                except Exception as e:
                    print(e)
            else:
                _userData['bot']['command_stats'][f'{cog}'][f'{command}'] += 1

            await self.updateUser(user, _userData)




# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ↓ Local ↓ : WIP
#   › Handles providing local files such as images, video, cogs, py files, etc.
#   › Fill with functions as you need, intended to keep other files clear and let utils do the heavy lifting.
#   › Author: Lino
#   › Date: 15 Nov, 2022
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class Local():
    def __init__(self):
        self.config: Config = None
        self.terminal: Terminal = None

    async def setConfig(self, config):
        if config is not None:
            self.config = config

    async def setTerminal(self, terminal):
        if terminal is not None:
            self.terminal = terminal

    async def GetCogs(self, proposedCogDirectory: str = None):
        cogDirectory = None
        if self.config is not None and proposedCogDirectory is None:
            cogDirectory = self.config.COG_DIRECTORY_PATH
        elif proposedCogDirectory is not None:
            cogDirectory = proposedCogDirectory
        else:
            await self.terminal.Log().CRITICAL(f"Failed to fetch cogs, Config is not set and no path was supplied.")
            return None

        try:
            valid_files = []
            disabled_files = []
            invalid_files = []
            for file in os.listdir(cogDirectory):
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
        except Exception as e:
            await self.terminal.Log().CRITICAL(f"{e}")
            return None

    async def load_extensions(self, discordBot: commands.Bot, debug_mode: bool = False, systemCogs: bool = False):
        """
        Scans for files in the cog directory specified in the Config(). Loads the file if it ends in '.py', and registers files ending in '.disabled' as disabled cogs.
        """
        cogDirectory = self.config.COG_DIRECTORY_PATH
        cogs = await self.GetCogs(cogDirectory)

        if systemCogs:
            cogDirectory = "hangoutcore.SystemCogs"
            cogs = await self.GetCogs(os.path.join(os.path.dirname(__file__), 'SystemCogs'))

        if cogs is not None:
            if len(cogs["valid_files"]) > 0:
                for cog in cogs["valid_files"]:
                    await self.terminal.Log().INFO(f" └ Found {cog}")
                    try:
                        await discordBot.load_extension(f'{cogDirectory}.{cog[:-3]}')
                    except Exception as e:
                        await self.terminal.errorprocessing().CogLoadError(cog, e, debug_mode)
                    else:
                        await self.terminal.Log().INFO(f"  └ successfully loaded {cog}.")
                for cog in cogs["disabled_files"]:
                    await self.terminal.Log().INFO(f" └ Found Disabled file {cog}, Skipping.")
                for cog in cogs["invalid_files"]:
                    if cog == "__pycache__" or "__init__":
                        pass
                    else:
                        await self.terminal.Log().INFO(f" └ Found invalid file {cog}, Skipping.")
                if systemCogs:
                    await self.terminal.Log().INFO(f"Successfully loaded {len(cogs['valid_files'])} System Extension(s).")
                else:
                    await self.terminal.Log().INFO(f"Successfully loaded {len(cogs['valid_files'])} Extension(s).")
                if len(cogs["invalid_files"]) > 0:
                    await self.terminal.Log().WARNING(
                        f"Found {len(cogs['invalid_files'])} invalid extension(s) in the 'cogs' directory. If you believe this is an error please verify each .py file and make sure it is set up as a cog properly, Otherwise you can ignore this message.")
            else:
                await self.terminal.Log().INFO(f"No extensions where found. Skipping...")


    async def GetTicketTranscript(ticketid: str):
        transcriptDirectory = (fr"transcripts\\")
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
    def __init__(self):
        self.INIT_TIME = None
        self.CONFIG = None
        self.SILENT = False

    async def setConfig(self, config=None):
        if config is not None:
            self.CONFIG = config
    
    async def setInitTime(self, time=None):
        if time is not None:
            self.INIT_TIME = time

    async def setSilent(self, silentMode: bool = False):
        self.SILENT = silentMode

    async def print_center(self, s: str):
        """Print on the center of the terminal. Used primarily for decorative purposes."""
        print(s.center(shutil.get_terminal_size().columns))

    async def print_hr(self):
        """Print a horizontal line across the terminal. Used primarily for decorative purposes."""
        print('━'.center(shutil.get_terminal_size().columns, '━'))

    async def clear(self):
        """Clears the terminal."""
        if name == 'nt':
            _ = system('cls')
        else:
            _ = system('clear')

    async def initiate(self, debug: bool = False, bot_setup: bool = False, outdated: bool = False):# 
        """
        Clear's and prepares terminal for bot output.
        """
        
        cfg = self.CONFIG
        start_time = self.INIT_TIME
        await self.clear()
        # print header
        if debug:
            print(Style.BRIGHT + Back.RED, end="\r")
        else:
            print(Style.NORMAL + Fore.BLACK + Back.WHITE, end="\r")
        await self.print_center(" ") # Empty String for spacing
        await self.print_center("██╗░░██╗░█████╗░███╗░░██╗░██████╗░░█████╗░██╗░░░██╗████████╗░█████╗░░█████╗░██████╗░███████╗")
        await self.print_center("██║░░██║██╔══██╗████╗░██║██╔════╝░██╔══██╗██║░░░██║╚══██╔══╝██╔══██╗██╔══██╗██╔══██╗██╔════╝")
        await self.print_center("███████║███████║██╔██╗██║██║░░██╗░██║░░██║██║░░░██║░░░██║░░░██║░░╚═╝██║░░██║██████╔╝█████╗░░")
        await self.print_center("██╔══██║██╔══██║██║╚████║██║░░╚██╗██║░░██║██║░░░██║░░░██║░░░██║░░██╗██║░░██║██╔══██╗██╔══╝░░")
        await self.print_center("██║░░██║██║░░██║██║░╚███║╚██████╔╝╚█████╔╝╚██████╔╝░░░██║░░░╚█████╔╝╚█████╔╝██║░░██║███████╗")
        await self.print_center("╚═╝░░╚═╝╚═╝░░╚═╝╚═╝░░╚══╝░╚═════╝░░╚════╝░░╚═════╝░░░░╚═╝░░░░╚════╝░░╚════╝░╚═╝░░╚═╝╚══════╝")
        await self.print_center("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

        if bot_setup:
            await self.print_center("Bot Setup\n")
        else:
            if cfg is None:
                await self.print_center("// Bot Name Could Not Be Loaded \\")
                await self.print_center("// Bot Version Could Not Be Loaded \\")
            else:
                await self.print_center(str(cfg["bot"]["name"]))
                await self.print_center(str(cfg["bot"]["version"]))

        if start_time is None:
            await self.print_center("// Time Argument Not Provided. \\")
        else:
            await self.print_center(str(start_time))
            await self.print_center(" ") # if we only us /n in the above line for this space then it messes with formatting. I know, dumb.
        
        if debug:
            await self.print_center(f'// Debug Mode Enabled \\\ ')
            await self.print_center('SYS Version ' + str(sys.version))
            await self.print_center('API Version ' + str(sys.api_version))
            await self.print_center('Discord Version ' + str(discord.__version__))
            await self.print_center('HangoutCore Version ' + str(hangoutcore.__version__))

        if outdated:
            print(Style.RESET_ALL + Back.RESET, end="\r")
            print(Style.BRIGHT + Back.RED, end="\r")
            await self.print_center(f"// HangoutCore Is Outdated \\\ ")
        # prep for rest
        print(Style.RESET_ALL + Back.RESET, end="\r")
        await self.print_hr()

    class Log():

        def __init__(self):
            self.loggerName = "HangoutCore"
            self.logger = logging.getLogger(self.loggerName)

        def setLoggerName(self, loggerName):
            self.loggerName = loggerName

        async def DEBUG(self, log: str = None):
            if log is not None:
                if self.logger.level == 10:
                    print(f"[{Fore.BLUE}DEBUG{Fore.RESET}] {log}") # Only print if we need to
                self.logger.debug(log)

        async def INFO(self, log: str = None):
            if log is not None:
                print(f"[{Fore.GREEN}INFO{Fore.RESET}] {log}")
                self.logger.info(log)

        async def WARNING(self, log: str = None):
            if log is not None:
                print(f"[{Fore.YELLOW}WARNING{Fore.RESET}] {log}")
                self.logger.warning(log)

        async def ERROR(self, log: str = None):
            if log is not None:
                print(f"[{Fore.RED}ERROR{Fore.RESET}] {log}")
                self.logger.error(log)

        async def CRITICAL(self, log: str = None):
            if log is not None:
                print(f"{Style.BRIGHT}{Back.RED}[CRITICAL] {log}{Style.RESET_ALL}{Back.RESET}")
                self.logger.critical(log)
    
    async def obfuscateString(self, inputString:str, amount:int=4, obfuscateChar:str='#'):
        """
        Used for allowing our user to recognize a string/token while keeping the rest of it hidden from prying eyes such as a twitch stream, a screen recording or any other public environment.
        """

        outputString = ""
        for i in range(len(inputString)):
            if i < len(inputString) - amount:
                if inputString[i] == '.':
                    outputString = outputString + inputString[i]
                else:
                    outputString = outputString + obfuscateChar
            # elif i == len(inputString) - amount:
            #     outputString = outputString + "-" + inputString[i]
            else:
                outputString = outputString + inputString[i]
        return outputString

    async def EXIT(self, log: str):
        """Closes script with preset formatting for output message."""
        exit(f"{Style.BRIGHT}{Back.RED}[SYSTEM]{Back.RESET}{Fore.RED} {log}{Fore.RESET}{Style.RESET_ALL}")

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # ↓ Custom Error Processing ↓ : WIP
    #   › Intended for when you only need specific data from an error.
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    class errorprocessing():
        def __init__(self):
            self.terminal = Terminal()

        async def CogLoadError(self, file, error, debug_mode):
            """ Error Processing tailored to display the specific error when loading a cog, 
                designed to minimise clutter and lines not relevant."""
            ErrorTraceback = traceback.format_exception(type(error), error, error.__traceback__)
            if debug_mode:
                await self.terminal.Log().ERROR(f"  └ Failed to load {file}\n" + "".join(ErrorTraceback))
            else:
                await self.terminal.Log().ERROR(f"""  └ Failed to load {file}.
                {Back.RED}{error}{Back.RESET}""")

        class CommandError:

            def InsufficientPerms(self, NotifyGuild: bool, command: commands.Command, member: discord.Member):
                ErrorMessage = f"""{member.name} attempted to execute command: {command.name} however they do not have sufficient permissions."""
                self.terminal.Log().ERROR(ErrorMessage)
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
                self.terminal.Log().CRITICAL(
                    f"{guild.name} does not have a Notification Channel set up. They will not be able to recieve Notifications.")
                return f"This Guild does not have a notification channel registered in our database. Please utilize the **/setup** command and try again"


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ↓ Custom Views ↓ : WIP
#   › Used as a way to store frequently used views, such as Confirmation, AutoRole, Ticket, etc.
#   › Author: Lino
#   › Date: 15 Nov, 2022
#   Will eventually move to config... This is so that bot configs can control what views are present based off what they need.
#   Allowing users to quickly transition from bot to bot or even sharing config files without needing them to modify util.py
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class CommonUI(): # use this as a place to store commonly used discord ui objects such as embeds, views, etc.
    
    class ConfirmationView(discord.ui.View):
        def __init__(self):
            super().__init__()
            self.value = None

        @discord.ui.button(label='Confirm', style=discord.ButtonStyle.green)
        async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.send_message('Confirming', ephemeral=True)
            self.value = True
            self.stop()

        @discord.ui.button(label='Cancel', style=discord.ButtonStyle.grey)
        async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.send_message('Cancelling', ephemeral=True)
            self.value = False
            self.stop()

    class PaginationView(discord.ui.View):
        def __init__(self, data, footer, key, description, value, interaction: discord.Interaction, timeout: Optional[float] = 180):
            super().__init__(timeout=timeout)
            self.data = data
            self.dataKey = key
            self.dataDescription = description
            self.dataValue = value
            self.originalInteraction = interaction
            self.messageFooter: str = footer
            self.currentPage: int = 0
            
        def createEmbed(self):
            embedObject = discord.Embed(title = self.data[self.currentPage][self.dataKey], color = discord.Color.from_rgb(47, 49, 54), timestamp=datetime.now())
            embedObject.set_footer(text=f"Page: {self.currentPage+1} of {len(self.data)} - {self.messageFooter}")
            embedObject.description = f"{self.data[self.currentPage][self.dataDescription]}\n"
            for value in self.data[self.currentPage][self.dataValue]:
                embedObject.description = f"{embedObject.description} {value}\n"
            return embedObject

        async def update_message(self):
            self.updateButtons()
            await self.originalInteraction.edit_original_response(embed=self.createEmbed(), view=self)

        def updateButtons(self):
            if (len(self.data)-1) == 0:
                self.first.disabled = True
                self.first.style = discord.ButtonStyle.gray
                self.previous.disabled = True
                self.previous.style = discord.ButtonStyle.gray
                self.last.disabled = True
                self.last.style = discord.ButtonStyle.gray
                self.next.disabled = True
                self.next.style = discord.ButtonStyle.gray
                return

            if self.currentPage == 0:
                self.first.disabled = True
                self.first.style = discord.ButtonStyle.gray
                self.previous.disabled = True
                self.previous.style = discord.ButtonStyle.gray
            else:
                self.first.disabled = False
                self.first.style = discord.ButtonStyle.blurple
                self.previous.disabled = False
                self.previous.style = discord.ButtonStyle.gray

            if self.currentPage == (len(self.data)-1):
                self.last.disabled = True
                self.last.style = discord.ButtonStyle.gray
                self.next.disabled = True
                self.next.style = discord.ButtonStyle.gray
            else:
                self.last.disabled = False
                self.last.style = discord.ButtonStyle.blurple
                self.next.disabled = False
                self.next.style = discord.ButtonStyle.gray

            self.count.label = f"Page: {self.currentPage + 1}"

        @discord.ui.button(label="|<", style=discord.ButtonStyle.blurple)
        async def first(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.defer(ephemeral=True)
            self.currentPage = 0
            await self.update_message()
        
        @discord.ui.button(label="<", style=discord.ButtonStyle.gray)
        async def previous(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.defer(ephemeral=True)
            if self.currentPage != 0:
                self.currentPage -= 1
                await self.update_message()

        @discord.ui.button(label=f"Page: ", style=discord.ButtonStyle.gray, disabled=True)
        async def count(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.defer(ephemeral=True)
            pass # Do whatever your button needs to do here.
        
        @discord.ui.button(label=">", style=discord.ButtonStyle.gray)
        async def next(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.defer(ephemeral=True)
            if self.currentPage != (len(self.data)-1):
                self.currentPage += 1
                await self.update_message()
        
        @discord.ui.button(label=">|", style=discord.ButtonStyle.blurple)
        async def last(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.defer(ephemeral=True)
            self.currentPage = len(self.data)-1
            await self.update_message()

    class GuildBankView(discord.ui.View):
        def __init__(self, interaction, database, data: str = None, footer: str = "System Response", timeout: Optional[float] = 180):
            super().__init__(timeout=timeout)
            self.originalInteraction = interaction
            self.messageFooter: str = footer
            self.data = data
            self.database = database

        def createEmbed(self):
            embedObject = discord.Embed(title = f"{self.data['extras']['guild_economy']['name']}", color = discord.Color.from_rgb(47, 49, 54), timestamp=datetime.now())
            embedObject.set_footer(text=f"{self.messageFooter}")
            embedObject.description = f"`test`"
            return embedObject

        async def update_message(self):
            if type(self.originalInteraction) == discord.Message:
                await self.originalInteraction.edit(content=None, embed=self.createEmbed(), view=self)
            elif type(self.originalInteraction) == discord.Interaction:
                await self.originalInteraction.edit_original_response(embed=self.createEmbed(), view=self)

        @discord.ui.button(label="Check Balance", style=discord.ButtonStyle.blurple)
        async def balance(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.send_message("Balance", ephemeral=True)
            await self.update_message()
        
        @discord.ui.button(label="Send Money", style=discord.ButtonStyle.gray)
        async def send_money(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.send_message("Sending", ephemeral=True)
            await self.update_message()
            userData = await self.database.retreiveUser(interaction.user)
            _userData = userData[2]
            print(_userData)

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
