"""
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    HangoutCore Main Script
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
import click
import discord
import logging
import logging.handlers
import sys

from datetime import datetime
from hangoutcore.util import *
from hangoutcore.bot import HangoutCoreBot

async def main():
    init_time = '{0:%d%b%Y %Hh:%Mm}'.format(datetime.now())
    argv = list(set(sys.argv[1:])) # Setting a list to a set and then back to a list will remove any duplicates as a precaution.
    debug = False
    config = None
    token = -1
    silent = False
    freshInstall = False

    if '-h' in sys.argv or '--help' in argv:
        print(f"""

    ██╗░░██╗░█████╗░███╗░░██╗░██████╗░░█████╗░██╗░░░██╗████████╗░█████╗░░█████╗░██████╗░███████╗
    ██║░░██║██╔══██╗████╗░██║██╔════╝░██╔══██╗██║░░░██║╚══██╔══╝██╔══██╗██╔══██╗██╔══██╗██╔════╝
    ███████║███████║██╔██╗██║██║░░██╗░██║░░██║██║░░░██║░░░██║░░░██║░░╚═╝██║░░██║██████╔╝█████╗░░
    ██╔══██║██╔══██║██║╚████║██║░░╚██╗██║░░██║██║░░░██║░░░██║░░░██║░░██╗██║░░██║██╔══██╗██╔══╝░░
    ██║░░██║██║░░██║██║░╚███║╚██████╔╝╚█████╔╝╚██████╔╝░░░██║░░░╚█████╔╝╚█████╔╝██║░░██║███████╗
    ╚═╝░░╚═╝╚═╝░░╚═╝╚═╝░░╚══╝░╚═════╝░░╚════╝░░╚═════╝░░░░╚═╝░░░░╚════╝░░╚════╝░╚═╝░░╚═╝╚══════╝
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[-c, --config : string  ] Load the specified config, Also sets as default. If the specified config cannot be found, return to previous config as a precaution.
[-d, --debug  : bool    ] Enable debug mode for more information to be displayed in the terminal. Changes log mode to DEBUG.
[-n, --new    : empty   ] Manually put HangoutCore in a setup state in order to create a new configuration. Sets the new config as default.
[-s, --silent : bool    ] Enable/Disable to have information sent to log only, or terminal and log(). Useful for running as a service since there's no access to terminal.
[-t, --token  : integer ] Specify which token to use if you're using multiple. Allows user to skip token choice prompt.
        """) # Formatting looks ugly I know. Looks pretty good in the terminal though...
        sys.exit(0)

    if len(argv) >= 1:
        # Need to create a pre-check to make sure the variables exist after the arguments.
        # otherwise we run into the issue of causing errors down the road that we could easily avoid.
        if '-d' in argv:
            argvPos = argv.index('-d')
            debug = argv[argvPos + 1]
            argv.pop(argvPos + 1)
            argv.pop(argvPos)
        elif '--debug' in argv:
            argvPos = argv.index('--debug')
            debug = argv[argvPos + 1]
            argv.pop(argvPos + 1)
            argv.pop(argvPos)

        if '-s' in argv:
            argvPos = argv.index('-s')
            silent = argv[argvPos + 1]
            argv.pop(arvPos + 1)
            argv.pop(argv)
        elif '--silent' in argv:
            argvPos = argv.index('--silent')
            silent = argv[argvPos + 1]
            argv.pop(argvPos + 1)
            argv.pop(argv)

        if '-c' in argv:
            argvPos = argv.index('-c')
            config = argv[argvPos + 1]
            argv.pop(argvPos + 1)
            argv.pop(argvPos)
        elif '--config' in argv:
            argvPos = argv.index('--config')
            config = argv[argvPos + 1]
            argv.pop(argvPos + 1)
            argv.pop(argvPos)

        if '-t' in argv:
            argvPos = argv.index('-t')
            token = argv[argvPos + 1]
            argv.pop(argvPos + 1)
            argv.pop(argvPos)
        elif '--token' in argv:
            argvPos = argv.index('--token')
            token = argv[argvPos + 1]
            argv.pop(argvPos + 1)
            argv.pop(argvPos)

        if '-n' in argv:
            argvPos = argv.index('-n')
            freshInstall = True
            argv.pop(argvPos)
        
        # Final check to make sure there's no invalid arguments that we missed.
        if len(argv) > 0:
            Terminal().Log().CRITICAL(f"There appears to be invalid arguments in your entry. Please Double check your spelling and try again.\nYour input: {' '.join(sys.argv)}\nInvalid argument(s): {' '.join(argv)}")
            sys.exit(0)
        
    # This function will be moved to util
    def obfuscateString(inputString:str, amount:int=4, obfuscateChar:str='#'):
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
            elif i == len(inputString) - amount:
                outputString = outputString + "-" + inputString[i]
            else:
                outputString = outputString + inputString[i]
        return outputString

    
    config = Config()
    terminal = Terminal()

    # This may seem redundant but this allows us to share our instance of the Terminal class across HangoutCore. 
    # Any Modifications we make to our instance will be immediately available to the rest of HangoutCore
    config.setConfigTerminal(terminal) 
    
    if freshInstall:
        config.setup(manual=True)
    elif not config.appConfigExists():
        config.setup()

    if config.init(): # if hangoutcore.properties exists, load it and set our variables
        config.load(config) # Load our bot config based off these variables ^
    else:
        # We should almost never get to this. BUT if we do then we need to make sure the user knows about it to avoid looking elsewhere.
        terminal.Log().Critical(f"hangoutcore.properties could not be found. This means our setup failed, or we do not have permissions to create/access it. Please restart HangoutCore and try again.")
    
    # Setup Logging for HangoutCore and Discord.py

    loggerDiscord = logging.getLogger("discord")
    loggerHangoutCore = logging.getLogger("HangoutCore")
    loggerRoot = logging.getLogger("root")

    # We assume that the bot successfully loaded our config. otherwise this wont work the way we intend
    logName = str(f"{config.getLogDirectoryPath()}/log_{init_time.replace(' ', '_')}.log") # We clear any spaces in our log name to avoid incompatabilities
    logEncoding = "utf-8"
    date_format = "%m/%d/%Y %I:%M:%S %p"

    handler = logging.FileHandler(
        filename=logName,
        encoding=logEncoding
    )

    # Logging Level INFO | 0 : NOTSET, 10 : DEBUG, 20 : INFO, 30 : WARNING, 40 : ERROR, 50 : CRITICAL
    if debug:
        loggerDiscord.setLevel(10)
        loggerHangoutCore.setLevel(10)
    else:
        loggerDiscord.setLevel(20)
        loggerHangoutCore.setLevel(20)

    formatter = logging.Formatter("""[%(asctime)s][%(name)s][%(levelname)s] %(message)s""", date_format)
    handler.setFormatter(formatter)
    
    loggerDiscord.addHandler(handler)
    loggerHangoutCore.addHandler(handler)

    # Initiate Terminal class with some necessary variables

    terminal.setConfig(config.getConfig())
    terminal.setInitTime(init_time)
    terminal.setSilent(silent)


    terminal.initiate(debug=debug, bot_setup=False)

    # Begin Prepping to launch Bot
    terminal.Log.INFO(type(config.CONFIG["bot"["token"]]))

    # if token != -1:
    #     config.CONFIG["bot"]["token"]

    # obToken = obfuscateString(exampleToken, 4, '*')

def init():
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        Terminal().Log().CRITICAL(f"Please refrain from using CTRL+C to shutdown bot.")
        # Here we'd make sure database exited/saved gracefully as well as any other essential process that may suffer from stopping abruptly.
        Terminal().EXIT(f"Shutting Down...")
        sys.exit(0)
    # except Exception as e:
    #     Terminal().Log().ERROR(e)
    #     Terminal().EXIT(f"Shutting Down...")
    # except:
    #     Terminal().Log().CRITICAL(f"Shutting Down...")
    #     sys.exit(0)

if __name__ == "__main__":
    init()