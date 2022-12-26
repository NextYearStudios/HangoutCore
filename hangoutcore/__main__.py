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
import aiomysql
import click
import discord
import logging
import logging.handlers
import sys

from aiohttp import ClientSession
from datetime import datetime
from hangoutcore.util import *
from hangoutcore.bot import HangoutCoreBot
from questionnaire import Questionnaire

async def main():
    init_time = '{0:%d%b%Y %Hh:%Mm}'.format(datetime.now())
    argv = sys.argv[1:] 
    argv_debug = False
    argv_configName = None
    argv_token = -1
    argv_silent = False
    argv_freshInstall = False
    sys.path.append(os.getcwd()) # This expands package finding to our working directory 
    

    config = Config()
    terminal = Terminal()

    if '-h' in argv or '--help' in argv:
        print(f"""

    ██╗░░██╗░█████╗░███╗░░██╗░██████╗░░█████╗░██╗░░░██╗████████╗░█████╗░░█████╗░██████╗░███████╗
    ██║░░██║██╔══██╗████╗░██║██╔════╝░██╔══██╗██║░░░██║╚══██╔══╝██╔══██╗██╔══██╗██╔══██╗██╔════╝
    ███████║███████║██╔██╗██║██║░░██╗░██║░░██║██║░░░██║░░░██║░░░██║░░╚═╝██║░░██║██████╔╝█████╗░░
    ██╔══██║██╔══██║██║╚████║██║░░╚██╗██║░░██║██║░░░██║░░░██║░░░██║░░██╗██║░░██║██╔══██╗██╔══╝░░
    ██║░░██║██║░░██║██║░╚███║╚██████╔╝╚█████╔╝╚██████╔╝░░░██║░░░╚█████╔╝╚█████╔╝██║░░██║███████╗
    ╚═╝░░╚═╝╚═╝░░╚═╝╚═╝░░╚══╝░╚═════╝░░╚════╝░░╚═════╝░░░░╚═╝░░░░╚════╝░░╚════╝░╚═╝░░╚═╝╚══════╝
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[-c, --config : string  ] Load the specified config, Also sets as default. 
                          If the specified config cannot be found, return to previous config as a precaution.
[-d, --debug  : bool    ] Enable debug mode for more information to be displayed in the terminal. 
                          Changes log mode to DEBUG.
[-n, --new    : empty   ] Manually put HangoutCore in a setup state in order to create a new configuration. 
                          Sets the new config as default.
[-s, --silent : bool    ] Enable/Disable to have information sent to log only, or terminal and log().
                          Useful for running as a service since there's no access to terminal.
[-t, --token  : integer ] Specify which token to use if you're using multiple. Allows user to skip token choice prompt.
        """) # Formatting looks ugly I know. Looks pretty good in the terminal though...
        sys.exit(0)

    def invalidArg(arg):
        return terminal.Log().WARNING(f"You need to specify a value for the argument provided. arguments: {arg}")

    if len(argv) >= 1:
        # Need to create a pre-check to make sure the variables exist after the arguments.
        # otherwise we run into the issue of causing errors down the road that we could easily avoid.
        if '-d' in argv:
            argvPos = argv.index('-d')
            try:
                if argv[argvPos + 1].lower() == "true":
                    argv_debug = True
                else:
                    argv_debug = False
            except IndexError:
                invalidArg(arg = '-d')
                return
            argv.pop(argvPos + 1)
            argv.pop(argvPos)
        elif '--debug' in argv:
            argvPos = argv.index('--debug')
            try:
                if argv[argvPos + 1].lower() == "true":
                    argv_debug = True
                else:
                    argv_debug = False
            except IndexError:
                invalidArg('--debug')
                return 
            argv.pop(argvPos + 1)
            argv.pop(argvPos)

        if '-s' in argv:
            argvPos = argv.index('-s')
            
            try:
                if argv[argvPos + 1].lower() == "true":
                    argv_silent = True
                else:
                    argv_silent = False
            except IndexError:
                invalidArg('-s')
                return
            argv.pop(argvPos + 1)
            argv.pop(argv)
        elif '--silent' in argv:
            argvPos = argv.index('--silent')
            try:
                if argv[argvPos + 1].lower() == "true":
                    argv_silent = True
                else:
                    argv_silent = False
            except IndexError:
                invalidArg('--silent')
                return
            argv.pop(argvPos + 1)
            argv.pop(argv)

        if '-c' in argv:
            argvPos = argv.index('-c')
            try:
                argv_configName = argv[argvPos + 1]
            except IndexError:
                invalidArg('-c')
                return
            argv.pop(argvPos + 1)
            argv.pop(argvPos)
        elif '--config' in argv:
            argvPos = argv.index('--config')
            try:
                argv_configName = argv[argvPos + 1]
            except IndexError:
                invalidArg('--config')
                return
            argv.pop(argvPos + 1)
            argv.pop(argvPos)

        if '-t' in argv:
            argvPos = argv.index('-t')
            try:
                argv_token = int(argv[argvPos + 1])
            except IndexError:
                invalidArg('-t')
                return
            argv.pop(argvPos + 1)
            argv.pop(argvPos)
        elif '--token' in argv:
            argvPos = argv.index('--token')
            try:
                argv_token = argv[argvPos + 1]
            except IndexError:
                invalidArg('--token')
                return
            argv_token = int(argv[argvPos + 1])
            argv.pop(argvPos + 1)
            argv.pop(argvPos)

        if '-n' in argv:
            argvPos = argv.index('-n')
            argv_freshInstall = True
            argv.pop(argvPos)
        
        # Final check to make sure there's no invalid arguments that we missed.
        if len(argv) > 0:
            terminal.Log().CRITICAL(f"There appears to be invalid arguments in your entry. Please Double check your spelling and try again.\nYour input: {' '.join(sys.argv)}\nInvalid argument(s): {' '.join(argv)}")
            sys.exit(0)
    
    loggerDiscord = logging.getLogger("discord")
    loggerHangoutCore = logging.getLogger("HangoutCore")
    loggerRoot = logging.getLogger("root")

    # Logging Level INFO | 0 : NOTSET, 10 : DEBUG, 20 : INFO, 30 : WARNING, 40 : ERROR, 50 : CRITICAL
    if argv_debug:
        loggerDiscord.setLevel(10)
        loggerHangoutCore.setLevel(10)
    else:
        loggerDiscord.setLevel(20)
        loggerHangoutCore.setLevel(20)

    # This function will be moved to util
    
    

    # This may seem redundant but this allows us to share our instance of the Terminal class across HangoutCore. 
    # Any Modifications we make to our instance will be immediately available to the rest of HangoutCore
    await config.setConfigTerminal(terminal) 
    
    if argv_freshInstall:
        await config.setup(manual=True)
    elif not await config.appConfigExists():
        await config.setup()

    if await config.init(): # if hangoutcore.properties exists, load it and set our variables
        await config.load(argv_configName) # Load our bot config based off these variables ^
    else:
        # We should almost never get to this. BUT if we do then we need to make sure the user knows about it to avoid looking elsewhere.
        terminal.Log().Critical(f"hangoutcore.properties could not be found. This means our setup failed, or we do not have permissions to create/access it. Please restart HangoutCore and try again.")
    
    # Setup Logging for HangoutCore and Discord.py

    # We assume that the bot successfully loaded our config. otherwise this wont work the way we intend
    logName = str(fr"{await config.getLogDirectoryPath()}/log_{init_time.replace(' ', '_')}.log").replace(':', '') # We clear any spaces in our log name to avoid incompatabilities
    logEncoding = "utf-8"
    date_format = "%m/%d/%Y %I:%M:%S %p"

    handler = logging.FileHandler(
        filename=logName,
        encoding=logEncoding
    )

    formatter = logging.Formatter("""[%(asctime)s][%(name)s][%(levelname)s] %(message)s""", date_format)
    handler.setFormatter(formatter)
    
    loggerDiscord.addHandler(handler)
    loggerHangoutCore.addHandler(handler)

    await terminal.setConfig(config.CONFIG)
    await terminal.setInitTime(init_time)
    await terminal.setSilent(argv_silent)


    # Initiate Terminal class with some necessary variables
    
    response = requests.get(f"https://pypi.org/pypi/hangoutcore/json")
    latest_version = response.json()['info']['version']
    if hangoutcore.__version__ != latest_version:
        await terminal.initiate(debug=argv_debug, bot_setup=False, outdated=True)
        await terminal.Log().WARNING(f"HangoutCore is out of date. Please update to the latest version using 'pip install -U hangoutcore'.")
        await terminal.Log().WARNING(f"Current Version: {hangoutcore.__version__} | HangoutCore Latest Version: {latest_version}")
    else:
        await terminal.initiate(debug=argv_debug, bot_setup=False)
        



    logFiles = os.listdir(config.LOG_DIRECTORY_PATH)
    
    while len(logFiles) > 5:
        logFiles = os.listdir(config.LOG_DIRECTORY_PATH)
        oldest_file = sorted([ f"{config.LOG_DIRECTORY_PATH}/{f}" for f in os.listdir(config.LOG_DIRECTORY_PATH)], key=os.path.getctime)[0]

        if len(logFiles) > 5:
            os.remove(oldest_file)
        else:
            break

    # Begin Prepping to launch Bot

    configTokens = config.CONFIG['bot']['token']
    botToken = None

    if type(configTokens) == str:
        await terminal.Log().DEBUG(f"Token entry in config file is a string.")
        botToken = configTokens
    elif type(configTokens) == list:
        await terminal.Log().DEBUG(f"Token entry in config file is a list.")
        if argv_token == -1:
            if argv_silent or len(configTokens) == 1:
                await terminal.Log().DEBUG(f"Found 1 token or silent mode is enabled. Using Token 0.")
                botToken = configTokens[0] # Default to the first token
            else:
                await terminal.Log().DEBUG(f"Multiple tokens were found, Prompting user to choose.")
                filteredTokens = []
                for token in configTokens:
                    filteredTokens.append(await terminal.obfuscateString(token, 6, '*'))
                q = Questionnaire()
                q.one("token", *filteredTokens,
                prompt=f"Current Config Loaded: {await config.getConfigDirectoryPath()}/{await config.getConfigPath()}\nWhich of the following tokens would you like to use?")
                q.run()
                tokenChoice = filteredTokens.index(q.answers.get('token'))
                botToken = configTokens[tokenChoice]
        else:
            lenTokens = len(configTokens)
            if argv_token > lenTokens:
                await terminal.Log().CRITICAL(f"You attempted to load token #{argv_token}. You only have {lenTokens} Tokens listed in your config file.")
                sys.exit(1)
            else:
                try:
                    await terminal.Log().DEBUG(f"User requested Token {argv_token}.")
                    botToken = configTokens[argv_token]
                except IndexError:
                    await terminal.Log().ERROR(f"You attempted to specify a token that's out of range. Your config only has {len(config.CONFIG['bot']['token'])} token(s). Please check your input and try again.")
                    sys.exit(1)
    
    # Launch Bot
    
    async with ClientSession() as our_client:
        activity = await config.getBotActivity()
        intents = await config.getBotIntents()
        prefixes = await config.getBotPrefix()
        # db_pool = await aiomysql.create_pool(
        #         db       = config.CONFIG["database"]["name"],
        #         host     = config.CONFIG["database"]["host"],
        #         port     = config.CONFIG["database"]["port"],
        #         user     = config.CONFIG["database"]["user"],
        #         password = config.CONFIG["database"]["password"]
        #     )
        async with HangoutCoreBot(
            commands.when_mentioned,
            intents = intents,
            activity = activity,
            web_client = our_client,
            #db_pool = db_pool,
            debug_mode = argv_debug,
            config = config,
            terminal = terminal
        ) as HangoutCore:
            await HangoutCore.start(botToken)

def init():
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        try:
            asyncio.run(Terminal().Log().CRITICAL(f"Please refrain from using CTRL+C to shutdown bot."))
            # Here we'd make sure database exited/saved gracefully as well as any other essential process that may suffer from stopping abruptly.
            asyncio.run(Terminal().EXIT(f"Shutting Down..."))
        except:
            pass
        pass
    except SystemExit:
        try:
            asyncio.run(Terminal().EXIT(f"Exiting..."))
        except:
            pass
        pass
    # except Exception as e:
    #     Terminal().Log().ERROR(e)
    #     Terminal().EXIT(f"Shutting Down...")
    # except:
    #     Terminal().Log().CRITICAL(f"Shutting Down...")
    #     sys.exit(0)

if __name__ == "__main__":
    init()