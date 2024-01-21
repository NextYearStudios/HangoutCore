import aiomysql
import jproperties
import logging

from . import app, bot, utils

__version__ = "3.00.1"
__discord__ = "linoshangout"
__creator__ = "272230336656834560"

colorBG = utils.terminal.colorBG
colorFG = utils.terminal.colorFG

CONFIG_APP_NAME = ""
CONFIG_APP: jproperties.Properties

CONFIG_BOT_OUTDATED: bool = False
CONFIG_BOT_NAME: str = ""
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
DB_POOL: aiomysql.Pool = None # type: ignore
BOT: bot.HangoutCoreBot = None


loggerDiscord = logging.getLogger("discord")
loggerHangoutCore = logging.getLogger("HangoutCore")
loggerRoot = logging.getLogger("root")

class responses():
    """Stored responses for terminal arguments.
    ----------
    Primarily used to reduce clutter in main script"""
    help = """
[-c-a, --config-app : string  ] Load the specified app config. 
                          If the specified config cannot be found, returns to default.
[-c-b, --config-bot : string  ] Load the specified bot config, Also sets as default. 
                          If the specified config cannot be found, return to previous config as a precaution.
[-d, --debug  : bool    ] Enable debug mode for more information to be displayed in the terminal. 
                          Changes log mode to DEBUG.
[-n, --new    : empty   ] Manually put HangoutCore in a setup state in order to create a new configuration. 
                          Sets the new config as default.
[-s, --silent : bool    ] Enable/Disable to have information sent to log only, or terminal and log().
                          Useful for running as a service since there's no access to terminal.
[-t, --token  : integer ] Specify which token to use if you're using multiple. Allows user to skip token choice prompt.
"""
    w_message = "Please do not salt the snails"
