import logging
import os
import sys
from datetime import datetime, timezone

import aiomysql
import aiomysql.utils
import discord
import jproperties

from . import utils

try:
    from ._version import version as __version__
except ImportError:
    __version__ = "0.0.0"

__creator__ = 272230336656834560

init_time: datetime = datetime.now(timezone.utc)
bot = None
db_pool = None
debug: bool = False
directory: dict[str, str] = {"cogs": "", "configs": "", "logs": ""}
invalid_args: bool = False
logger: dict[str, logging.Logger] = {
    "Discord": logging.getLogger("discord"),
    "HangoutCore": logging.getLogger("HangoutCore"),
    "Root": logging.getLogger("root"),
}
silent: bool = False
system_cogs: bool = False
system_group: discord.app_commands.Group = None
terminal: dict[str, utils.terminal] = {
    os.getpid(): utils.terminal("Hangoutcore", logger["HangoutCore"]),
}
terminal[os.getpid()].log = terminal[os.getpid()].Log(
    "HangoutCore", logger["HangoutCore"]
)
token: int = -1
fresh_install: bool = False


class Config:
    def __init__(self):
        self.app_config = self.App()
        self.bot_config = self.Bot()

    class App(jproperties.Properties):
        def __init__(self):
            self.name: str = "hangoutcore.properties"

    class Bot:
        def __init__(self):
            self.outdated: bool = False
            self.name: str = None
            self.config: dict = {}


config = Config()

# CONFIG_APP_NAME: str = 'hangoutcore.properties'
# CONFIG_APP: jproperties.Properties
# CONFIG_BOT_OUTDATED: bool = False
# CONFIG_BOT_NAME: str = None
# CONFIG_BOT: dict
# DIRECTORY_COGS: str = ""
# DIRECTORY_CONFIGS: str = ""
# DIRECTORY_LOGS: str = ""
# DEBUG: bool = False
# INVALID_ARGS: bool = False
# SILENT: bool = False
# TOKEN: int = -1
# FRESH_INSTALL: bool = False
# SYSTEM_COGS: bool = True
# INIT_TIME = None
# DB_POOL: aiomysql.Pool | None = None
# BOT = None
# SYSTEMGROUP: discord.app_commands.Group = None
# terminal: utils.terminal = None
# log: utils.terminal.Log = None
# loggerDiscord = logging.getLogger("discord")
# loggerHangoutCore = logging.getLogger("HangoutCore")
# loggerRoot = logging.getLogger("root")
