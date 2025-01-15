import argparse
import logging
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

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

parser: argparse.ArgumentParser = argparse.ArgumentParser(
    prog="HangoutCore",
    description="HangoutCore Script",
    epilog="Text",
    exit_on_error=True,
)
parser.add_argument("command", choices=["start", "init"])
parser.add_argument(
    "-ac",
    "--app-config",
    action="store",
    default="hangoutcore.properties",
    help="Specify application configuration to use",
)
parser.add_argument(
    "-bc", "--bot-config", action="store", help="Specify bot configuration to use"
)
parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode")
parser.add_argument(
    "-dc", "--default-cogs", action="store_true", help="Enable default cogs"
)
parser.add_argument("-n", "--new", action="store_true", help="Force new install")
parser.add_argument("-s", "--silent", action="store_true", help="Enable silent mode")
parser.add_argument(
    "-t",
    "--token",
    default=-1,
    action="store",
    type=int,
    help="Specify token index regarding config token list",
)

args = parser.parse_args()

db_pool = None

logger: dict[str, logging.Logger] = {
    "Discord": logging.getLogger("discord"),
    "HangoutCore": logging.getLogger("HangoutCore"),
    "Root": logging.getLogger("root"),
}
_logFormatter = logging.Formatter(
    """[%(name)s][%(levelname)s] %(message)s""", "%m/%d/%Y %I:%M:%S %p"
)
_fileHandler = logging.FileHandler(
    filename=rf"init.log", mode="w", encoding="utf-8", delay=False, errors=None
)
_fileHandler.setFormatter(_logFormatter)
logger["Root"].addHandler(_fileHandler)
logger["Root"].setLevel(logging.NOTSET)
# logger["HangoutCore"].addHandler(_fileHandler)
# logger["HangoutCore"].setLevel(logging.NOTSET)

system_group: discord.app_commands.Group = None

terminal: dict[str, utils.terminal] = {
    os.getpid(): utils.terminal("Hangoutcore", logger["HangoutCore"]),
}

terminal[os.getpid()].log = terminal[os.getpid()].Log(
    "HangoutCore", logger["HangoutCore"]
)


class Config:
    def __init__(self):
        self.app_config = self.App()
        self.bot_config = self.Bot()

    class App(jproperties.Properties):
        def __init__(self):
            self.name: str = "hangoutcore.properties"
            self.data: jproperties.Properties = None
            self.directory: dict = {
                "cogs": "",
                "configs": "",
                "logs": "",
            }

    class Bot(object):
        def __init__(self):
            self.outdated: bool = False
            self.name: str = None
            self.path: Path = None
            self.data: dict = {}


config = Config()
