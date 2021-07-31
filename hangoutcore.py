import config
import datetime
import discord
import logging
import os, sys
import utils
import ctypes
import ctypes.util


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

    activity = discord.Activity()

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
        
    def __init__(self, command_prefix, argv):
        super().__init__(command_prefix=command_prefix,
            activity = self.activity,
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
        self.start_time = '{0:%d%b%Y %Hh:%Mm}'.format(datetime.datetime.now())
        utils.terminal.initiate(self.start_time, self.debug_mode)
        utils.log("INFO", f"Looking for Bot Modules in the 'cogs' Directory.")
        cogs = utils.GetCogs()
        for file in cogs["valid_files"]:
            utils.log("INFO", f" └ Found {file}")
            try:
                cog = bot.load_extension(f'{config.COG_DIRECTORY_PATH}.{file[:-3]}')
            except Exception as e:
                utils.ErrorProcessing.CogLoadError(file, e, self.debug_mode)
            else:
                utils.log("INFO", f"  └ successfully loaded {file}.")
        for file in cogs["disabled_files"]:
            utils.log("INFO", f" └ Found Disabled file {file}, Skipping.")
        for file in cogs["invalid_files"]:
            if file == "__pycache__" or "__init__":
                pass
            else:
                utils.log("INFO", f" └ Found invalid file {file}, Skipping.")
        utils.terminal.refresh(self.start_time, self.debug_mode)
        utils.log("INFO", f"Successfully loaded {len(cogs['valid_files'])} extension(s).")
        utils.log("INFO", f"Logged in as {self.user} (ID: {self.user.id}).")
        if len(cogs["invalid_files"]) > 0:
            utils.log("WARNING", f"Found {len(cogs['invalid_files'])} invalid extension(s) in the 'cogs' directory. If you believe this is an error please verify each .py file and make sure it is set up as a cog properly, Otherwise you can ignore this message.")
        
        opuslib = ctypes.util.find_library('opus')
        if opuslib is not None:
            try:
                utils.log("INFO", f"Loading Opus.")
                discord.opus.load_opus('opus')
            except Exception as e:
                utils.log("ERROR", e)
            else:
                if not discord.opus.is_loaded():
                    utils.log("CRITICAL", "Opus Failed To Load.")
                else:
                    utils.log("INFO", "Successfully loaded opus.")
        else:
            utils.log("WARNING", "Could not find Opus, You will not be able to play audio without it.")
                
    
        

def get_prefix(bot, message):
        prefixes = cfg["bot"]["prefixes"]

        # Check to see if we are outside of a guild. e.g DM's etc.
        if not message.guild or prefixes is None:
            # Only allow ! to be used in DMs or if no prefix is specified.
            return '!'

        return commands.when_mentioned_or(*prefixes)(bot, message)

if __name__ == "__main__":
    bot = HangoutCoreBot(command_prefix=get_prefix, argv=sys.argv[1:])

    @commands.is_owner()
    @bot.command(name="load")
    async def loadCog(ctx: commands.Context, cog:str):
        await ctx.message.delete()
        if not cog.endswith('.py'):
            cog = cog + '.py'
        cog = str(cog).lower()
        if cog in os.listdir(config.COG_DIRECTORY_PATH):
            if f"{config.COG_DIRECTORY_PATH}.{cog[:-3]}" in bot.extensions:
                await ctx.send(f"Sorry. That cog has already been loaded.", delete_after=15)
            else:
                try:
                    bot.load_extension(f"{config.COG_DIRECTORY_PATH}.{cog[:-3]}")
                except Exception as e:
                    print(e)
                else:
                    embed = discord.Embed(
                            title=f"Successfully Loaded {cog}",
                            colour=discord.Colour.dark_theme(),
                            timestamp=datetime.datetime.now()
                    )
                    embed.set_footer(
                        text=f'Automatic Notification | Category: System',
                        icon_url=f'{bot.user.avatar.url}'
                    )
                    await ctx.send(embed=embed,delete_after=15)
    
    @commands.is_owner()
    @bot.command(name="unload")
    async def unloadCog(ctx: commands.Context, cog:str):
        await ctx.message.delete()
        if not cog.endswith('.py'):
            cog = cog + '.py'
        cog = str(cog).lower()
        cogs = utils.GetCogs()
        if cog in cogs["valid_files"]:
            if f"{config.COG_DIRECTORY_PATH}.{cog[:-3]}" not in bot.extensions:
                await ctx.send(f"Sorry. That cog has already been unloaded.", delete_after=15)
            else:
                try:
                    bot.unload_extension(f"{config.COG_DIRECTORY_PATH}.{cog[:-3]}")
                except Exception as e:
                    print(e)
                else:
                    embed = discord.Embed(
                            title=f"Successfully Unloaded {cog}",
                            colour=discord.Colour.dark_theme(),
                            timestamp=datetime.datetime.now()
                    )
                    embed.set_footer(
                        text=f'Automatic Notification | Category: System',
                        icon_url=f'{bot.user.avatar.url}'
                    )
                    await ctx.send(embed=embed,delete_after=15)
        else:
            await ctx.send(f"Sorry, that cog is not valid. Please check your spelling and try again.")

    @bot.command()
    async def extensions(ctx: commands.Context):
        await ctx.message.delete()
        print(bot.extensions)
        


if isinstance(cfg["bot"]["token"], str) and cfg["bot"]["token"] != "":
    bot.run(cfg["bot"]["token"])
elif isinstance(cfg["bot"]["token"], list) and cfg["bot"]["token"][0] != "":
    bot.run(cfg["bot"]["token"][0])
