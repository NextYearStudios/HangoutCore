import aiomysql
import aiomysql.utils
import discord
import jproperties
import logging

from . import bot, utils

__version__ = "3.00.1"
__discord__ = "linoshangout"
__creator__ = "272230336656834560"

# colorBG = utils.terminal.colorBG
# colorFG = utils.terminal.colorFG

CONFIG_APP_NAME: str = 'hangoutcore.properties'
CONFIG_APP: jproperties.Properties

CONFIG_BOT_OUTDATED: bool = False
CONFIG_BOT_NAME: str = None
CONFIG_BOT: dict

DIRECTORY_COGS: str = ""
DIRECTORY_CONFIGS: str = ""
DIRECTORY_LOGS: str = ""

DEBUG: bool = False
INVALID_ARGS: bool = False
SILENT: bool = False
TOKEN: int = -1
FRESH_INSTALL: bool = False

SYSTEM_COGS: bool = True

INIT_TIME = None
DB_POOL: aiomysql.Pool | None = None
BOT: bot.HangoutCoreBot = None
SYSTEMGROUP: discord.app_commands.Group = None

terminal: utils.terminal = None
log: utils.terminal.Log = None


loggerDiscord = logging.getLogger("discord")
loggerHangoutCore = logging.getLogger("HangoutCore")
loggerRoot = logging.getLogger("root")

# class responses():
#     """Stored responses for terminal arguments.
#     ----------
#     Primarily used to reduce clutter in main script"""
#     help = """[b]
# [[red]-c-a, --config-app  : string  [white]] Load the specified app config. 
#                                  If the specified config cannot be found, returns to default.
# [[red]-c-b, --config-bot  : string  [white]] Load the specified bot config, Also sets as default. 
#                                  If the specified config cannot be found, return to previous config as a precaution.
# [[red]-d  , --debug       : bool    [white]] Enable debug mode for more information to be displayed in the terminal. 
#                                  Changes log mode to DEBUG.
# [[red]-n  , --new         : empty   [white]] Manually put HangoutCore in a setup state in order to create a new configuration. 
#                                  Sets the new config as default.
# [[red]-s-c, --system-cogs : bool    [white]] Enable/Disable to use provided system modules.

# [[red]-s  , --silent      : bool    [white]] Enable/Disable to have information sent to log only, or terminal and log().
#                                  Useful for running as a service since there's no access to terminal.
# [[red]-t  , --token       : integer [white]] Specify which token to use if you're using multiple. Allows user to skip token choice prompt.

# [/b]"""
#     w_message = "Please do not salt the snails"
