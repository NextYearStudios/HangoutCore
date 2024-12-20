"""
	HangoutCore's Main Script.
	----------
	Last Updated: June 24, 2024
	Last Updated by: Lino
	License: Refer to LICENSE.md
	Notes:
		This file is still a work in progress.
	━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	This script handles the following:
	----------
	Starting/Stopping Discord Bot
	Starting/Stopping Database
	━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	WARNING: This is a Core Script
	----------
		› Please do not modify any of the following content unless you know what you're doing. Modifying the following code and not updating the rest of the bot 
			code to match can/will cause issues.
		› If you do decide to modify the following code please understand that HangoutCore's Dev team, Discord.py's Dev Team nor Python's Dev team are obligated
			to help you.
		› By Modifying the following code you acknowledge and agree to the text above.
	━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import aiomysql
import asyncio
import concurrent.futures
import discord
import hangoutcore
import hangoutcore.setup
import logging
import os
import requests
import sys

from aiohttp import ClientSession
from datetime import datetime, UTC
from discord import app_commands
from discord.ext import commands
from pathlib import Path
from rich.console import Group
from rich.logging import RichHandler
from rich.panel import Panel

from hangoutcore import utils
from hangoutcore.bot import HangoutCoreBot

_logFormatter = logging.Formatter("""[%(name)s][%(levelname)s] %(message)s""", "%m/%d/%Y %I:%M:%S %p")
_fileHandler = logging.FileHandler(
	filename = fr"init.log",
	mode = "w",
	encoding = "utf-8",
	delay = False,
	errors = None
)
_fileHandler.setFormatter(_logFormatter)

hangoutcore.loggerHangoutCore.addHandler(_fileHandler)
hangoutcore.loggerHangoutCore.setLevel(logging.NOTSET)

terminal = utils.terminal("Hangoutcore", hangoutcore.loggerHangoutCore)
log = terminal.Log("Hangoutcore", hangoutcore.loggerHangoutCore)

hangoutcore.terminal = terminal
hangoutcore.log = log

async def __main__():
	sys.path.append(os.getcwd()) # This expands package finding to our working directory 
	hangoutcore.INIT_TIME = '{0:%d%b%Y %Hh:%Mm}'.format(datetime.now(UTC))

	# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	# Section Description: Argument Parsing

	def process_args(argv:list[str]):
		def invalid_arg(r:int, arg: str = None):
			hangoutcore.INVALID_ARGS = True
			if r == 0:
				log.ERROR(f"'{arg}' is not a valid argument.")
			elif r == 1:
				log.ERROR(f"'{arg}' requires a numeric value.")
			elif r == 2:
				log.ERROR(f"'{arg}' requires a string value.")
			elif r == 3:
				log.ERROR(f"'{arg}' requires a bool value.")

		def get_arg(short_arg:str, long_arg:str) -> str|bool|int:
			if argv is None:
				return None
			else:
				_arg_position = None
				_return = {
					"exists": False,
					"value": None
				}

				def _getValue(argPos: int):
					try:
						_arg_value = argv[argPos].lower()
						if str(_arg_value).startswith('-'):
							_arg_value = None
							return None
						else:
							argv.pop(argPos)
					except IndexError:
						return None
					else:
						if _arg_value == "true":
							return True
						elif _arg_value == "false":
							return False
						elif _arg_value.isnumeric():
							return int(_arg_value)
						else:
							return _arg_value

				if short_arg in argv:
					_return["exists"] = True
					_arg_position = argv.index(short_arg)
					argv.pop(_arg_position)
					_return['value'] = _getValue(_arg_position)
				elif long_arg in argv:
					_return["exists"] = True
					_arg_position = argv.index(long_arg)
					argv.pop(_arg_position)
					_return['value'] = _getValue(_arg_position)
				
				return _return

		_arg_help = get_arg('-h', '--help')
		_arg_appconfig = get_arg('-a-c', '--app-config')
		_arg_botconfig = get_arg('-b-c', '--bot-config')
		_arg_debug = get_arg('-d', '--debug')
		_arg_new = get_arg('-n', '--new')
		_arg_silent = get_arg('-s', '--silent')
		_arg_systemcogs = get_arg('-s-c', '--system-cogs')
		_arg_token = get_arg('-t', '--token')

		_invalidArgs = []

		if _arg_help['exists']:
			def __spaces__(x:int) -> str:
				"""Returns a string of spaces * x"""
				return x*' '
			terminal.print_hr()
			terminal.print(Panel(Group(
				# " ", # Empty String for spacing
				"██╗░░██╗░█████╗░███╗░░██╗░██████╗░░█████╗░██╗░░░██╗████████╗░█████╗░░█████╗░██████╗░███████╗", # .center(shutil.get_terminal_size().columns),
				"██║░░██║██╔══██╗████╗░██║██╔════╝░██╔══██╗██║░░░██║╚══██╔══╝██╔══██╗██╔══██╗██╔══██╗██╔════╝", # .center(shutil.get_terminal_size().columns),
				"███████║███████║██╔██╗██║██║░░██╗░██║░░██║██║░░░██║░░░██║░░░██║░░╚═╝██║░░██║██████╔╝█████╗░░", # .center(shutil.get_terminal_size().columns),
				"██╔══██║██╔══██║██║╚████║██║░░╚██╗██║░░██║██║░░░██║░░░██║░░░██║░░██╗██║░░██║██╔══██╗██╔══╝░░", # .center(shutil.get_terminal_size().columns),
				"██║░░██║██║░░██║██║░╚███║╚██████╔╝╚█████╔╝╚██████╔╝░░░██║░░░╚█████╔╝╚█████╔╝██║░░██║███████╗", # .center(shutil.get_terminal_size().columns),
				"╚═╝░░╚═╝╚═╝░░╚═╝╚═╝░░╚══╝░╚═════╝░░╚════╝░░╚═════╝░░░░╚═╝░░░░╚════╝░░╚════╝░╚═╝░░╚═╝╚══════╝", # .center(shutil.get_terminal_size().columns),
				"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", # .center(shutil.get_terminal_size().columns),
				# " ",
			)), justify="center", alt = "Program Title")
			terminal.print_hr("Help")
			terminal.print(f"[b][[red]-c-a, --config-app  : string  [white]] Load the specified app config. If the specified config cannot be found, returns to default.[/b]")
			terminal.print_hr()
			terminal.print(f"[b][[red]-c-b, --config-bot  : string  [white]] Load the specified bot config, Also sets as default.\n{__spaces__(33)}If the specified config cannot be found, return to previous config as a precaution.[/b]")
			terminal.print_hr()
			terminal.print(f"[b][[red]-d  , --debug       : bool    [white]] Enable debug mode for more information to be displayed in the terminal. Changes log mode to DEBUG.[/b]")
			terminal.print_hr()
			terminal.print(f"[b][[red]-n  , --new         : empty   [white]] Manually put HangoutCore in a setup state in order to create a new configuration.\n{__spaces__(33)}Sets the new config as default.[/b]")
			terminal.print_hr()
			terminal.print(f"[b][[red]-s-c, --system-cogs : bool    [white]] Enable/Disable to use provided system modules.[/b]")
			terminal.print_hr()
			terminal.print(f"[b][[red]-s  , --silent      : bool    [white]] Enable/Disable to have information sent to log only, or terminal and log().\n{__spaces__(33)}Useful for running as a service since there's no access to terminal.[/b]")
			terminal.print_hr()
			terminal.print(f"[b][[red]-t  , --token       : integer [white]] Specify which token to use if you're using multiple. Allows user to skip token choice prompt.[/b]")
			terminal.print_hr()

		if _arg_appconfig['exists']:
			if _arg_appconfig['value'] is not None:
				hangoutcore.CONFIG_APP_NAME = _arg_appconfig['value']
			else:
				_invalidArgs.append({'arg': '--app-config', 'value': 2})

		if _arg_botconfig['exists']:
			if _arg_botconfig['value'] is not None:
				hangoutcore.CONFIG_BOT_NAME = _arg_botconfig['value']
			else:
				_invalidArgs.append({'arg': '--bot-config', 'value': 2})

		if _arg_debug['exists']:
			if _arg_debug['value'] is not None:
				hangoutcore.DEBUG = _arg_debug['value']
				if _arg_debug['value']:
					hangoutcore.loggerHangoutCore.setLevel(logging.DEBUG)
					hangoutcore.loggerDiscord.setLevel(logging.DEBUG)
				else:
					hangoutcore.loggerHangoutCore.setLevel(logging.INFO)
					hangoutcore.loggerDiscord.setLevel(logging.INFO)
			else:
				_invalidArgs.append({'arg': '--debug', 'value': 3})

		if _arg_new['exists']:
			if _arg_new['value'] is not None:
				hangoutcore.FRESH_INSTALL = _arg_new['value']
			else:
				_invalidArgs.append({'arg': '--new', 'value': 3})

		if _arg_silent['exists']:
			if _arg_silent['value'] is not None:
				hangoutcore.SILENT = _arg_silent['value']
				terminal.__setsilent__(_arg_silent['value'])
				log.__setsilent__(_arg_silent['value'])
			else:
				_invalidArgs.append({'arg': '--silent', 'value': 3})

		if _arg_systemcogs['exists']:
			if _arg_systemcogs['value'] is not None:
				hangoutcore.SYSTEM_COGS = _arg_systemcogs['value']
			else:
				_invalidArgs.append({'arg': '--system-cogs', 'value': 3})

		if _arg_token['exists']:
			if _arg_token['value'] is not None:
				hangoutcore.TOKEN = _arg_token['value']
			else:
				_invalidArgs.append({'arg': '--token', 'value': 1})

		if len(_invalidArgs) > 0 or len(argv) > 0:
			terminal.print_hr()
			terminal.print_center("WARNING")
			terminal.print_hr()
			for invalidArg in _invalidArgs:
				invalid_arg(invalidArg['value'], invalidArg['arg'])
			for arg in argv:
				invalid_arg(0, arg)

			log.INFO(f"Your provided args are listed below, Please double check your input and try again:\n hangoutcore {sys.argv[1:]}")

			if not terminal.confirm("[[red]CONFIRMATION REQUIRED[/red]] Would you like to continue startup?", default = False):
				sys.exit(1)
		
	if len(sys.argv[1:]) > 0:
		process_args(sys.argv[1:])

	# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	# Section Description: Setup title

	terminal.clear()
	terminal.print_hr()
	terminal.print(Panel(Group(
		# " ", # Empty String for spacing
		"██╗░░██╗░█████╗░███╗░░██╗░██████╗░░█████╗░██╗░░░██╗████████╗░█████╗░░█████╗░██████╗░███████╗", # .center(shutil.get_terminal_size().columns),
		"██║░░██║██╔══██╗████╗░██║██╔════╝░██╔══██╗██║░░░██║╚══██╔══╝██╔══██╗██╔══██╗██╔══██╗██╔════╝", # .center(shutil.get_terminal_size().columns),
		"███████║███████║██╔██╗██║██║░░██╗░██║░░██║██║░░░██║░░░██║░░░██║░░╚═╝██║░░██║██████╔╝█████╗░░", # .center(shutil.get_terminal_size().columns),
		"██╔══██║██╔══██║██║╚████║██║░░╚██╗██║░░██║██║░░░██║░░░██║░░░██║░░██╗██║░░██║██╔══██╗██╔══╝░░", # .center(shutil.get_terminal_size().columns),
		"██║░░██║██║░░██║██║░╚███║╚██████╔╝╚█████╔╝╚██████╔╝░░░██║░░░╚█████╔╝╚█████╔╝██║░░██║███████╗", # .center(shutil.get_terminal_size().columns),
		"╚═╝░░╚═╝╚═╝░░╚═╝╚═╝░░╚══╝░╚═════╝░░╚════╝░░╚═════╝░░░░╚═╝░░░░╚════╝░░╚════╝░╚═╝░░╚═╝╚══════╝", # .center(shutil.get_terminal_size().columns),
		"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", # .center(shutil.get_terminal_size().columns),
		# " ",
	)), justify="center", alt = "Program Title")
	terminal.print_hr()
	
	# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	# Section Description: Locate and process app config / presents option to init otherwise

	_appconfig = await utils.local.appConfig.get(hangoutcore.CONFIG_APP_NAME)
	if _appconfig is None:
		if terminal.confirm("[[red]CONFIRMATION REQUIRED[/red]] Would you like to begin initialization?", default = True):
			await hangoutcore.setup.__main__()
		else:
			sys.exit(1)
	else:
		hangoutcore.CONFIG_APP_NAME = _appconfig[0]
		hangoutcore.CONFIG_APP = _appconfig[1]
		hangoutcore.CONFIG_BOT_NAME = hangoutcore.CONFIG_APP["botConfig"].data
		hangoutcore.DIRECTORY_CONFIGS = hangoutcore.CONFIG_APP["botConfigDirectory"].data
		hangoutcore.DIRECTORY_COGS = hangoutcore.CONFIG_APP["botCogDirectory"].data
		hangoutcore.DIRECTORY_LOGS = hangoutcore.CONFIG_APP["botLogDirectory"].data
	
	# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	# Section Description: Locate and process bot config / presents option to init otherwise

	hangoutcore.CONFIG_BOT = await utils.local.botConfig.get(Path(hangoutcore.DIRECTORY_CONFIGS).joinpath(hangoutcore.CONFIG_BOT_NAME).absolute())
	if hangoutcore.CONFIG_BOT is None:
		if terminal.confirm("[[red]CONFIRMATION REQUIRED[/red]] Would you like to begin initialization?", default = True):
			await hangoutcore.setup.__main__()
		else:
			sys.exit(1)
	else:
		if hangoutcore.CONFIG_BOT['_info']['version'] < utils.local.botConfig.CONFIG_VERSION:
			hangoutcore.CONFIG_BOT_OUTDATED = True
			log.WARNING(f"Bot config located at ({Path(hangoutcore.DIRECTORY_CONFIGS).joinpath(hangoutcore.CONFIG_BOT_NAME).absolute()}) is outdated.")

	# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	# Section Description: Update logger

	hangoutcore.loggerHangoutCore.debug(fr"Initial setup complete, updating log location. New log location: {hangoutcore.DIRECTORY_LOGS}/log_{hangoutcore.INIT_TIME.replace(' ', '_').replace(':', '')}.log")
	hangoutcore.loggerHangoutCore.removeHandler(hangoutcore.loggerHangoutCore.handlers[0])
	_fileHandler = logging.FileHandler(
		filename = fr"{hangoutcore.DIRECTORY_LOGS}/log_{hangoutcore.INIT_TIME.replace(' ', '_').replace(':', '')}.log",
		mode = "a",
		encoding = "utf-8",
		delay = False,
		errors = None
	)
	_fileHandler.setFormatter(_logFormatter)
	hangoutcore.loggerHangoutCore.addHandler(_fileHandler)
	hangoutcore.loggerDiscord.addHandler(_fileHandler)

	_cliFormatter = logging.Formatter("""[%(name)s][%(levelname)s] %(message)s""", "%m/%d/%Y %I:%M:%S %p")
	_cliHandler = logging.StreamHandler()
	_cliHandler.setFormatter(_cliFormatter)
	# hangoutcore.loggerDiscord.addHandler(_cliHandler)RichHandler()
	# hangoutcore.loggerDiscord.addHandler(RichHandler())

	_logFiles = os.listdir(hangoutcore.DIRECTORY_LOGS)
	
	# Sort log files by date and trim to max of 5
	while len(_logFiles) > 5:
		_logFiles = os.listdir(hangoutcore.DIRECTORY_LOGS)
		oldest_file = sorted([ f"{hangoutcore.DIRECTORY_LOGS}/{f}" for f in os.listdir(hangoutcore.DIRECTORY_LOGS)], key=os.path.getctime)[0]

		if len(_logFiles) > 5:
			os.remove(oldest_file)
		else:
			break

	# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	# Section Description: Setup Bot description

	async def is_latest(package_name: str):
		_package = sys.modules[package_name]
		response = requests.get(f'https://pypi.org/pypi/{package_name}/json')
		latest_version = response.json()['info']['version']
		if _package.__version__ is not None:
			# terminal.log.DEBUG(f'{package_name}: {latest_version} | {_package.__version__}')
			if latest_version > _package.__version__ or latest_version < _package.__version__: # Throws False if local is newer than online to remind user that local is not matching public version
				return False
			else:
				return True
		elif _package.version is not None:
			# terminal.log.DEBUG(f'{package_name}: {latest_version} | {_package.version}')
			if latest_version > _package.version or latest_version < _package.version:
				return False
			else:
				return True

	if await is_latest("discord"):
		_discord_version = f"Discord.py Version: [b][green]{discord.__version__}[/b]"
	else:
		_discord_version = f"Discord.py Version: [b]{discord.__version__}[/b] [red reverse](Outdated)"

	if await is_latest("hangoutcore"):
		_hangoutcore_version = f"HangoutCore Version: [b][green]{hangoutcore.__version__}[/b]"
	else:
		_hangoutcore_version = f"HangoutCore Version: [b]{hangoutcore.__version__}[/b] [red reverse](Version Mismatch)"

	if hangoutcore.CONFIG_BOT_OUTDATED:
		_configOutdated = f"Bot Config Version: [b]{hangoutcore.CONFIG_BOT['_info']['version']}[/b] [red reverse](Outdated)"
	else:
		_configOutdated = f"Bot Config Version:  [b][green]{hangoutcore.CONFIG_BOT['_info']['version']}[/b]"
	
	if hangoutcore.DEBUG:
		terminal.print(
			Panel(
				title = "[red]DEBUG MODE ENABLED", # Why I need 4 /'s is beyond me. I'll keep messing with this later but for now it works.
				subtitle =  '{0:%d%b%Y %Hh:%Mm}'.format(datetime.now()),
				renderable = Group(
					f"Bot Name: [b][green]{hangoutcore.CONFIG_BOT['bot']['name']}[/b]",
					f"Bot Version: [b][green]{hangoutcore.CONFIG_BOT['bot']['version']}[/b]",
					_configOutdated,
					f"SYS Version [b][green]{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}[/b]",
					f"API Version [b][green]{sys.api_version}[/b]",
					f"{_discord_version}",
					f"{_hangoutcore_version}",
					"",
					f"CPU Thread Count: [b][green]{os.cpu_count()}",
					f"Parent Process ID: [b][green]{os.getppid()}[/b]",
					f"Process ID: [b][green]{os.getpid()}[/b]"
				),
				style = f"red"),
				justify="center")
	else:
		terminal.print(
			Panel(
				subtitle= '{0:%d%b%Y %Hh:%Mm}'.format(datetime.now()),
				renderable = Group(
					f"Bot Name: [b]{hangoutcore.CONFIG_BOT['bot']['name']}[/b]",
					f"Bot Version: [green]{hangoutcore.CONFIG_BOT['bot']['version']}",
					f"{_discord_version}",
					f"{_hangoutcore_version}"
				)
			), 
			style=f"on {terminal.colorBG}", 
			justify="center")

	# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	# Section Description: Prints debug stuff, not super important

	terminal.print_hr("Pre-Load Output")
	log.DEBUG(f"Fresh Install: {hangoutcore.FRESH_INSTALL}")
	log.DEBUG(f"Silent: {hangoutcore.SILENT}")
	log.DEBUG(f"Debug: {hangoutcore.DEBUG}")
	log.DEBUG(f"Token: {hangoutcore.TOKEN}")
	log.DEBUG(f"App Config Name: {hangoutcore.CONFIG_APP_NAME}")
	log.DEBUG(f"App Config: {type(hangoutcore.CONFIG_APP)}")
	if hangoutcore.CONFIG_BOT_OUTDATED:
		log.DEBUG(f"Warning: Bot Config Is Outdated")
	log.DEBUG(f"Bot Config Name: {hangoutcore.CONFIG_BOT_NAME}")
	log.DEBUG(f"Bot Config: {type(hangoutcore.CONFIG_BOT)}")
	log.DEBUG(f"Bot Config Directory: {hangoutcore.DIRECTORY_CONFIGS}")
	log.DEBUG(f"Bot Cog Directory: {hangoutcore.DIRECTORY_COGS}")
	log.DEBUG(f"Bot Log Directory: {hangoutcore.DIRECTORY_LOGS}")
	log.DEBUG(f"Bot Using System Cogs: {hangoutcore.SYSTEM_COGS}")
	
	# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	# Section Description: Process token selection

	_configTokens = hangoutcore.CONFIG_BOT['bot']['token']
	_botToken = None

	if type(_configTokens) == str:
		log.DEBUG("Config Token is string.")
		_botToken = _configTokens
	elif type(_configTokens) == list:
		log.DEBUG("Config Tokens is list.")
		if hangoutcore.SILENT:
			try:
				log.DEBUG("Using first token since no token was specified in silent mode.")
				_botToken = _configTokens[0]
			except Exception as err:
				log.ERROR(err)
		elif hangoutcore.TOKEN != -1:
			try:
				log.DEBUG("Using specified token.")
				_botToken = _configTokens[hangoutcore.TOKEN]
			except Exception as err:
				log.ERROR(err)
		else:
			_filteredTokens = []
			for i, token in enumerate(_configTokens):
				_censoredToken = terminal.obfuscate(token,0,6,'*')
				_tokenStatus = False
				_tokenRequest: requests.Response = requests.get('https://discord.com/api/v10/users/@me',
				headers={'Authorization': f'Bot {token}'}).json()
				
				if _tokenRequest.get('message') == '401: Unauthorized':
					log.DEBUG(f"Failed to verify token {i}: '{_censoredToken}'")
				else:
					log.DEBUG(f"Verified token {i}: '{_censoredToken}'\n{_tokenRequest}")
					_tokenStatus = True
				
				_filteredTokens.append({
					"CensoredToken": terminal.obfuscate(token,0,6,'*'),
					"RawToken": token,
					"TokenValid": _tokenStatus,
					"TokenRequest": _tokenRequest})

			terminal.print_hr()
			terminal.print_center("Please choose an option from below.")
			terminal.print_hr()
			_choices = []
			for i, token in enumerate(_filteredTokens):
				_choices.append(f'{i+1}')
				terminal.print(f"Token [{i+1}]:")
				terminal.print(f"Bot Name: {token['TokenRequest'].get('username')}")
				if token['TokenValid']:
					terminal.print(f"[green][b]Valid[/b]: {token['CensoredToken']}")
				else:
					terminal.print(f"[red][b]Invalid[/b]{token['CensoredToken']}")
						
			terminal.print_hr()
			terminal.print_center(f"Cancel")
			_choices.append('cancel')
			while True:
				_tokenInput = terminal.input("",choices = _choices)
				
				if _tokenInput.lower() == "cancel":
					sys.exit(0)
				else:
					if terminal.confirm(f"You chose '{_filteredTokens[int(_tokenInput)-1]['TokenRequest'].get('username')}', Are you sure?", default = True):
						_botToken = _filteredTokens[int(_tokenInput)-1]
						break
					else:
						continue

	# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	# Section Description: TODO UPDATE DESCRIPTION
		
	def getBotActivity() -> discord.Activity:
		if hangoutcore.CONFIG_BOT is None:
			return None

		_rawActivity = hangoutcore.CONFIG_BOT['bot']['status']['type']
		_activity = None
		_activities = {
			"unknown": discord.ActivityType.unknown,
			"playing": discord.ActivityType.playing,
			"streaming": discord.ActivityType.streaming,
			"listening": discord.ActivityType.listening,
			"watching": discord.ActivityType.watching,
			"custom": discord.ActivityType.custom,
			"competing": discord.ActivityType.competing,
		}

		if _rawActivity in _activities.keys():
			_activity = discord.Activity(
				type = _activities[_rawActivity],
				name = hangoutcore.CONFIG_BOT['bot']['status']['name'],
				game = hangoutcore.CONFIG_BOT['bot']['status']['game'],
				url = hangoutcore.CONFIG_BOT['bot']['status']['url'],
				# timestamps = datetime.now(UTC)
				)
			return _activity
	
	def getBotIntents() -> discord.Intents:
		_rawIntents: dict = hangoutcore.CONFIG_BOT['bot']['intents']
		_intents = discord.Intents.none()
		_invalidFlags = []
		_missingFlags = []
		
		for flag in hangoutcore.CONFIG_BOT['bot']['intents']:
			if flag not in _intents.VALID_FLAGS:
				_invalidFlags.append(flag)

		for flag in _intents.VALID_FLAGS:
			if flag in _rawIntents.keys():
				if _rawIntents[flag]:
					setattr(_intents, flag, _rawIntents[flag])
			else:
				_missingFlags.append(flag)

		if len(_missingFlags) > 0:
			log.WARNING(f"The following intentions are missing from your bot config.")
			for flag in _missingFlags:
				terminal.print(f"Intention: '{flag}'")

		if len(_invalidFlags) > 0:
			log.WARNING(f"The following intentions retrieved from your bot config are invalid.")
			for flag in _invalidFlags:
				terminal.print(f"Intention: '{flag}'")
		
		return _intents

	log.DEBUG("Fetching bot activity from config.")
	_botActivity = getBotActivity()
	log.DEBUG(f"Fetched: {_botActivity}")
	log.DEBUG("Fetching bot intents from config.")
	_botIntents = getBotIntents()
	log.DEBUG(f"Fetched: {_botIntents}")

	async with ClientSession() as our_client:
		_dbType = str(hangoutcore.CONFIG_BOT['database']['type'])
		_devGuildID = int(hangoutcore.CONFIG_BOT['bot']['developer_guild_id'])

		if _dbType.lower() == "mysql":
			try:
				log.INFO(f"{_dbType}: Attempting to connect to database.")
				log.DEBUG(f"Database Name: {hangoutcore.CONFIG_BOT['database']['name']}")
				log.DEBUG(f"Database Host: {hangoutcore.CONFIG_BOT['database']['host']}")
				log.DEBUG(f"Database Port: {hangoutcore.CONFIG_BOT['database']['port']}")
				log.DEBUG(f"Database User: {hangoutcore.CONFIG_BOT['database']['user']}")
				log.DEBUG(f"Database Password: {terminal.obfuscate(hangoutcore.CONFIG_BOT['database']['password'], 0, 0, '*')}")
				
				_tempPool = await aiomysql.create_pool(
						db       = hangoutcore.CONFIG_BOT["database"]["name"],
						host     = hangoutcore.CONFIG_BOT["database"]["host"],
						port     = hangoutcore.CONFIG_BOT["database"]["port"],
						user     = hangoutcore.CONFIG_BOT["database"]["user"],
						password = hangoutcore.CONFIG_BOT["database"]["password"]
					)
			except aiomysql.MySQLError as err:
				log.ERROR(f"{_dbType}: {err.args[1]} | Error No. {err.args[0]}")
			else:
				log.INFO(f"Successfully connected to database: {hangoutcore.CONFIG_BOT['database']['host']}:{hangoutcore.CONFIG_BOT['database']['port']} with user: {hangoutcore.CONFIG_BOT['database']['user']}")
				hangoutcore.DB_POOL = _tempPool
		else:
			log.ERROR(f"{_dbType}: Database Config Invalid. Please check your bot config.")
			log.ERROR(f"{_dbType}: Skipping...")
			log.DEBUG(f"Starting bot with token: {_botToken['CensoredToken']}")

		async with HangoutCoreBot(
			commands.when_mentioned,
			intents = _botIntents,
			activity = _botActivity,
			web_client = our_client,
			db_pool = hangoutcore.DB_POOL,
			init_time = hangoutcore.INIT_TIME,
			DeveloperGuild_ID = _devGuildID,
			owner_id = 272230336656834560
		) as HangoutCore:
			hangoutcore.BOT = HangoutCore

			# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
			# Section Description: Add some 'core' commands, These are intended to be used by bot staff and should be available at all times.

			log.DEBUG("Creating 'System' group")
			class SystemGroup(app_commands.Group):
				
				def __init__(self, name = "system", description = "System Commands"):
					super().__init__(name=name, description=description)

				async def interaction_check(self, interaction: discord.Interaction) -> bool:
					
					if await HangoutCore.is_user_bot_staff(interaction):
						return True
					else:
						await interaction.response.send_message('You do not have the required role to use these commands.', ephemeral=True)
						return False

			hangoutcore.SYSTEMGROUP = SystemGroup()

			_systemGroup = hangoutcore.SYSTEMGROUP
			_commandGroup = SystemGroup(name = "commands")
			_moduleGroup = SystemGroup(name = "module")
				
			log.DEBUG("Adding 'Clear Commands' command to 'Command' group.")
			@_commandGroup.command(name = "clear", description = "Clear all commands and sync the bot.")
			async def clear_commands(interaction: discord.Interaction) -> None:
				await interaction.response.defer(ephemeral = True, thinking = True)

				async def _clear():
					_devGuild = discord.Object(id = HangoutCore.DeveloperGuild_ID, type = discord.Guild)
					HangoutCore.tree.clear_commands(guild = _devGuild)
					HangoutCore.tree.clear_commands(guild = None)
					# HangoutCore.tree.add_command(_systemGroup)

				if HangoutCore.BotSynced:
					_confirmView = utils.ui.Confirm(confirmation = "Cleared.")
					await interaction.followup.send(f"Already synced. Would you like to clear anyways?", view = _confirmView, ephemeral = True)
					await _confirmView.wait()
					if _confirmView.value is None:
						log.DEBUG("Confirmation timed out.")
					elif _confirmView.value:
						try:
							await _clear()
						except Exception as err:
							log.ERROR(err)
						else:
							log.DEBUG("Confirmed")
					else:
						pass
				else:
					try:
						await _clear()
					except Exception as err:
						log.ERROR(err)
					else:
						log.DEBUG("Confirmed")
						await interaction.followup.send(f"Bot commands have been cleared, Please sync.", ephemeral = True)

			log.DEBUG("Adding 'Sync Commands' command to 'Command' group.")
			@_commandGroup.command(name = "sync", description = "Sync the bot commands, optionally globally.")
			async def sync_commands(interaction: discord.Interaction, globally: bool = False) -> None:
				await interaction.response.defer(ephemeral = True, thinking = True)

				async def _sync():
					if globally:
							await HangoutCore.tree.sync()
							HangoutCore.BotSynced = True
							await interaction.followup.send(f"Bot has been synced globally.", ephemeral = True)
					else:
						_devGuild = discord.Object(id = HangoutCore.DeveloperGuild_ID, type = discord.Guild)
						if _devGuild is None:
							await interaction.followup.send(f"Failed to sync, Dev guild is None.")
						HangoutCore.tree.copy_global_to(guild = _devGuild)
						await HangoutCore.tree.sync(guild = _devGuild)
						HangoutCore.BotSynced = True

				if HangoutCore.BotSynced:
					_confirmView = utils.ui.Confirm(confirmation = "Synced.")
					await interaction.followup.send(f"Already synced. Would you like to sync anyways?", view = _confirmView, ephemeral = True)
					await _confirmView.wait()
					if _confirmView.value is None:
						log.DEBUG("Confirmation timed out.")
						# await interaction.followup.send(f"Bot has been synced to developer guild.", ephemeral = True)
					elif _confirmView.value:
						await _sync()
					else:
						pass
				else:
					try:
						await _sync()
						await interaction.followup.send(f"Bot has been synced to developer guild.", ephemeral = True)
					except Exception as err:
						log.DEBUG(err)
	
			log.DEBUG("Adding 'Command' group to 'System' group.")
			_systemGroup.add_command(_commandGroup)

			async def module_autocomplete(interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
				_options = []
				_cogDirectory = hangoutcore.DIRECTORY_COGS
				_cogs = None
				
				try:
					_cogs = os.listdir(_cogDirectory)
				except Exception as err:
					HangoutCore.log.ERROR(err)
					raise err

				for cog in _cogs:
					if cog.endswith(".py"):
						_options.append(cog)

				return [
					app_commands.Choice(name=option, value=option)
					for option in _options if current.lower() in option.lower()
				]

			log.DEBUG("Adding 'List Module' command to 'Module' group.")
			@_moduleGroup.command(name = "list", description = "List all available modules.")
			async def list_module(interaction: discord.Interaction) -> None:
				await interaction.response.defer(ephemeral = True, thinking = True)
				_cogDirectory = hangoutcore.DIRECTORY_COGS
				_cogs = None
				
				_embed = discord.Embed(
					title = "Modules",
					description = "A list of all the Modules.",
					timestamp = datetime.now(UTC)
				)

				_embed.set_footer(text = "System Response")
				try:
					_cogs = os.listdir(_cogDirectory)
					for cog in _cogs:
						if cog.endswith(".py"):
							_embed.description += f"\n- {cog}"

				except Exception as err:
					HangoutCore.log.ERROR(err)
					raise err

				await interaction.followup.send(embed = _embed, ephemeral = True)

			log.DEBUG("Adding 'Load Module' command to 'Module' group.")
			@_moduleGroup.command(name = "load", description = "Load a specified module.")
			@app_commands.autocomplete(module=module_autocomplete)
			async def load_module(interaction: discord.Interaction, module: str) -> None:
				await interaction.response.defer(ephemeral = True, thinking = True)
				module = module.lower()

				try:
					await HangoutCore.load_extensions(module)
				except HangoutCore.terminal.ExtensionAlreadyLoadedError as err:
					log.ERROR(f"{err}")
					await interaction.followup.send("...", embed = HangoutCore.errorEmbed(102, extension = module, err = err), ephemeral = True)
				except FileNotFoundError as err:
					log.ERROR(f"{err}")
					await interaction.followup.send("...", embed = HangoutCore.errorEmbed(102, extension = module, err = err), ephemeral = True)
				except Exception as err:
					log.ERROR(f"{err}")
					await interaction.followup.send("...", embed = HangoutCore.errorEmbed(101, extension = module, err = err), ephemeral = True)
				else:
					await interaction.followup.send(f"Module '{module}' has been loaded.", ephemeral = True)

			log.DEBUG("Adding 'Reload Module' command to 'Module' group.")
			@_moduleGroup.command(name = "reload", description = "Reload a specified module.")
			@app_commands.autocomplete(module=module_autocomplete)
			async def reload_module(interaction: discord.Interaction, module: str) -> None:
				await interaction.response.defer(ephemeral = True, thinking = True)
				if not module.startswith('cogs.'):
					module = f"cogs.{module}"
				if module in HangoutCore.extensions.keys():
					try:
						await HangoutCore.reload_extension(name = module)
					except Exception as err:
						log.ERROR(f"{err}")
						await interaction.followup.send(f"Could not reload module '{module}' due to an error.", ephemeral = True)
					else:
						await interaction.followup.send(f"Module '{module[5:].capitalize()}' has been reloaded.", ephemeral = True)
				else:
					log.DEBUG(f"{HangoutCore.extensions}")
					await interaction.followup.send(f"The module name you provided could not be found. Please check your input and try again.", ephemeral = True)

			log.DEBUG("Adding 'Unload Module' command to 'Module' group.")
			@_moduleGroup.command(name = "unload", description = "Unload a specified module.")
			@app_commands.autocomplete(module=module_autocomplete)
			async def unload_module(interaction: discord.Interaction, module: str) -> None:
				await interaction.response.defer(ephemeral = True, thinking = True)
				if not module.startswith('cogs.'):
					module = f"cogs.{module}"
				if module in HangoutCore.extensions.keys():
					try:
						await HangoutCore.unload_extension(name = module)
					except Exception as err:
						log.ERROR(f"{err}")
						await interaction.followup.send(f"Could not unload module '{module}' due to an error.", ephemeral = True)
					else:
						await interaction.followup.send(f"Module '{module[5:].capitalize()}' has been unloaded.", ephemeral = True)
				else:
					log.DEBUG(f"{HangoutCore.extensions}")
					await interaction.followup.send(f"The module name you provided could not be found. Please check your input and try again.", ephemeral = True)

			log.DEBUG("Adding 'Module' group to 'System' group.")
			_systemGroup.add_command(_moduleGroup)

			log.DEBUG("Adding 'System' group")
			HangoutCore.tree.add_command(_systemGroup)

			await HangoutCore.start(_botToken['RawToken'])

def __init__():

	try:
		asyncio.run(__main__())
	except Exception as err:
		log.ERROR(f"[b]{err}[/b]")
		raise err

if __name__ == "__main__":
	__init__()