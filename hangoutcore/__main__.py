import asyncio
import json
import os
import requests
import shutil
import sys

import discord

from datetime import datetime, timezone
from jproperties import Properties
from pathlib import Path
from rich.console import Group
from rich.logging import RichHandler
from rich.panel import Panel

import hangoutcore

# import hangoutcore.bot
# import hangoutcore.setup
import hangoutcore.utils as utils

async def main():
	terminal = hangoutcore.terminal[os.getpid()]

	async def app_setup():
		if terminal.confirm("[[red]CONFIRMATION REQUIRED[/red]] Would you like to begin initialization?", default = True):
			terminal.log.DEBUG(f"Beginning setup...")

			def requestBotToken() -> list[str]: # returns [token, bot_name]
				while True:
					_botToken = terminal.input(f"Please Enter The Bot Token (Input will be blank for your protection)", password = True)
					# get the bot from discord api, so we can verify with the user if it is what they want to use
					terminal.log.INFO(f"Retreiving token status from Discord...")
					_botRequest = requests.get('https://discord.com/api/v10/users/@me',
												headers={'Authorization': f'Bot {_botToken}'}).json()
					if _botRequest.get('message') == '401: Unauthorized':
						terminal.log.ERROR("Token Verification Failed: Token does not exist")
						continue
					else:
						terminal.log.INFO(f"Token Verification Passed.")
						terminal.print(Panel(
									title = r"// Bot Settings \\",
									subtitle =  '{0:%d%b%Y %Hh:%Mm}'.format(hangoutcore.init_time),
									renderable = Group(
										"",
										f"Bot ID: [b]{_botRequest.get('id')}[/b]",
										f"Bot Name: [b]{_botRequest.get('username')}[/b]",
										""
									),
									# style = f"red on {terminal.colorBG}",
								),
								style=f"on {terminal.colorBG}",
								# justify="center"
							)
						if terminal.confirm(f"Are you sure you'd like to use the bot listed above?"):
							break
						else:
							continue
				return [_botToken, _botRequest.get('username')]

			def requestBotName(default: str):
				_botName = terminal.input(f"Please Enter The Bot Name (Default: {default}): ")
				if _botName == "" or _botName == None:
					return default
				else:
					return _botName

			def requestBotDescription():
				_botDescription = terminal.input(f"Please Enter The Bot Description: (This can always be changed in the config later.)")
				return _botDescription

			def requestBotPrefix():
				_default = "!"
				_botPrefix = terminal.input(f"(Legacy) Please Enter The Bot Prefix (Default: {_default}): ")
				if _botPrefix == "":
					return _default
				else:
					return _botPrefix

			def requestBotVersion():
				_default = "0.0.0"
				_botVersion = terminal.input(f"Please Enter The Bot Version (Default: {_default}): ")
				if _botVersion == "":
					return _default
				else:
					return _botVersion

			def requestBotConfigName():
				_default = "config.json"
				_ConfigName = terminal.input(f"Please enter your desired config name. (Default: '\\{_default}'): \\")
				if _ConfigName == "":
					return _default
				if not _ConfigName.endswith(".json"):
					_ConfigName = f"{_ConfigName}.json"
				return _ConfigName

			def requestBotConfigDirectory():
				_default = "configs"
				_ConfigDirectory = terminal.input(
					f"Please enter where you'd like to store your configs (Default: '\\{_default}'): \\")
				if _ConfigDirectory == "":
					return _default
				else:
					return _ConfigDirectory

			def requestBotLogDirectory():
				_default = "logs"
				_LogDirectory = terminal.input(f"Please enter where you'd like to store your logs (Default: '\\{_default}'): \\")
				if _LogDirectory == "":
					return _default
				else:
					return _LogDirectory

			def requestBotCogDirectory():
				_default = "cogs"
				_CogDirectory = terminal.input(f"Please enter where you'd like to store your cogs (Default: '\\{_default}'): \\")
				if _CogDirectory == "":
					return _default
				else:
					return _CogDirectory

			def requestInstallDefaultCogs():
				if terminal.confirm(f"Would you like to install the Default Cogs?"):
					return True
				else:
					return False

			settingsConfirmed = False

			while not settingsConfirmed:
				if not hangoutcore.args.debug:
					terminal.clear()
				botToken = requestBotToken()
				# botPrefix = requestBotPrefix() # No longer necessary, here incase needed
				botName = requestBotName(botToken[1])
				botToken = botToken[0] 
				botDescription = requestBotDescription()
				botVersion = requestBotVersion()
				botConfigName = requestBotConfigName()
				botConfigDirectory = requestBotConfigDirectory()
				botLogDirectory = requestBotLogDirectory()
				botCogDirectory = requestBotCogDirectory()
				installDefaultCogs = requestInstallDefaultCogs()

				terminal.print(Panel(title = r"// Bot Settings \\",
									subtitle =  '{0:%d%b%Y %Hh:%Mm}'.format(hangoutcore.init_time),
									renderable = Group(
										"",
										f"Bot Name: [b]{botName}[/b]",
										f"Bot Description: [b]{(str(botDescription[:30]) + '... (String only shortened on terminal to avoid clutter.)') if len(botDescription) > 30 else botDescription}[/b]",
										# f"Bot Prefix: [b]{botPrefix}[/b]",
										f"Bot Version: [b]{botVersion}[/b]",
										f"Bot Config Location: [b]\\{botConfigDirectory}\\{botConfigName}[/b]",
										f"Bot Cog Location: [b]\\{botCogDirectory}[/b]",
										f"Bot Log Location: [b]\\{botLogDirectory}[/b]",
										f"Install Default Cogs: [b]{installDefaultCogs}[/b]",
										f"Bot Token: [b]{terminal.obfuscate(botToken, 0, 6, '*')}[/b]",
										""
									),
								),
								style=f"on {terminal.colorBG}")
				if terminal.confirm(f"Please verify the details above and confirm they are correct."):

					# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
					# Section Title: Create directories / copy files

					terminal.print("")
					terminal.log.INFO(f"Creating a new properties file to store directory settings/locations.")

					p = Properties()
					p["botConfig"] = botConfigName
					p["botConfigDirectory"] = botConfigDirectory
					p["botLogDirectory"] = botLogDirectory
					p["botCogDirectory"] = botCogDirectory

					if not Path.exists(Path(os.path.dirname(__file__)).parent.joinpath("hangoutcore.properties").absolute()):
						terminal.log.INFO(f"Creating config: {Path(os.path.dirname(__file__)).parent.joinpath('hangoutcore.properties').absolute()}")
						with open(f"hangoutcore.properties", "wb") as hangoutcore_config:
							p.store(hangoutcore_config, encoding="utf-8")  # Store provided information in a properties file.
					else:
						terminal.log.WARNING(f"The following file already exists :'hangoutcore.properties'")
						if terminal.confirm(f"Would you like to override it and continue?"):

							with open(f"hangoutcore.properties", "wb") as hangoutcore_config:
								p.store(hangoutcore_config, encoding="utf-8")  # Store provided information in a properties file.

					terminal.print("")
					terminal.log.INFO(f"Creating Directories:")

					if not Path.exists(Path(os.path.dirname(__file__)).parent.joinpath(botConfigDirectory).absolute()):
						terminal.log.INFO(f"Creating Directory: {Path(os.path.dirname(__file__)).parent.joinpath(botConfigDirectory).absolute()}")
						Path.mkdir(botConfigDirectory, parents = True, exist_ok = True)
					else:
						terminal.log.WARNING(f"Directory '\\{botConfigDirectory}' Already Exists, Skipping.")

					if not Path.exists(Path(os.path.dirname(__file__)).parent.joinpath(botCogDirectory).absolute()):
						terminal.log.INFO(f"Creating Directory: {Path(os.path.dirname(__file__)).parent.joinpath(botCogDirectory).absolute()}")
						Path.mkdir(botCogDirectory, parents = True, exist_ok = True)
					else:
						terminal.log.WARNING(f"Directory '\\{botCogDirectory}' Already Exists, Skipping.")

					if not Path.exists(Path(os.path.dirname(__file__)).parent.joinpath(botLogDirectory).absolute()):
						terminal.log.INFO(f"Creating Directory: {Path(os.path.dirname(__file__)).parent.joinpath(botLogDirectory).absolute()}")
						Path.mkdir(botLogDirectory, parents = True, exist_ok = True)
					else:
						terminal.log.WARNING(f"Directory '\\{botLogDirectory}' Already Exists, Skipping.")

					if installDefaultCogs:
						terminal.print("")
						terminal.log.INFO(f"Copying Default Cogs to '\\{botCogDirectory}'")
						for systemCog in os.listdir(f"{Path(os.path.dirname(hangoutcore.utils.__file__)).parent.joinpath('SystemCogs').absolute()}"):
							if systemCog.endswith(f".py"):
								_cogPath = Path(os.path.dirname(__file__)).parent.joinpath(botCogDirectory).absolute()
								_systemCogPath = Path(os.path.dirname(hangoutcore.utils.__file__)).parent.joinpath('SystemCogs').absolute()

								if Path.exists(_cogPath.joinpath(systemCog)):
									terminal.log.WARNING(f"The following file already exists '\\{systemCog}'")
									if terminal.confirm(f"Would you like to override it and continue?"):
										shutil.copyfile(_systemCogPath.joinpath(systemCog), _cogPath.joinpath(systemCog))
								else:
									terminal.log.WARNING(f"Copying the file '\\{systemCog}' to '\\{botCogDirectory}'")
									shutil.copyfile(_systemCogPath.joinpath(systemCog), _cogPath.joinpath(systemCog))
					
					hangoutcore.config.app_config.data = p
					hangoutcore.config.app_config.directory["config"] = botConfigDirectory
					hangoutcore.config.app_config.directory["cogs"] = botCogDirectory
					hangoutcore.config.app_config.directory["logs"] = botLogDirectory
					hangoutcore.config.bot_config.name = botConfigName

					_configDirPath = Path(os.path.dirname(__file__)).parent.joinpath(botConfigDirectory).absolute()
					with open(_configDirPath.joinpath(botConfigName), 'w') as file:
						json.dump(utils.local.botConfig.EXAMPLE_CONFIG, file, indent = 4)

					_config = await utils.local.botConfig.get(_configDirPath.joinpath(botConfigName))

					_config['bot']['token'] = [botToken]
					_config['bot']['name'] = botName
					_config['bot']['version'] = botVersion
					_config['bot']['description'] = botDescription

					await utils.local.botConfig.save(_configDirPath.joinpath(botConfigName), _config)
					break
				else:
					continue
		else:
			sys.exit(1)

	if hangoutcore.args.command == "init":
		await app_setup()

	async def establish_env():

		if hangoutcore.args.new:
			await app_setup()
		else:
			terminal.log.DEBUG(f"Checking if app config exists...")
			_exists = await utils.local.appConfig.exists(hangoutcore.args.app_config)
			terminal.log.DEBUG(f"{hangoutcore.args.app_config}: {_exists}")
			if not _exists:
				await app_setup()
			else:
				_ac = await utils.local.appConfig.get(hangoutcore.args.app_config)
				hangoutcore.config.app_config.name = _ac[0]
				hangoutcore.config.app_config.data = _ac[1]
				hangoutcore.config.app_config.directory["configs"] = _ac[1]["botConfigDirectory"].data
				hangoutcore.config.app_config.directory["cogs"] = _ac[1]["botCogDirectory"].data
				hangoutcore.config.app_config.directory["logs"] = _ac[1]["botLogDirectory"].data
				hangoutcore.config.bot_config.name = _ac[1]["botConfig"].data
				hangoutcore.config.bot_config.path = Path(f"{os.getcwd()}/{hangoutcore.config.app_config.directory["configs"]}/{hangoutcore.config.bot_config.name}")

				terminal.log.DEBUG(f"Checking if bot directories exist...")
				for dir in hangoutcore.config.app_config.directory:
					_exists = os.path.exists(dir)
					terminal.log.DEBUG(f"{dir}: {_exists}")
					if not _exists:
						terminal.log.DEBUG(f"Creating directory '/{dir}'...")
						os.makedirs(dir)

				terminal.log.DEBUG(f"Checking if bot config exists...")
				_bc_exists = await utils.local.botConfig.exists(hangoutcore.config.bot_config.path)
				terminal.log.DEBUG(f"{hangoutcore.config.bot_config.name}: {_bc_exists}")
				if not _bc_exists:
					terminal.log.CRITICAL("Failed to locate bot config.")
					await app_setup()
				else:
					_bc_data = await utils.local.botConfig.get(hangoutcore.config.bot_config.path)
					hangoutcore.config.bot_config.data = _bc_data
					if not await utils.local.botConfig.latest(hangoutcore.config.bot_config.data):
						terminal.log.WARNING(f"Your bot config is out of date.")
						if terminal.confirm("[[red]CONFIRMATION REQUIRED[/red]] Would you like to update?", default = True):
							pass
						hangoutcore.config.bot_config.outdated = True

	async def format_terminal():
		terminal.clear()

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

		if await utils.local.is_package_latest("discord"):
			_discord_version = f"Discord.py Version: [b][green]{discord.__version__}[/b]"
		else:
			_discord_version = f"Discord.py Version: [b]{discord.__version__}[/b] [red reverse](Outdated)"

		if await utils.local.is_package_latest("hangoutcore"):
			_hangoutcore_version = f"HangoutCore Version: [b][green]{hangoutcore.__version__}[/b]"
		else:
			_hangoutcore_version = f"HangoutCore Version: [b]{hangoutcore.__version__}[/b] [red reverse](Version Mismatch)"

		if await utils.local.botConfig.latest(hangoutcore.config.bot_config.data):
			_config_version = f"Bot Config Version:  [b][green]{hangoutcore.config.bot_config.data['_info']['version']}[/b]"
		else:
			_config_version = f"Bot Config Version: [b]{hangoutcore.config.bot_config.data['_info']['version']}[/b] [red reverse](Outdated)"

		if hangoutcore.args.debug:
			terminal.print(
				Panel(
					title = "[red]DEBUG MODE ENABLED",
					subtitle =  '{0:%d%b%Y %Hh:%Mm}'.format(hangoutcore.init_time),
					renderable = Group(
						f"Bot Name: [b][green]{hangoutcore.config.bot_config.data['bot']['name']}[/b]",
						f"Bot Version: [b][green]{hangoutcore.config.bot_config.data['bot']['version']}[/b]",
						f"{_config_version}",
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
					subtitle = '{0:%d%b%Y %Hh:%Mm}'.format(hangoutcore.init_time),
					renderable = Group(
						f"Bot Name: [b]{hangoutcore.config.bot_config.data['bot']['name']}[/b]",
						f"Bot Version: [green]{hangoutcore.config.bot_config.data['bot']['version']}",
						f"{_config_version}",
						f"{_discord_version}",
						f"{_hangoutcore_version}"
					)
				),
				justify="center")

	async def establish_db_conn():
		terminal.log.INFO("Establishing database connection...")

	async def start_bot():
		pass

	await establish_env()
	await format_terminal()
	await establish_db_conn()

def init():
	try:
		asyncio.run(main())
	except KeyboardInterrupt:
		pass
	except Exception as err:
		print(f"ERROR: {err}")
	pass


if __name__ == "__main__":
	init()
