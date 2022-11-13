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
import click
import discord
import json
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

cfg = None

class bot():
    def __init__(self):
        pass
    
    def GetIntents():
        intents = discord.Intents.default() # Set Bot Intents
        intents.members = True
        intents.message_content = True  
        intents.typing = True
        intents.presences = True
        intents.guilds = True
        return intents

    def GetActivity():
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

    def GetPrefix(bot, message):
        prefixes = cfg["bot"]["prefixes"]

        # Check to see if we are outside of a guild. e.g DM's etc.
        if not message.guild or prefixes is None:
            # Only allow ! to be used in DMs or if no prefix is specified.
            return '!'

        return commands.when_mentioned_or(*prefixes)(bot, message)

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

        class confirmationView(discord.ui.View):
            def __init__(self):
                super().__init__(timeout=3000)
                self.value = None

            @discord.ui.button(label='Confirm', style=discord.ButtonStyle.green)
            async def confirm(self, button: discord.ui.Button, interaction: discord.Interaction):
                self.value = True
                await interaction.response.send_message(f'Removing..', ephemeral=True)
                self.stop()

            @discord.ui.button(label='Cancel', style=discord.ButtonStyle.grey)
            async def cancel(self, button: discord.ui.Button, interaction: discord.Interaction):
                self.value = False
                await interaction.response.send_message(f'Cancelled.', ephemeral=True)
                self.stop()
    
    class CustomButtons():
        def __init__(self):
            pass

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
        
        def load(config=CONFIG_PATH):
            """
            Attempt to load the config from path provided if none provided use CONFIG_PATH,
            if one does not exist then create a new file at CONFIG_PATH and
            copy EXAMPLE_CONFIG into it.
            """
            if os.path.exists(f"{bot.config.CONFIG_DIRECTORY_PATH}/{config}") and os.path.isfile(f"{bot.config.CONFIG_DIRECTORY_PATH}/{config}"):
                with open(f"{bot.config.CONFIG_DIRECTORY_PATH}/{config}") as file:
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
                botPrefix = input("Please enter your bot prefix.: ")
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
                    bot.config.write(value=botPrefix, key1="bot", key2="prefixes", key3=0)
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

        def queue(level, log):
            if level is not None:
                bot.terminal.log_Q.append(f"{level}|{log}")

        def EXIT(log:str):
            """Closes script with preset formatting for output message."""
            exit(f"{Style.BRIGHT}{Back.RED}[SYSTEM]{Back.RESET}{Fore.RED} {log}{Fore.RESET}{Style.RESET_ALL}")

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
            for file in os.listdir(bot.config.COG_DIRECTORY_PATH):
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
                    ticketTranscript = discord.File(fp=bot.local.GetTicketTranscriptPath(ticketid=ticketid),filename=f"{discordChannel.name}.md")
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
                    bot.terminal.log.ERROR(f"{e}")

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
                bot.terminal.log.ERROR(f"  └ Failed to load {file}\n" + "".join(ErrorTraceback))
            else:
                
                bot.terminal.log.ERROR(f"""  └ Failed to load {file}.
                {Back.RED}{error}{Back.RESET}""")

        class CommandError():

            def InsufficientPerms(NotifyGuild: bool, command: commands.Command, member: discord.Member):
                ErrorMessage = f"""{member.name} attempted to execute command: {command.name} however they do not have sufficient permissions."""
                bot.terminal.log.ERROR(ErrorMessage)
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
                bot.terminal.log.CRITICAL(f"{guild.name} does not have a Notification Channel set up. They will not be able to recieve Notifications.")
                return f"This Guild does not have a notification channel registered in our database. Please utilize the **/setup** command and try again"

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

        # async def RegisterGuild(guild: discord.Guild):
        #     async with asqlite.connect(cfg['database']['name']) as conn:
        #         async with conn.cursor() as cursor:
        #             await cursor.execute('''\
        #                 CREATE TABLE IF NOT EXISTS guilds 
        #                 (id integer PRIMARY KEY UNIQUE NOT NULL, name text, guild_notification_channel_id integer, stickymessage_ids text, stickymessage_moderator_id integer, autorole_enabled text NOT NULL DEFAULT 'False', autorole_moderator_id integer, autorole_role_ids text, selfrole_enabled text NOT NULL DEFAULT 'False', selfrole_moderator_id integer, selfrole_role_ids text, guildstats_enabled text NOT NULL DEFAULT 'False', guildstats_channel_id integer, guildstats_options text, voicelobby_enabled text NOT NULL DEFAULT 'False', voicelobby_channel_id integer, guildsuggestions_enabled text NOT NULL DEFAULT 'False', guildsuggestions_channel_id integer, ticketsystem_enabled text NOT NULL DEFAULT 'False', ticketsystem_moderator_id integer, ticketsystem_channel_id integer)''')
        #             await cursor.execute(f"""\
        #                 SELECT * FROM guilds 
        #                 WHERE id = (?)
        #                 """,(guild.id))
        #             result = await cursor.fetchone()
        #             if result is None:
        #                 await cursor.execute(f"""\
        #                     INSERT INTO guilds
        #                     (id, name, autorole_enabled, selfrole_enabled, guildstats_enabled, voicelobby_enabled, guildsuggestions_enabled, ticketsystem_enabled)
        #                     VALUES( ?, ?, 'False', 'False', 'False', 'False', 'False', 'False')
        #                     """, (guild.id, guild.name))
        #                 await conn.commit()
        #             else:
        #                 await cursor.execute(f"""\
        #                     UPDATE guilds SET name = ?
        #                     WHERE id = ?"""
        #                     , (guild.name, guild.id))

        # async def RegisterGuildNotificationChannel(guild: discord.Guild, channel: discord.TextChannel):
        #     async with asqlite.connect(cfg['database']['name']) as conn:
        #         async with conn.cursor() as cursor:
        #             if channel is not None:
        #                 await cursor.execute(f"""\
        #                     UPDATE guilds SET guild_notification_channel_id = ?
        #                     WHERE id = ?
        #                     """, (channel.id, guild.id))
                    
        #             await conn.commit()
        
        # async def RetrieveGuildNotificationChannel(guild: discord.Guild):
        #     async with asqlite.connect(cfg['database']['name']) as conn:
        #         async with conn.cursor() as cursor:
        #             await cursor.execute(f"""SELECT guild_notification_channel_id FROM guilds WHERE id = ?""", (guild.id))
        #             result = await cursor.fetchall()
        #             if result is not None:
        #                 if result[0][0] is not None:
        #                     NotificationChannel = discord.utils.get(guild.channels, id=result[0][0])
        #                     return NotificationChannel
        #                 else:
        #                     return None

        # async def RegisterAutoRoleSystem(guild: discord.Guild, enabled: bool = None, moderator_role: discord.Role = None, role_ids: list[int] = None):
        #     async with asqlite.connect(cfg['database']['name']) as conn:
        #         async with conn.cursor() as cursor:
        #             if enabled is not None:
        #                 await cursor.execute(f"""\
        #                     UPDATE guilds SET autorole_enabled = ?
        #                     WHERE id = ?
        #                     """, (enabled, guild.id))
        #             if moderator_role is not None:
        #                 await cursor.execute(f"""\
        #                     UPDATE guilds SET autorole_moderator_id = ?
        #                     WHERE id = ?
        #                     """, (moderator_role.id, guild.id))
        #             if role_ids is not None:
        #                 await cursor.execute(f"""\
        #                     UPDATE guilds SET autorole_role_ids = ?
        #                     WHERE id = ?
        #                     """, (role_ids, guild.id))
        #             await conn.commit()

        # async def RetrieveAutoRoleSystem(guild: discord.Guild):
        #     async with asqlite.connect(cfg['database']['name']) as conn:
        #         async with conn.cursor() as cursor:
        #             await cursor.execute(f"""SELECT autorole_enabled, autorole_moderator_id, autorole_role_ids FROM guilds WHERE id = ?""", (guild.id))
        #             result = await cursor.fetchall()
        #             if result is not None:
        #                 return result[0]

        # async def RegisterTicketSystem(guild: discord.Guild, enabled: bool = None, category_id: discord.CategoryChannel = None, moderator_role: discord.Role = None):
        #     async with asqlite.connect(cfg['database']['name']) as conn:
        #         async with conn.cursor() as cursor:
        #             if enabled is not None:
        #                 await cursor.execute(f"""\
        #                     UPDATE guilds SET ticketsystem_enabled = ?
        #                     WHERE id = ?
        #                     """, (enabled, guild.id))
                    
        #             if category_id is not None:
        #                 await cursor.execute(f"""\
        #                     UPDATE guilds SET ticketsystem_channel_id = ?
        #                     WHERE id = ?
        #                     """, (category_id.id, guild.id))
                    
        #             if moderator_role is not None:
        #                 await cursor.execute(f"""\
        #                     UPDATE guilds SET ticketsystem_moderator_id = ?
        #                     WHERE id = ?
        #                     """, (moderator_role.id, guild.id))
        #             await conn.commit()

        # async def RetrieveTicketSystem(guild: discord.Guild):
        #     async with asqlite.connect(cfg['database']['name']) as conn:
        #         async with conn.cursor() as cursor:
        #             await cursor.execute(f"""SELECT ticketsystem_enabled, ticketsystem_channel_id, ticketsystem_moderator_id FROM guilds WHERE id = ?""", (guild.id))
        #             result = await cursor.fetchall()
        #             if result is not None:
        #                 return result[0]

cfg = bot.config.load() # Set config once script is loaded.