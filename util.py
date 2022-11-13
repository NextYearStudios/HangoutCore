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

import click
import discord
import json
import os, sys
import shutil

from getpass import getpass
from asyncio import sleep
from colorama import *
from datetime import datetime
from discord.ext import commands
from jproperties import Properties
from typing import Optional
from os import system, name

class bot():

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ↓ Config ↓ : WIP
#   › Used for handling bot configuration file.
#   › Author: Lino
#   › Date: 12 Nov, 2022
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    class config():
        warned = False
        CONFIG_VERSION = 5.6
        CONFIG_PATH = 'config.json' # Path and name of config file.
        CONFIG_DIRECTORY_PATH = "configs" # Name of directory where cogs will be stored.
        COG_DIRECTORY_PATH = "cogs" # Name of directory where cogs will be stored.
        LOG_DIRECTORY_PATH = "logs" # Name of directory where log files will be stored.
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
                "type": "mysql",
                "host": "localhost",
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
                "version" : CONFIG_VERSION, # config version
                "update_reason" : "Initial Creation"
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
                        if cfg['_info']['version'] >= bot.config.CONFIG_VERSION:
                            return cfg
                        else:
                            if not bot.config.warned: # Config is outdated
                                bot.config.warned = True
                                bot.terminal.queue("WARNING",f"{bot.config.CONFIG_PATH} is outdated. Please update it to match the example config provided in config.py")
                            return cfg
                    else:
                        if not bot.config.warned: # Couldn't Find version, file probably outdated or corrupted.
                            bot.config.warned = True
                            bot.terminal.queue("WARNING",f"{bot.config.CONFIG_PATH} is either outdated or corrupt. Please delete the old one and run the bot again to create a new one.")
                        return cfg

        def write(config=CONFIG_PATH, value:str=None, key1:str=None, key2=None, key3=None, key4=None):
            """
            Attempt to write to the config from path provided if none provided use CONFIG_PATH,
            if one does not exist we warn the terminal. We do not create one in the possibility that
            the user misspelled the path provided.
            ***USE CAUTION UPDATING CONFIG WITH THIS, YOU CAN MODIFY CONFIG VALUES TO UNSAFE VALUES THAT WE DO NOT FILTER THROUGH***
            """
            with open(f"{bot.config.CONFIG_DIRECTORY_PATH}/{config}", "r") as botConfig:
                configData = json.load(botConfig)

            if key4 is not None:
                configData[key1][key2][key3][key4] = value
            elif key3 is not None:
                configData[key1][key2][key3] = value
            elif key2 is not None:
                configData[key1][key2] = value
            elif key1 is not None:
                configData[key1] = value
                
            with open(f"{bot.config.CONFIG_DIRECTORY_PATH}/{config}", "w") as botConfig:
                json.dump(configData, botConfig, indent=4)

        def setup(init_time:str):
            """
            This function runs through the process of setting up our bot config with the necessary details. such as bot Name, Token, Authorized Users, Etc.
            """
            print("Oh No! I could not find a config file.")
            if click.confirm("Do you wish to begin the setup process?", default=True):
                bot.terminal.initiate(init_time,False,True) # Clear and prepare terminal for setup process

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
                        bot.terminal.log.ERROR("The token provided did not match. Please try again.")
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
                botVersion = requestBotVersion()
                botToken = requestBotToken()
                botConfigName = requestBotConfigName()
                botConfigDirectory = requestBotConfigDirectory()
                botLogDirectory = requestBotLogDirectory()
                botCogDirectory = requestBotCogDirectory()

                bot.terminal.initiate(init_time,False,True) # refresh terminal
                if click.confirm(f"""Bot Name: {botName}\nBot Description: {botDescription}\nBot Version: ({botVersion})\nBot Token: {"*"*len(botToken)}\nBot Config Name: {botConfigName}\nBot Config Directory: /{botConfigDirectory}\nBot Log Directory: /{botLogDirectory}\nBot Cog Directory: /{botCogDirectory}\nAre the values above accurate?""", default=True):
                    bot.terminal.log.INFO("Creating a properties file to store hangoutcore variables.")
                    p = Properties()
                    p["botConfig"] = botConfigName
                    p["botConfigDirectory"] = botConfigDirectory
                    p["botLogDirectory"] = botLogDirectory
                    p["botCogDirectory"] = botCogDirectory

                    with open(f"hangoutcore.properties", "wb") as hangoutcore_config:
                        p.store(hangoutcore_config, encoding="utf-8") # Store provided information in a properties file.
                    bot.config.CONFIG_PATH = botConfigName
                    bot.config.CONFIG_DIRECTORY_PATH = botConfigDirectory
                    bot.config.COG_DIRECTORY_PATH = botCogDirectory
                    bot.config.LOG_DIRECTORY_PATH = botLogDirectory
                    if not os.path.exists(botConfigDirectory):
                        bot.terminal.log.INFO(f"Creating Config Directory: /{botConfigDirectory}")
                        os.mkdir(botConfigDirectory)
                    else:
                        bot.terminal.log.INFO(f"Config directory already exists, skipping...")
                    if not os.path.exists(botCogDirectory):
                        bot.terminal.log.INFO(f"Creating Cog Directory: /{botCogDirectory}")
                        os.mkdir(botCogDirectory)
                    else:
                        bot.terminal.log.INFO(f"Cog directory already exists, skipping...")
                    if not os.path.exists(botLogDirectory):
                        bot.terminal.log.INFO(f"Creating Log Directory: /{botLogDirectory}")
                        os.mkdir(botLogDirectory)
                    else:
                        bot.terminal.log.INFO(f"Log directory already exists, skipping...")

                    with open(f"{botConfigDirectory}/{botConfigName}", 'w') as file: # Create initial config file.
                        json.dump(bot.config.EXAMPLE_CONFIG, file, indent=4)

                    #return bot.config.load(path=f"{botConfigDirectory}/Config.json")

                    bot.config.write(value=botName, key1="bot", key2="name")
                    bot.config.write(value=botDescription, key1="bot", key2="description")
                    bot.config.write(value=botVersion, key1="bot", key2="version")
                    bot.config.write(value=botToken, key1="bot", key2="token", key3=0)
                else:
                    bot.config.setup(init_time)

            else:
                bot.terminal.log.ERROR("HangoutCore Setup Canceled.")
                bot.terminal.EXIT("Exiting...")

        def exists():
            if os.path.exists("hangoutcore.properties") and os.path.isfile("hangoutcore.properties"):
                with open("hangoutcore.properties", "r+b") as hangoutcore_config: # Access stored variables to locate config file
                    p = Properties()
                    p.load(hangoutcore_config, "utf-8")
                    botConfig = p.get("botConfig").data
                    botConfigDirectory = p.get("botConfigDirectory").data
                    if os.path.exists(f"{botConfigDirectory}/{botConfig}") and os.path.isfile(f"{botConfigDirectory}/{botConfig}"):
                        return True
                    else:
                        return False
            else:
                return False

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ↓ Terminal ↓ : WIP
#   › Used to optimize terminal handling
#   › Author: Lino
#   › Date: 12 Nov, 2022
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    class terminal():
        log_Q = []
        def __init__(self):
            pass
    
        def print_center(s:str):
            print(s.center(shutil.get_terminal_size().columns))

        def print_hr():
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
            if bot_setup:
                bot.terminal.clear()
                if debug:
                    print(Style.BRIGHT + Back.RED,end="\r")
                else:
                    print(Style.NORMAL + Fore.BLACK + Back.WHITE,end="\r")
                bot.terminal.print_center("Bot Setup")
                bot.terminal.print_center("")
                bot.terminal.print_center(str(start_time))
                if debug:
                    bot.terminal.print_center(f'// Debug Mode Enabled \\\ ')
                    bot.terminal.print_center('SYS Version ' + str(sys.version))
                    bot.terminal.print_center('API Version ' + str(sys.api_version))
                    bot.terminal.print_center('Discord Version ' + str(discord.__version__))
                print(Style.RESET_ALL + Back.RESET,end="\r")
                bot.terminal.print_hr()
            elif not bot_setup:
                bot.terminal.clear()
                if debug:
                    print(Style.BRIGHT + Back.RED,end="\r")
                else:
                    print(Style.NORMAL + Fore.BLACK + Back.WHITE,end="\r")
                #bot_terminal.print_center(str(cfg["bot"]["name"]))
                #bot_terminal.print_center(str(cfg["bot"]["version"]))
                bot.terminal.print_center(str(start_time))
                if debug:
                    bot.terminal.print_center(f'// Debug Mode Enabled \\\ ')
                    bot.terminal.print_center('SYS Version ' + str(sys.version))
                    bot.terminal.print_center('API Version ' + str(sys.api_version))
                    bot.terminal.print_center('Discord Version ' + str(discord.__version__))
                print(Style.RESET_ALL + Back.RESET,end="\r")
                bot.terminal.print_hr()
        
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

        def EXIT(log:str):
            """Closes script with preset formatting for output message."""
            exit(f"{Style.BRIGHT}{Back.RED}[SYSTEM]{Back.RESET}{Fore.RED} {log}{Fore.RESET}{Style.RESET_ALL}")