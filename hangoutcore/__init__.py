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

__creator__ = discord.Object(id=272230336656834560)

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
