"""
    Utility Module for HangoutCore
    › Please do not modify any of the following content unless you know what you're doing. Modifying the following code and not updating the rest of the bot code to match can/will cause issues.
    › If you do decide to modify the following code please understand that HangoutCore's Dev team, Discord.py's Dev Team nor Python's Dev team are obligated to help you.
    › By Modifying the following code you acknowledge and agree to the text above.
    Module Last Updated: November 15, 2022
    Module Last Updated by: Lino
    Notes:
        None
"""
import asyncio
import aiofiles
import aiomysql # Async MYSQL
import click
import ctypes
import discord
import json
import pymysql.cursors
import os, sys
import shutil
import traceback

from getpass import getpass
from asyncio import sleep
from colorama import *
from datetime import datetime
from discord.ext import commands
from jproperties import Properties
from typing import Optional
from os import system, name


#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ↓ Bot ↓ : WIP
#   › Fill with functions as you need, intended to keep other files clear and let utils do the heavy lifting.
#   › Author: Lino
#   › Date: 15 Nov, 2022
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class bot():
    def GetIntents():
        """Retrieves specified bot intents from config file. If the config file is not able to be loaded this sets intents to false just in case."""
        cfg = config.load()
        if cfg is not None:
            intents = discord.Intents.default() # Set Bot Intents
            intents.members = cfg['bot']['intents']['members']
            intents.message_content = cfg['bot']['intents']['message_content']  
            intents.typing = cfg['bot']['intents']['typing']
            intents.presences = cfg['bot']['intents']['presences']
            intents.guilds = cfg['bot']['intents']['guilds']
            return intents
        else:
            terminal.log.WARNING(f"Could not retrieve intents from config. Setting intents to false as a precaution.")
            intents = discord.Intents.default() # Set Bot Intents
            intents.members = False
            intents.message_content = False
            intents.typing = False
            intents.presences = False
            intents.guilds = False
            return intents

    def GetActivity():
        """Retrieves Bot Activity specified in config file. If an activity cannot be loaded from the config then we set it to 'listening to !help'"""
        cfg = config.load()
        if cfg is not None:
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
        else:
            activity = discord.Activity(
                type=discord.ActivityType.listening,
                name="!help"
                )
        return activity

    def GetPrefix(discordBot, message:discord.message):
        """Returns the prefixes specified in the config file. If none can be loaded from config then we set prefix as '!'"""
        cfg = config.load()
        if cfg is not None:
            prefixes = cfg["bot"]["prefixes"]
            
            if prefixes is None:
                return '!'
            return commands.when_mentioned_or(prefixes[0])(bot, message)

    class CustomViews():
        def __init__(self):
            pass
        class autoroleView(discord.ui.View):
            def __init__(self):
                super().__init__(timeout=None)

            @discord.ui.button(label='Game Development', style=discord.ButtonStyle.grey, custom_id='persistent_autorole:gameDev')
            async def green(self, button: discord.ui.Button, interaction: discord.Interaction):
                role = interaction.guild.get_role(868692760524365875)
                user = interaction.user
                if role in user.roles:
                    confirmation = bot.CustomViews.confirmationView()
                    await interaction.response.send_message(f"Are you sure you'd like to remove {role.mention} from your roles?",view=confirmation, ephemeral=True)
                    await confirmation.wait()
                    if confirmation.value is None:
                        await interaction.response.send_message(f"Timed out.", ephemeral=True)
                    elif confirmation.value:
                        await user.remove_roles(role, reason="User removed via AutoRole.")
                        await interaction.response.send_message(f"You've successfully been unassigned {role.mention}.", ephemeral=True)
                    else:
                        return      
                else:
                    await user.add_roles(role, reason="User added via AutoRole.")
                    await interaction.response.send_message(f"You've successfully been assigned {role.mention}.", ephemeral=True)

            @discord.ui.button(label='Bot Development', style=discord.ButtonStyle.grey, custom_id='persistent_autorole:botDev')
            async def grey(self, button: discord.ui.Button, interaction: discord.Interaction):
                role = interaction.guild.get_role(868692545490804746)
                user = interaction.user
                if role in user.roles:
                    confirmation = bot.CustomViews.confirmationView()
                    await interaction.response.send_message(f"Are you sure you'd like to remove {role.mention} from your roles?",view=confirmation, ephemeral=True)
                    await confirmation.wait()
                    if confirmation.value is None:
                        await interaction.response.send_message(f"Timed out.", ephemeral=True)
                    elif confirmation.value:
                        await user.remove_roles(role, reason="User removed via AutoRole.")
                        await interaction.response.send_message(f"You've successfully been unassigned {role.mention}.", ephemeral=True)
                    else:
                        return      
                else:
                    await user.add_roles(role, reason="User added via AutoRole.")
                    await interaction.response.send_message(f"You've successfully been assigned {role.mention}.", ephemeral=True)

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
    
    
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ↓ Audio Handling ↓ : WIP
#   › Used for playing music and keeping the audio function clutter out of the main script.
#   › Author: Lino
#   › Date: 15 Nov, 2022
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    class audio():
        class guildstate():
            def __init__(self):
                self.now_playing = None
                self.playlist = []
                self.skip_votes = set()
                self.volume = int(config.load()["music"]["max_volume"])/100
                
        def verify_opus():
            """
                Looks for opus throughout the system, Attempts to load if found.
            """
            opuslib = ctypes.util.find_library('opus')
            if opuslib is not None:
                try:
                    terminal.log.INFO(f"Loading Opus.")
                    discord.opus.load_opus('opus')
                except Exception as e:
                    terminal.log.ERROR(e)
                else:
                    if not discord.opus.is_loaded():
                        terminal.log.CRITICAL("Opus Failed To Load.")
                    else:
                        terminal.log.INFO("Successfully loaded opus.")
            else:
                terminal.log.WARNING("Could not find Opus, You will not be able to play audio without it.")

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ↓ Config ↓ : WIP
#   › Used for handling bot configuration file.
#   › Author: Lino
#   › Date: 15 Nov, 2022
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class config():

    warned = False
    CONFIG_VERSION = 5.7
    CONFIG_PATH = 'config.json' # Path and name of config file.
    CONFIG_DIRECTORY_PATH = "configs" # Name of directory where cogs will be stored.
    COG_DIRECTORY_PATH = "cogs" # Name of directory where cogs will be stored.
    LOG_DIRECTORY_PATH = "logs" # Name of directory where log files will be stored.
    EXAMPLE_CONFIG = { # Changing this will only matter when the bot creates a new config. Actual config at CONFIG_PATH
        "bot" : {
            "prefixes" : ["!"], #Bot uses this array for prefixes. Add as many as you want, and keep in mind you can include spaces but be careful not to over complicate your prefixes.
            "token" : [""], # If you intend on using any token other than the first in the list, change hangoutcore.py to match.
            "intents" : {
                "members" : True,
                "message_content" : True,
                "typing" : True,
                "presences" : True,
                "guilds" : True
            },
            "status" : {
                "type" : "listening", # Valid Options are competing, playing, listening, streaming, watching
                "name" : "!help", # Activity Name
                "url" : "" # Twitch or Youtube URL if type is Streaming
            },
            "name" : "Bot Name", # Bot name
            "version" : "0.0.0", # Bot version
            "description" : "Bot Description would go here.",
            "developer_guild_id" : 000000000, # Developer guild id for  Used for test commands.
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
            "type": "mysql",
            "host": "localhost",
            "port": 3306,
            "name" : "database", # db name
            "user" : "user",
            "password" : "pass"
        },
        "music" : {
            "max_volume" : 250, # Max Volume
            "vote_skip" : True, # whether vote skip is enabled or not.
            "vote_skip_ratio" : 0.5 # minimum ratio needed for vote skip
        },
        "_info" : { # config info
            "version" : CONFIG_VERSION, # config version
            "update_reason" : "Initial Creation"
        }
    }

    def exists():
        if os.path.exists("hangoutcore.properties") and os.path.isfile("hangoutcore.properties"):
            with open("hangoutcore.properties", "r+b") as hangoutcore_config: # Access stored variables to locate config file
                p = Properties()
                p.load(hangoutcore_config, "utf-8")
                botConfig = p.get("botConfig").data
                botConfigDirectory = p.get("botConfigDirectory").data
                config.CONFIG_PATH = botConfig
                config.CONFIG_DIRECTORY_PATH = botConfigDirectory
                config.COG_DIRECTORY_PATH = p.get("botCogDirectory").data
                config.LOG_DIRECTORY_PATH = p.get("botLogDirectory").data
                if os.path.exists(f"{botConfigDirectory}/{botConfig}") and os.path.isfile(f"{botConfigDirectory}/{botConfig}"):
                    return True
                else:
                    return False
        else:
            return False

    def load(configPath=CONFIG_PATH):
        """
        Attempt to load the config from path provided if none provided uses the config name provided during initiation.
        """
        if config.exists():
            with open(f"{config.CONFIG_DIRECTORY_PATH}/{configPath}") as configFile:
                cfg = json.load(configFile)
                if '_info' in cfg:
                    if cfg['_info']['version'] >= config.CONFIG_VERSION:
                        return cfg
                    else:
                        if not config.warned: # Config is outdated
                            config.warned = True
                            terminal.queue("WARNING",f"{config.CONFIG_PATH} is outdated. Please update it to match the example config provided in config.py")
                            if click.confirm(f"Attention: Your config version {cfg['_info']['version']} is outdated. Would you like to update to {config.CONFIG_VERSION}", default=True):
                                new_cfg = config.EXAMPLE_CONFIG
                                new_cfg['_info']['update_reason'] = f"Update To Config Version {config.CONFIG_VERSION}"
                                for key in cfg['bot'].keys():
                                    new_cfg['bot'][key] = cfg['bot'][key]
                                for key in cfg['database'].keys():
                                    new_cfg['database'][key] = cfg['database'][key]
                                for key in cfg['music'].keys():
                                    new_cfg['music'][key] = cfg['music'][key]
                                with open(f"{config.CONFIG_DIRECTORY_PATH}/{configPath}", "w") as botConfig:
                                    json.dump(new_cfg, botConfig, indent=4)
                            else:
                                return cfg
                else:
                    if not config.warned: # Couldn't Find version, file probably outdated or corrupted.
                        config.warned = True
                        terminal.queue("WARNING",f"{config.CONFIG_PATH} is either outdated or corrupt. Please delete the old one and run the bot again to create a new one.")
                    return cfg

    def setup(init_time:str):
        """
        This function runs through the process of setting up our bot config with the necessary details. such as bot Name, Token, Authorized Users, Etc.
        """
        print("Oh No! I could not find a config file.")
        if click.confirm("Do you wish to begin the setup process?", default=True):
            terminal.initiate(init_time,False,True) # Clear and prepare terminal for setup process

            def requestBotName():
                setup_botName = input(f"Please Enter The Bot Name: ")
                while setup_botName == "":
                    print("Bot Name cannot be blank, Please Enter again.")
                    setup_botName = input(f"Please Enter The Bot Name: ")
                return setup_botName
            def requestBotVersion():
                setup_botVersion = input(f"Please Enter The Bot Version (Default: 0.0.0): ")
                if setup_botVersion == "":
                    setup_botVersion = "0.0.0"
                return setup_botVersion
            def requestBotToken():
                setup_botToken = getpass(f"Please Enter The Bot Token (Input will be blank for your protection): ")
                setup_botToken2 = getpass(f"Please Re-Enter The Bot Token (For Verification): ")
                while setup_botToken != setup_botToken2:
                    terminal.log.ERROR("The token provided did not match. Please try again.")
                    setup_botToken = getpass(f"Please Enter The Bot Token (Input will be blank for your protection): ")
                    setup_botToken2 = getpass(f"Please Re-Enter The Bot Token (For Verification): ")
                return setup_botToken
            def requestBotConfigName():
                botConfigName = input(f"Please enter your desired config name. (Default: config): ")
                if not botConfigName.endswith(".json") and botConfigName == "":
                    botConfigName = "config.json"
                elif not botConfigName.endswith(".json"):
                    botConfigName = botConfigName + ".json"
                return botConfigName
            def requestBotConfigDirectory():
                botConfigDirectory = input(f"Please enter where you'd like to store your configs (Default: /configs): /")
                if botConfigDirectory == "":
                    botConfigDirectory = "configs"
                return botConfigDirectory
            def requestBotLogDirectory():
                botLogDirectory = input(f"Please enter where you'd like to store your logs (Default: /logs): /")
                if botLogDirectory == "":
                    botLogDirectory = "logs"
                return botLogDirectory
            def requestBotCogDirectory():
                botCogDirectory = input(f"Please enter where you'd like to store your cogs (Default: /cogs): /")
                if botCogDirectory == "":
                    botCogDirectory = "cogs"
                return botCogDirectory

            botName = requestBotName()
            botDescription = input("Please enter your bot description, this can be modified in the config file.:\n")
            botPrefix = input("Please enter your bot prefix.: ")
            botVersion = requestBotVersion()
            botToken = requestBotToken()
            botConfigName = requestBotConfigName()
            botConfigDirectory = requestBotConfigDirectory()
            botLogDirectory = requestBotLogDirectory()
            botCogDirectory = requestBotCogDirectory()

            terminal.initiate(init_time,False,True) # refresh terminal
            if click.confirm(f"""Bot Name: {botName}\nBot Description: {botDescription}\nBot Version: ({botVersion})\nBot Token: {"*"*len(botToken)}\nBot Config Name: {botConfigName}\nBot Config Directory: /{botConfigDirectory}\nBot Log Directory: /{botLogDirectory}\nBot Cog Directory: /{botCogDirectory}\nAre the values above accurate?""", default=True):
                terminal.log.INFO("Creating a properties file to store hangoutcore variables.")
                p = Properties()
                p["botConfig"] = botConfigName
                p["botConfigDirectory"] = botConfigDirectory
                p["botLogDirectory"] = botLogDirectory
                p["botCogDirectory"] = botCogDirectory

                with open(f"hangoutcore.properties", "wb") as hangoutcore_config:
                    p.store(hangoutcore_config, encoding="utf-8") # Store provided information in a properties file.
                config.CONFIG_PATH = botConfigName
                config.CONFIG_DIRECTORY_PATH = botConfigDirectory
                config.COG_DIRECTORY_PATH = botCogDirectory
                config.LOG_DIRECTORY_PATH = botLogDirectory
                if not os.path.exists(botConfigDirectory):
                    terminal.log.INFO(f"Creating Config Directory: /{botConfigDirectory}")
                    os.mkdir(botConfigDirectory)
                else:
                    terminal.log.INFO(f"Config directory already exists, skipping...")
                if not os.path.exists(botCogDirectory):
                    terminal.log.INFO(f"Creating Cog Directory: /{botCogDirectory}")
                    os.mkdir(botCogDirectory)
                else:
                    terminal.log.INFO(f"Cog directory already exists, skipping...")
                if not os.path.exists(botLogDirectory):
                    terminal.log.INFO(f"Creating Log Directory: /{botLogDirectory}")
                    os.mkdir(botLogDirectory)
                else:
                    terminal.log.INFO(f"Log directory already exists, skipping...")

                with open(f"{botConfigDirectory}/{botConfigName}", 'w') as file: # Create initial config file.
                    json.dump(config.EXAMPLE_CONFIG, file, indent=4)

                #return config.load(path=f"{botConfigDirectory}/Config.json")

                config.write(value=botName, key1="bot", key2="name")
                config.write(value=botDescription, key1="bot", key2="description")
                config.write(value=botPrefix, key1="bot", key2="prefixes", key3=0)
                config.write(value=botVersion, key1="bot", key2="version")
                config.write(value=botToken, key1="bot", key2="token", key3=0)
            else:
                config.setup(init_time)

        else:
            terminal.log.ERROR("HangoutCore Setup Canceled.")
            terminal.EXIT("Exiting...")

    def write(configPath=CONFIG_PATH, value:str=None, key1:str=None, key2=None, key3=None, key4=None):
        """
        Attempt to write to the config from path provided if none provided use CONFIG_PATH,
        if one does not exist we warn the terminal. We do not create one in the possibility that
        the user misspelled the path provided.
        ***USE CAUTION UPDATING CONFIG WITH THIS, YOU CAN MODIFY CONFIG VALUES TO UNSAFE VALUES THAT WE DO NOT FILTER THROUGH***
        """
        with open(f"{config.CONFIG_DIRECTORY_PATH}/{configPath}", "r") as botConfig:
            configData = json.load(botConfig)

        if key4 is not None:
            configData[key1][key2][key3][key4] = value
        elif key3 is not None:
            configData[key1][key2][key3] = value
        elif key2 is not None:
            configData[key1][key2] = value
        elif key1 is not None:
            configData[key1] = value
            
        with open(f"{config.CONFIG_DIRECTORY_PATH}/{configPath}", "w") as botConfig:
            json.dump(configData, botConfig, indent=4)

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ↓ Database ↓ : WIP
#   › Used to keep the majority of the heavy lifting out of main script, and cog files.
#   › Author: Lino
#   › Date: 15 Nov, 2022
#   › TODO: Add support for SQLITE, POSTGRES, MYSQL and more. to make it easier for first time programmers.
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class database():
    def __init__(self):
        pass

    async def RegisterGuild(loop, guild: discord.Guild):
        cfg = config.load()
        if cfg is not None:
            pool = await aiomysql.create_pool(
                db = cfg["database"]["name"],
                host = cfg["database"]["host"],
                port = cfg["database"]["port"],
                user = cfg["database"]["user"],
                password = cfg["database"]["password"]

            )

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ↓ Local ↓ : WIP
#   › Handles providing local files such as images, video, cogs, py files, etc.
#   › Fill with functions as you need, intended to keep other files clear and let utils do the heavy lifting.
#   › Author: Lino
#   › Date: 15 Nov, 2022
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

    async def load_extensions(discordBot:discord.Client, debug_mode:bool=False):
        """
        Scans for files in the cog directory specified in the config. Loads the file if it ends in '.py', and registers files ending in '.disabled' as disabled cogs.
        """
        cogs = local.GetCogs()

        for cog in cogs["valid_files"]:
            terminal.log.INFO(f" └ Found {cog}")
            try:
                await discordBot.load_extension(f'{config.COG_DIRECTORY_PATH}.{cog[:-3]}')
            except Exception as e:
                terminal.errorprocessing.CogLoadError(cog, e, debug_mode)
            else:
                terminal.log.INFO(f"  └ successfully loaded {cog}.")
        for cog in cogs["disabled_files"]:
            terminal.log.INFO(f" └ Found Disabled file {cog}, Skipping.")
        for cog in cogs["invalid_files"]:
            if cog == "__pycache__" or "__init__":
                pass
            else:
                terminal.log.INFO(f" └ Found invalid file {cog}, Skipping.")
        terminal.log.INFO(f"Successfully loaded {len(cogs['valid_files'])} extension(s).")
        if len(cogs["invalid_files"]) > 0:
            terminal.log.WARNING(f"Found {len(cogs['invalid_files'])} invalid extension(s) in the 'cogs' directory. If you believe this is an error please verify each .py file and make sure it is set up as a cog properly, Otherwise you can ignore this message.")

    async def GetTicketTranscript(ticketid:str):
        transcriptDirectory = (f"transcripts\\")
        if os.path.exists(f"{transcriptDirectory}{ticketid}.md"):
            with open(f"{transcriptDirectory}{ticketid}.md", 'rb') as transcriptFile:
                return transcriptFile

    def GetTicketTranscriptPath(ticketid:str):
        transcriptDirectory = (f"transcripts\\")
        if os.path.exists(f"{transcriptDirectory}{ticketid}.md"):
            return os.path.abspath(f"{transcriptDirectory}{ticketid}.md")

    async def CreateTicketTranscript(ticketid:str, discordChannel: discord.channel, ticketAuthor: discord.User):
        transcriptDirectory = (f"transcripts\\")
        if not os.path.exists(f"{transcriptDirectory}{ticketid}.md"):
            ticketTranscript:discord.File
            async with aiofiles.open(f"{transcriptDirectory}{ticketid}.md", 'a', encoding="utf-8") as transcriptFile:
                await transcriptFile.write(f"# Official Transcript for Ticket ID: {ticketid}:\n")
                await transcriptFile.write(f"---\n")
                await transcriptFile.write(f"## **BEGIN TRANSCRIPT** \n\n")
                async for message in discordChannel.history(limit = None, oldest_first = True):
                    created = datetime.strftime(message.created_at, "%m/%d/%Y at %H:%M:%S")
                    if message.edited_at:
                        edited = datetime.strftime(message.edited_at, "%m/%d/%Y at %H:%M:%S")
                        await transcriptFile.write(f"**{message.author} on {created}**: > {message.clean_content} (Edited at {edited})\n")
                        if len(message.embeds) > 0:
                            for embed in message.embeds:
                                await transcriptFile.write(f"- Embed: {str(embed)}\n")
                        if len(message.attachments) > 0:
                            for attachment in message.attachments:
                                await transcriptFile.write(f"- File Type: {attachment.content_type} [{attachment.filename}]({attachment.url})\n")
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
                                await transcriptFile.write(f"- File: \nType: {attachment.content_type}\nURL: [{attachment.filename}]({attachment.url})\n")
                await transcriptFile.write(f"\n## **END TRANSCRIPT** \n")
                await transcriptFile.write(f"---\n")
                generated = datetime.now().strftime("%m/%d/%Y at %H:%M:%S")
                await transcriptFile.write(f"*Generated at {generated} by {ticketAuthor.name}#{ticketAuthor.discriminator} AKA {ticketAuthor.display_name}*\n*Date Formatting: MM/DD/YY*\n*Time Zone: UTC*")
                ticketTranscript = discord.File(fp=local.GetTicketTranscriptPath(ticketid=ticketid),filename=f"{discordChannel.name}.md")
                #os.close(transcriptFile)
                #ticketTranscript.close()
                await transcriptFile.close()
                return ticketTranscript

    def DeleteTicketTranscript(ticketid:str):
        transcriptDirectory = (f"transcripts\\")
        if os.path.exists(f"{transcriptDirectory}{ticketid}.md"):
            try:
                os.remove(f"{transcriptDirectory}{ticketid}.md")
            except Exception as e:
                terminal.log.ERROR(f"{e}")

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ↓ Terminal ↓ : WIP
#   › Used to optimize terminal handling
#   › Author: Lino
#   › Date: 15 Nov, 2022
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class terminal():
    log_Queue = []

    def print_center(s:str):
        """Print on the center of the terminal. Used primarily for decorative purposes."""
        print(s.center(shutil.get_terminal_size().columns))

    def print_hr():
        """Print a horizontal line across the terminal. Used primarily for decorative purposes."""
        print('━'.center(shutil.get_terminal_size().columns, '━'))

    def clear():
        """Clears the terminal."""
        if name =='nt':
            _ = system('cls')    
        else: 
            _ = system('clear')

    def initiate(start_time:str, debug:bool=False, bot_setup:bool=False):
        """
        Clear's and prepares terminal for bot output.
        """
        cfg = config.load()
        if cfg is not None:
            if bot_setup:
                terminal.clear()
                if debug:
                    print(Style.BRIGHT + Back.RED,end="\r")
                else:
                    print(Style.NORMAL + Fore.BLACK + Back.WHITE,end="\r")
                terminal.print_center("Bot Setup")
                terminal.print_center("")
                terminal.print_center(str(start_time))
                if debug:
                    terminal.print_center(f'// Debug Mode Enabled \\\ ')
                    terminal.print_center('SYS Version ' + str(sys.version))
                    terminal.print_center('API Version ' + str(sys.api_version))
                    terminal.print_center('Discord Version ' + str(discord.__version__))
                print(Style.RESET_ALL + Back.RESET,end="\r")
                terminal.print_hr()
            elif not bot_setup:
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

    class log():
        def DEBUG(log:str):
            print(f"[{Fore.BLUE}DEBUG{Fore.RESET}] {log}")

        def INFO(log:str):
            print(f"[{Fore.GREEN}INFO{Fore.RESET}] {log}")

        def WARNING(log:str):
            print(f"[{Fore.YELLOW}WARNING{Fore.RESET}] {log}")
        
        def ERROR(log:str):
            print(f"[{Fore.RED}ERROR{Fore.RESET}] {log}")

        def CRITICAL(log:str):
            print(f"{Style.BRIGHT}{Back.RED}[CRITICAL] {log}{Style.RESET_ALL}{Back.RESET}")

    def queue(level, log):
        if level is not None:
            terminal.log_Queue.append(f"{level}|{log}")

    def EXIT(log:str):
        """Closes script with preset formatting for output message."""
        exit(f"{Style.BRIGHT}{Back.RED}[SYSTEM]{Back.RESET}{Fore.RED} {log}{Fore.RESET}{Style.RESET_ALL}")
        
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
                terminal.log.ERROR(f"  └ Failed to load {file}\n" + "".join(ErrorTraceback))
            else:
                
                terminal.log.ERROR(f"""  └ Failed to load {file}.
                {Back.RED}{error}{Back.RESET}""")

        class CommandError():

            def InsufficientPerms(NotifyGuild: bool, command: commands.Command, member: discord.Member):
                ErrorMessage = f"""{member.name} attempted to execute command: {command.name} however they do not have sufficient permissions."""
                terminal.log.ERROR(ErrorMessage)
                return ErrorMessage
        
        async def NotifyGuildStaff(guild: discord.Guild, color=discord.Color.from_rgb(47, 49, 54), title: str="Notification Title", message: str="Notification Message"):
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
                terminal.log.CRITICAL(f"{guild.name} does not have a Notification Channel set up. They will not be able to recieve Notifications.")
                return f"This Guild does not have a notification channel registered in our database. Please utilize the **/setup** command and try again"
