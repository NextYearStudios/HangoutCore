"""
    HangoutCore Main File
    › Please do not modify any of the following content unless you know what you're doing. Modifying the following code and not updating the rest of the bot code to match can/will cause issues.
    › If you do decide to modify the following code please understand that HangoutCore's Dev team, Discord.py's Dev Team nor Python's Dev team are obligated to help you.
    › By Modifying the following code you acknowledge and agree to the text above.
    Last Updated: Jan 21, 2024
    Last Updated by: Lino
    Notes:
        None
"""
import aiofiles
import asyncio
import hangoutcore
import json
import logging
import os
import requests
import shutil
import sys

from datetime import datetime
from hangoutcore.utils import *
from jproperties import Properties
from pathlib import Path
from rich.console import Group
from rich.panel import Panel

def AppConfigExists() -> dict[bool, list]:
    """
    Scan current directory for 'hangoutcore.properties'. We will use this to store necessary information such as config locations.
    """
    terminal.log.INFO(f"Scanning for 'hangoutcore.properties'.") # Notify the user that we will be scanning the directory. This is to make sure they're up to date with any action we perform on their system.
    path = os.getcwd()
    pFiles = []
    dict = {
        "exists": False,
        "files": []
    }
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.properties'):
                pFiles.append(file)
    if len(pFiles) > 0:
        dict["exists"] = True
        dict["files"] = pFiles
        return dict
    else:
        dict["exists"] = False
        return dict

