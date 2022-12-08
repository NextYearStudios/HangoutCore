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
import anyio
import asyncio
import click
import sys

from datetime import datetime
from hangoutcore.util import *
from hangoutcore.bot import HangoutCoreBot

async def main():
    argv = list(set(sys.argv[1:])) # Setting a list to a set and then back to a list will remove any duplicates as a precaution.
    debug = False
    config = None
    token = -1
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
        
    print(debug)
    print(config)
    print(token)

    exampleToken = "1234567890.1234567890.1234567890"

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

    obToken = obfuscateString(exampleToken, 4, '*')

    init_time = '{0:%d%b%Y %Hh:%Mm}'.format(datetime.now())
    config = Config()
    if freshInstall:
        config.setup(manual=True)
    elif not config.appConfigExists():
        config.setup()
    config.init() # Load our hangoutcore.properties file and setup config variables.
    config.load() # Load our bot config here
    
    Terminal().initiate(config)
    
def init():
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        Terminal().Log().CRITICAL(f"Please refrain from using CTRL+C to shutdown bot.")
        # Here we'd make sure database exited/saved gracefully as well as any other essential process that may suffer from stopping abruptly.
        Terminal().Log().CRITICAL(f"Shutting Down...")
        sys.exit(0)
    # except:
    #     Terminal().Log().CRITICAL(f"Shutting Down...")
    #     sys.exit(0)

if __name__ == "__main__":
    init()