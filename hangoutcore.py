import config
import datetime
import discord
import logging
import os, sys
import utils

from discord.ext import commands

cfg = config.load_config()

class HangoutCoreBot(commands.Bot):
    date = '{0:%d%b%Y_%Hh-%Mm}'.format(datetime.datetime.now())
    logging.basicConfig(
        filename=f'{config.LOG_DIRECTORY_PATH}/log_{date}.log',
        encoding='utf-8',
        level=logging.NOTSET,
        format='[%(asctime)s][%(levelname)s] %(message)s',
        datefmt='%m/%d/%Y %I:%M:%S %p'
        )

    intents = discord.Intents.default()
    intents.members = True  
    intents.typing = True
    intents.presences = True
    intents.guilds = True

    def __init__(self, command_prefix, argv):
        super().__init__(command_prefix=command_prefix,
            activity = discord.Activity(type=discord.ActivityType.listening, name="!help"),
            description=cfg["bot"]["description"],
            intents=self.intents)

        self.start_time = "" # Add the start_time variable so that we may access it for debuging or information display purposes.
        self.debug_mode = False

        if len(argv) > 0:
            if argv[0] == "-h":
                print("\nhangoutcore.py -debug <True/False>\n")
                sys.exit(2)
            elif argv[0] == "-d" or argv == "-debug":
                if argv[1] == "True":
                    self.debug_mode = True
                else:
                    self.debug_mode = False
        else:
            self.debug_mode = False

    async def on_ready(self):
        self.start_time = datetime.datetime.now()
        utils.terminal.initiate(self.start_time, self.debug_mode)
        utils.log("INFO", f"Looking for Bot Modules in the 'cogs' Directory.")
        valid_files = []
        disabled_files = []
        invalid_files = []
        for file in os.listdir(config.COG_DIRECTORY_PATH):
            if file.endswith('.py'):
                utils.log("INFO", f" └ Found {file}")
                try:
                    cog = bot.load_extension(f'{config.COG_DIRECTORY_PATH}.{file[:-3]}')
                except Exception as e:
                    utils.log("ERROR", f"  └ Failed to load {file}.\n  Exception: {e}")
                else:
                    utils.log("INFO", f"  └ successfully loaded {file}.")
                    valid_files.append(file)
            elif file.endswith('.disabled'):
                utils.log("INFO", f" └ Found Disabled file {file}, Skipping.")
                disabled_files.append(file)
            else:
                if file == "__pycache__" or "__init__":
                    pass
                else:
                    invalid_files.append(file)
                    utils.log("INFO", f" └ Found invalid file {file}, Skipping.")
        utils.terminal.refresh(self.start_time, self.debug_mode)
        utils.log("INFO", f"Logged in as {self.user} (ID: {self.user.id})")
        utils.log("INFO", f"Successfully loaded {len(valid_files)} extension(s).")
        if len(invalid_files) > 0:
            utils.log("WARNING", f"Found {len(invalid_files)} invalid extension(s) in the 'cogs' directory. If you believe this is an error please verify each .py file and make sure it is set up as a cog properly, Otherwise you can ignore this message.")

        
            
        

def get_prefix(bot, message):
        prefixes = cfg["bot"]["prefixes"]

        # Check to see if we are outside of a guild. e.g DM's etc.
        if not message.guild or prefixes is None:
            # Only allow ! to be used in DMs
            return '!'

        return commands.when_mentioned_or(*prefixes)(bot, message)

if __name__ == "__main__":
    bot = HangoutCoreBot(command_prefix=get_prefix, argv=sys.argv[1:])

if isinstance(cfg["bot"]["token"], str) and cfg["bot"]["token"] != "":
    bot.run(cfg["bot"]["token"])
elif isinstance(cfg["bot"]["token"], list) and cfg["bot"]["token"][0] != "":
    bot.run(cfg["bot"]["token"][0])