async def main():
    """
    Run through the process of setting up the necessary files for HangoutCore to operate.
    """
    sys.path.append(os.getcwd()) # This expands package finding to our working directory 
    hangoutcore.INIT_TIME = '{0:%d%b%Y_%Hh:%Mm}'.format(datetime.now())
    console = terminal.console
    
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # Section Title: Setup log handling
    
    logDirectory = 'setup-logs'
    
    while not await local.dirExists(logDirectory, True):
        terminal.log.ERROR(f'Unable to locate or create setup log directory.')
    
    logName = str(fr"{logDirectory}/log_{hangoutcore.INIT_TIME}.log").replace(':', '') # We clear any spaces in our log name to avoid incompatabilities
    logEncoding = "utf-8"
    date_format = "%m/%d/%Y %I:%M:%S %p"

    handler = logging.FileHandler(
        filename=logName,
        encoding=logEncoding
    )

    formatter = logging.Formatter("""[%(asctime)s][%(name)s][%(levelname)s] %(message)s""", date_format)
    handler.setFormatter(formatter)
    
    hangoutcore.loggerDiscord.addHandler(handler)
    hangoutcore.loggerHangoutCore.addHandler(handler)
    
    hangoutcore.loggerDiscord.setLevel(20)
    hangoutcore.loggerHangoutCore.setLevel(20)
    
    logFiles = os.listdir(logDirectory)
    
    # Sort log files by date and trim to max of 5
    while len(logFiles) > 5:
        logFiles = os.listdir(logDirectory)
        oldest_file = sorted([ f"{logDirectory}/{file}" for file in os.listdir(logDirectory)], key=os.path.getctime)[0]

        if len(logFiles) > 5:
            os.remove(oldest_file)
        else:
            break
        
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # Section Title: Main Functions for user input
    
    def requestBotName():
        _botName = terminal.input(f"Please Enter The Bot Name: ")
        while _botName == "" or _botName == None:
            terminal.log.WARNING("Bot Name cannot be blank, Please Enter again.")
            _botName = terminal.input(f"Please Enter The Bot Name: ")
        return _botName
    
    def requestBotDescription():
        _botDescription = terminal.input(f"Please Enter The Bot Description: (This can always be changed in the config later.)")
        return _botDescription

    def requestBotPrefix():
        _default = "!"
        _botPrefix = terminal.input(f"(Legacy) Please Enter The Bot Prefix (Default: {_default}): ")
        if _botPrefix == "":
            return _default
        else:
            return _botPrefix

    def requestBotVersion():
        _default = "0.0.0"
        _botVersion = terminal.input(f"Please Enter The Bot Version (Default: {_default}): ")
        if _botVersion == "":
            return _default
        else:
            return _botVersion

    def requestBotToken():
        while True:
            _botToken = terminal.input(f"Please Enter The Bot Token (Input will be blank for your protection)", password = True)
            # get the bot from discord api, so we can verify with the user if it is what they want to use
            terminal.log.INFO(f"Retreiving token status from Discord...")
            _botRequest = requests.get('https://discord.com/api/v10/users/@me',
                                        headers={'Authorization': f'Bot {_botToken}'}).json()
            if _botRequest.get('message') == '401: Unauthorized':
                terminal.log.ERROR("Token Verification Failed: Token does not exist")
                continue
            else:
                terminal.log.INFO(f"Token Verification Passed.")
                terminal.print(Panel(
                            title = r"// Bot Settings \\",
                            subtitle =  '{0:%d%b%Y %Hh:%Mm}'.format(datetime.now()),
                            renderable = Group(
                                "",
                                f"Bot ID: [b]{_botRequest.get('id')}[/b]",
                                f"Bot Name: [b]{_botRequest.get('username')}#{_botRequest.get('discriminator')}[/b]",
                                ""
                            ),
                            # style = f"red on {terminal.colorBG}",
                        ), 
                        style=f"on {terminal.colorBG}", 
                        # justify="center"
                    )
                if terminal.confirm(f"Are you sure you'd like to use the bot listed above?"):
                    break
                else:
                    continue
        return _botToken

    def requestBotConfigName():
        _default = "config.json"
        _ConfigName = terminal.input(f"Please enter your desired config name. (Default: '\{_default}'): \\")
        if _ConfigName == "":
            return _default
        if not _ConfigName.endswith(".json"):
            _ConfigName = _ConfigName + ".json"
        return _ConfigName

    def requestBotConfigDirectory():
        _default = "configs"
        _ConfigDirectory = terminal.input(
            f"Please enter where you'd like to store your configs (Default: '\{_default}'): \\")
        if _ConfigDirectory == "":
            return _default
        else:
            return _ConfigDirectory

    def requestBotLogDirectory():
        _default = "logs"
        _LogDirectory = terminal.input(f"Please enter where you'd like to store your logs (Default: '\{_default}'): \\")
        if _LogDirectory == "":
            return _default
        else:
            return _LogDirectory

    def requestBotCogDirectory():
        _default = "cogs"
        _CogDirectory = terminal.input(f"Please enter where you'd like to store your cogs (Default: '\{_default}'): \\")
        if _CogDirectory == "":
            return _default
        else:
            return _CogDirectory
        
    def requestInstallDefaultCogs():
        if terminal.confirm(f"Would you like to install the Default Cogs?"):
            return True
        else:
            return False

    settingsConfirmed = False
    
    terminal.log.INFO(f"Beginning Setup Process.")
    while not settingsConfirmed:
        
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        # Section Title: Setup terminal
        terminal.clear()
        terminal.print_hr()
        terminal.print_center(" ")
        terminal.print_logo()
        terminal.print_hr()
        
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        # Section Title: Initiate prompts for user input
        
        botToken = requestBotToken()
        # botPrefix = requestBotPrefix() # No longer necessary, here incase needed
        botName = requestBotName()
        botDescription = requestBotDescription()
        botVersion = requestBotVersion()
        botConfigName = requestBotConfigName()
        botConfigDirectory = requestBotConfigDirectory()
        botLogDirectory = requestBotLogDirectory()
        botCogDirectory = requestBotCogDirectory()
        installDefaultCogs = requestInstallDefaultCogs()
        
        terminal.print(Panel(title = r"// Bot Settings \\",
                            subtitle =  '{0:%d%b%Y %Hh:%Mm}'.format(datetime.now()),
                            renderable = Group(
                                "",
                                f"Bot Name: [b]{botName}[/b]",
                                f"Bot Description: [b]{(botDescription[:30] + '... (String only shortened on terminal to avoid clutter.)') if len(botDescription) > 30 else botDescription}[/b]",
                                # f"Bot Prefix: [b]{botPrefix}[/b]",
                                f"Bot Version: [b]{botVersion}[/b]",
                                f"Bot Config Location: [b]\{botConfigDirectory}\{botConfigName}[/b]",
                                f"Bot Cog Location: [b]\{botCogDirectory}[/b]",
                                f"Bot Log Location: [b]\{botLogDirectory}[/b]",
                                f"Install Default Cogs: [b]{installDefaultCogs}[/b]",
                                f"Bot Token: [b]{terminal.obfuscateString(botToken, 6, '*')}[/b]",
                                ""
                            ),
                        ), 
                        style=f"on {terminal.colorBG}")
        if terminal.confirm(f"Please verify the details above and confirm they are correct."):
            
            # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
            # Section Title: Create directories / copy files
            
            terminal.print("")
            terminal.log.INFO(f"Creating a new properties file to store directory settings/locations.")
            
            p = Properties()
            p["botConfig"] = botConfigName
            p["botConfigDirectory"] = botConfigDirectory
            p["botLogDirectory"] = botLogDirectory
            p["botCogDirectory"] = botCogDirectory
            
            if not Path.exists(Path(os.path.dirname(__file__)).parent.joinpath("hangoutcore.properties").absolute()):
                terminal.log.INFO(f"Creating Directory: {Path(os.path.dirname(__file__)).parent.joinpath('hangoutcore.properties').absolute()}")
            else:
                terminal.log.WARNING(f"The following file already exists :'hangoutcore.properties'")
                if terminal.confirm(f"Would you like to override it and continue?"):
                    
                    with open(f"hangoutcore.properties", "wb") as hangoutcore_config:
                        p.store(hangoutcore_config, encoding="utf-8")  # Store provided information in a properties file.
            
            terminal.print("")
            terminal.log.INFO(f"Creating Directories:")
            
            if not Path.exists(Path(os.path.dirname(__file__)).parent.joinpath(botConfigDirectory).absolute()):
                terminal.log.INFO(f"Creating Directory: {Path(os.path.dirname(__file__)).parent.joinpath(botConfigDirectory).absolute()}")
                Path.mkdir(botConfigDirectory, parents = True, exist_ok = True)
            else:
                terminal.log.WARNING(f"Directory '\{botConfigDirectory}' Already Exists, Skipping.")
        
            if not Path.exists(Path(os.path.dirname(__file__)).parent.joinpath(botCogDirectory).absolute()):
                terminal.log.INFO(f"Creating Directory: {Path(os.path.dirname(__file__)).parent.joinpath(botCogDirectory).absolute()}")
                Path.mkdir(botCogDirectory, parents = True, exist_ok = True)
            else:
                terminal.log.WARNING(f"Directory '\{botCogDirectory}' Already Exists, Skipping.")
                
            if not Path.exists(Path(os.path.dirname(__file__)).parent.joinpath(botLogDirectory).absolute()):
                terminal.log.INFO(f"Creating Directory: {Path(os.path.dirname(__file__)).parent.joinpath(botLogDirectory).absolute()}")
                Path.mkdir(botLogDirectory, parents = True, exist_ok = True)
            else:
                terminal.log.WARNING(f"Directory '\{botLogDirectory}' Already Exists, Skipping.")

            if installDefaultCogs:
                terminal.print("")
                terminal.log.INFO(f"Copying Default Cogs to '\{botCogDirectory}'")
                for systemCog in os.listdir(f"{Path(os.path.dirname(hangoutcore.utils.__file__)).parent.joinpath('SystemCogs').absolute()}"):
                    if systemCog.endswith(f".py"):
                        _cogPath = Path(os.path.dirname(__file__)).parent.joinpath(botCogDirectory).absolute()
                        _systemCogPath = Path(os.path.dirname(hangoutcore.utils.__file__)).parent.joinpath('SystemCogs').absolute()
                        
                        if Path.exists(_cogPath.joinpath(systemCog)):
                            terminal.log.WARNING(f"The following file already exists '\{systemCog}'")
                            if terminal.confirm(f"Would you like to override it and continue?"):
                                shutil.copyfile(_systemCogPath.joinpath(systemCog), _cogPath.joinpath(systemCog))
                        else:
                            terminal.log.WARNING(f"Copying the file '\{systemCog}' to '\{botCogDirectory}'")
                            shutil.copyfile(_systemCogPath.joinpath(systemCog), _cogPath.joinpath(systemCog))
            
            # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
            # Section Title: Create new bot config with provided info
            _configDirPath = Path(os.path.dirname(__file__)).parent.joinpath(botConfigDirectory).absolute()
            with open(_configDirPath.joinpath(botConfigName), 'w') as file:
                json.dump(local.botConfig.EXAMPLE_CONFIG, file, indent = 4)
                
            _config = await local.botConfig.get(_configDirPath.joinpath(botConfigName))
            
            _config['bot']['token'] = botToken
            _config['bot']['name'] = botName
            _config['bot']['version'] = botVersion
            _config['bot']['description'] = botDescription
            
            await local.botConfig.save(_configDirPath.joinpath(botConfigName), _config)
            
            break
        else:
            continue

def init():
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        try:
            terminal.print("")
            terminal.log.WARNING(f"User Cancelled Setup")
        except:
            pass
    except SystemExit:
        try:
            terminal.print("")
            terminal.EXIT(f"Exiting...")
        except:
            pass

if __name__ == "__main__":
    init()