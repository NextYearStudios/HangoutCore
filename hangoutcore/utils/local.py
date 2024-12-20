'''
	HangoutCore Module Script.
	----------
	Last Updated: June 24, 2024
	Last Updated by: Lino
	License: Refer to LICENSE.md
	Notes:
		None
	━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	This script handles the following:
	----------
	Local file handling
	━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	WARNING: This is a Core Script
		› Please do not modify any of the following content unless you know what you're doing. Modifying the following code and not updating the rest of the bot 
			code to match can/will cause issues.
		› If you do decide to modify the following code please understand that HangoutCore's Dev team, Discord.py's Dev Team nor Python's Dev team are obligated
			to help you.
		› By Modifying the following code you acknowledge and agree to the text above.
	━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
'''
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Section Title: Dependencies

import discord
import hangoutcore
import json
import os
import requests
import shutil
import sys
import traceback
from typing import Optional

import hangoutcore.SystemCogs


from discord.ext import commands
from jproperties import Properties
from pathlib import Path
from typing import Union

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Section Title: Functions


class appConfig(object):

	@staticmethod
	async def exists(config: str = 'hangoutcore.properties'):
		if not config.endswith('.properties'):
			config += '.properties'

		if os.path.exists(config) and os.path.isfile(config):
			return True
		else:
			return False

	@staticmethod
	async def get(config: str = 'hangoutcore.properties'):
		log = hangoutcore.log
		if not config.endswith('.properties'):
			config += '.properties'
		
		def failLocate():
			log.ERROR(f"Attempted to locate properties file '{config}'. Nothing was found.")
			return None

		log.DEBUG(f"Attempting to locate properties file '{config}'.")
		if await appConfig.exists(config):
			try:
				with open(config, 'r+b') as hangoutcore_config:
					log.DEBUG(f"Successfully located '{config}'.")
					p = Properties()
					p.load(hangoutcore_config, 'utf-8')
					return [config, p]
			except FileNotFoundError:
				failLocate()
		else:
			failLocate()

class botConfig(object):
	CONFIG_VERSION = 6.4
	EXAMPLE_CONFIG = {  # Changing this will only matter when the bot creates a new Config(). Actual config at CONFIG_PATH
		'bot': {
			'prefixes': ['!'],
			# Bot uses this array for prefixes. Add as many as you want, and keep in mind you can include spaces but be careful not to over complicate your prefixes.
			'token': [''],
			# If you intend on using any token other than the first in the list, change hangoutcore.py to match.
			'intents': {
				'guilds': False,
				'members': False,
				'bans': False,
				'emojis': False,
				'emojis_and_stickers': False,
				'integrations': False,
				'webhooks': False,
				'invites': False,
				'voice_states': False,
				'presences': False,
				'messages': False,
				'guild_messages': False,
				'dm_messages': False,
				'reactions': False,
				'guild_reactions': False,
				'dm_reactions': False,
				'typing': False,
				'guild_typing': False,
				'dm_typing': False,
				'message_content': False,
				'guild_scheduled_events': False,
				'auto_moderation': False,
				'auto_moderation_configuration': False,
				'auto_moderation_execution': False
			},
			'status': {
				'type': 'listening',  # Valid Options are competing, playing, listening, streaming, watching
				'name': '!help',  # Activity Name
				'game': '',
				'url': ''  # Twitch or Youtube URL if type is Streaming
			},
			'name': 'Bot Name',  # Bot name
			'version': '0.0.0',  # Bot version
			'description': 'Bot Description would go here.',
			'developer_guild_id': 000000000,  # Developer guild id for  Used for test commands.
			'contributers': [
				{
					'name': 'Contributer Name',  # Contributer name
					'discord_id': 000000000,  # Contributer discord id
					'owner': False,  # Set this to true if they're an owner. otherwise set it to False
					'developer': False
				}
			],
			'apis': [
				{
					'name': 'Api Name',  # API Name for display sake
					'token': 'Api Token',  # API Token for accessing API Data
					'header': {'Authorization': ''}  # API Header for ease of use
				}
			],
			'messages': {
				# The following section is for specifying various messages the bot will use. 
				# --------------------------------------------------------------------------------------------------------------------------------------------
				# This helps keep our code a little bit cleaner by keeping common messages in one place thats easily accessible from code anywhere in our bot
				# --------------------------------------------------------------------------------------------------------------------------------------------
				# The message names below are structured as follows:
				# message_type message_focus message_reason
				# Example:
				# error_guild_blacklisted
				# This message would be shown as an 'Error' involving the 'Guild' being 'Blacklisted'.
				#
				# warning_user_timeout
				# This message would be shown as a 'Warning' involving the 'User' being 'Timed Out', potentially showing the reason and/or time.
				#
				# messages consist of 2 entries in an array:
				# [Message_Number, Message]
				# Message Numbers should be assigned based on severity, This makes it easier to keep track of an error level simply by looking at the Number assigned.
				# 
				# --------------------------------------------------------------------------------------------------------------------------------------------
				# References in messages:
				# As long as these messages are fetched using the 'botErrorEmbed' function, references are handling dynamically.
				# Please see the documentation for that function to get more info.
				# --------------------------------------------------------------------------------------------------------------------------------------------
				'example_error': [0, 'Error Response to user'],

				'error_bot_fail': [101, 'Uh oh, Appears my code failed somewhere.\nPlease try again later, If this error persists please submit a ticket via our support server.'],
				'error_bot_invaliddatabaseconfiguration': [102, 'Failed to access database.\nPlease try again later, If this error persists please submit a ticket via our support server.'],
				'error_bot_invalidguilddata': [103, 'Failed to retreive data for this guild.\nPlease try again later, If this error persists please submit a ticket via our support server.'],
				'error_bot_invaliduserdata': [104, 'Failed to retreive data for this user.\nPlease try again later, If this error persists please submit a ticket via our support server.'],
				
				'error_user_blacklisted': [201, "You're currently blacklisted from using this bot.\nreason: `{blacklist_reason}`"],
				'error_user_blacklisted_noreason': [201, "You're currently blacklisted from using this bot.\nreason: `No Reason could be found, Please submit a ticket via our support server.`"],
				'error_user_insufficientpermissions': [202, 'You do not have the necessary permissions to use that. This event has been logged and a staff member has been notified.'],
				'error_user_invalidguildbalance': [203, 'Failed to retreive user balance.\nPlease try again later, If this error persists please submit a ticket via our support server.'],
				'error_user_insufficientguildbalance': [204, 'Sorry, You have insufficient funds to perform this action.'],

				'error_command_arg_uniquemember': [301, 'Sorry, You have to select someone other than yourself.'],
				'error_command_arg_botmember': [302, 'Sorry, You have to select an actual member. Bot members are not allowed.'],
				'error_command_arg_positive': [303, 'Sorry, You must provide a positive number greater than 0.'],

				'error_system_notenabled': [401, 'Sorry, {system_name} is not enabled here.']
			},
			'emoji': {
				'nsfw': '<:nsfw:1056285352723230751>'
			}
		},
		'database': {
			'type': 'mysql',
			'host': 'localhost',
			'port': 3306,
			'name': 'database',  # db name
			'user': 'user',
			'password': 'pass'
		},
		'music': {
			'vc_timeout': True,
			'vc_timeout_duration': 600,
			'max_volume': 250,  # Max Volume
			'vote_skip': True,  # whether vote skip is enabled or not.
			'vote_skip_ratio': 0.5  # minimum ratio needed for vote skip
		},
		'_info': {  # config info
			'version': CONFIG_VERSION,  # config version
			'update_reason': 'Initial Creation'
		}
	}

	@staticmethod
	async def exists(config: Path | str) -> bool:
		if not str(config).endswith('.json'):
			config = config.joinpath('.json')
		
		if Path.exists(config):
			return True
		else:
			return False
	
	
	@staticmethod
	async def get(config: Path | str):
		log = hangoutcore.log
		if not str(config).endswith('.json'):
			config = config.joinpath('.json')

		def failLocate():
			log.ERROR(f"Attempted to locate '{config}'. Nothing was found.")
			return None

		if await botConfig.exists(config):
			try:
				log.DEBUG(f"Attempting to locate '{config}'.")
				with open(config) as bot_config:
					configJSON = json.load(bot_config)
					return configJSON
			except FileNotFoundError:
				failLocate()
		else:
			failLocate()
		
#     @staticmethod
#     async def update(config: Optional[str | Path | None] = None):
#         '''
#         This function attempts to update the provided bot config, If one is not provided it will update the active bot config.
#         ``Warning: Not Implemented``
		
#         Parameters:
#         ------------
#         directory: :class:`str`, :class:`Path`, or :class:`None`
#             The parent directory our config is located in.
#         config: :class:`str`, or :class:`None`
#             The name of our target config.
#         '''
		
#         if config is None:
#             config = Path(hangoutcore.DIRECTORY_CONFIGS).joinpath(hangoutcore.CONFIG_BOT_NAME).absolute()
			
#         if not str(config).endswith('.json'):
#             config = config.joinpath('.json')
			
#         if not Path.exists(config):
#             terminal.log.ERROR(f"Error: Unable to update bot config. Provided config name: {config} does not exist.")
		
#         with open(config, 'w') as configFile:
#             _ogConfig: dict = hangoutcore.CONFIG_BOT
#             _newConfig: dict = botConfig.EXAMPLE_CONFIG
#             _newConfig['_info']['update_reason'] = f'Update to config version: {botConfig.CONFIG_VERSION}'
#             for key in _ogConfig['bot'].keys():
#                 terminal.print(f"Key: {key}")
#                 if key != 'intents' and key != 'messages':
#                     _newConfig['bot'][key] = _ogConfig['bot'][key]

#             for key in _ogConfig['database'].keys():
#                 terminal.print(f"Key: {key}")
#                 _newConfig['database'][key] = _ogConfig['database'][key]

#             for key in _ogConfig['music'].keys():
#                 terminal.print(f"Key: {key}")
#                 _newConfig['music'][key] = _ogConfig['music'][key]
#             json.dump(_newConfig, configFile, indent = 4)
			
#             hangoutcore.CONFIG_BOT = _newConfig
			
#     @staticmethod
#     async def save(config: Optional[str | Path | None] = None, data: Optional[dict | str] = None):
#         '''
#         This function attempts to update the provided bot config, If one is not provided it will update the active bot config.
#         ``Warning: Not Implemented``
		
#         Parameters:
#         ------------
#         directory: :class:`str`, :class:`Path`, or :class:`None`
#             The parent directory our config is located in.
#         config: :class:`str`, or :class:`None`
#             The name of our target config.
#         '''
		
#         if config is None:
#             config = Path(hangoutcore.DIRECTORY_CONFIGS).joinpath(hangoutcore.CONFIG_BOT_NAME).absolute()
			
#         if not str(config).endswith('.json'):
#             config = config.joinpath('.json')
			
#         if not Path.exists(config):
#             terminal.log.ERROR(f"Error: Unable to update bot config. Provided config name: {config} does not exist.")
		
#         with open(config, 'w') as configFile:
#             json.dump(data, configFile, indent = 4)

#     @staticmethod
#     async def is_developer(user: Optional[discord.User | discord.Member]):
#         '''
#         This function takes the provided `user` and verifies their status against our current bot config.
		
#         Parameters:
#         ------------
#         user: :class:`discord.User` or :class:`discord.Member`
#             The target user we are verifying.
			
#         Returns:
#         ------------
#         ``True``
#             If user matches config.
#         ``False``
#             If user does not.
#         '''
#         for contributer in hangoutcore.CONFIG_BOT['bot']['contributers']:
#             if contributer['discord_id'] == user.id and contributer['developer'] == True:
#                 return True
#             else:
#                 return False
			
#     @staticmethod
#     async def is_owner(user: Optional[discord.User | discord.Member]):
#         '''
#         This function takes the provided `user` and verifies their status against our current bot config.
		
#         Parameters:
#         ------------
#         user: :class:`discord.User` or :class:`discord.Member`
#             The target user we are verifying.
			
#         Returns:
#         ------------
#         ``True``
#             If user matches config.
#         ``False``
#             If user does not.
#         '''
#         for contributer in hangoutcore.CONFIG_BOT['bot']['contributers']:
#             if contributer['discord_id'] == user.id and contributer['owner'] == True:
#                 return True
#             else:
#                 return False
			
#     @staticmethod
#     async def is_contributer(user: Optional[discord.User | discord.Member]):
#         '''
#         This function takes the provided `user` and verifies their status against our current bot config.
		
#         Parameters:
#         ------------
#         user: :class:`discord.User` or :class:`discord.Member`
#             The target user we are verifying.
			
#         Returns:
#         ------------
#         ``True``
#             If user matches config.
#         ``False``
#             If user does not.
#         '''
#         for contributer in hangoutcore.CONFIG_BOT['bot']['contributers']:
#             if contributer['discord_id'] == user.id:
#                 return True
#             else:
#                 return False

# async def dirExists(directory: str, create: bool = False):
#     if not create:
#         return Path.exists(f'{directory}')
#     Path(f'{directory}').mkdir(parents = True, exist_ok = True)
#     return True

# async def is_latest(package_name: str):
#     _package = sys.modules[package_name]
#     response = requests.get(f'https://pypi.org/pypi/{package_name}/json')
#     latest_version = response.json()['info']['version']
#     if _package.__version__ is not None:
#         # terminal.log.DEBUG(f'{package_name}: {latest_version} | {_package.__version__}')
#         if latest_version > _package.__version__ or latest_version < _package.__version__: # Throws False if local is newer than online to remind user that local is not matching public version
#             return False
#         else:
#             return True
#     elif _package.version is not None:
#         # terminal.log.DEBUG(f'{package_name}: {latest_version} | {_package.version}')
#         if latest_version > _package.version or latest_version < _package.version:
#             return False
#         else:
#             return True

# async def GetCogs(cogDirectory: str) -> Union[dict[str, list[str]], None]:

#         try:
#             valid_files = []
#             disabled_files = []
#             invalid_files = []
#             for file in os.listdir(cogDirectory):
#                 if file.endswith('.py'):
#                     valid_files.append(file)
#                 elif file.endswith('.disabled'):
#                     disabled_files.append(file)
#                 else:
#                     if file == '__pycache__' or '__init__':
#                         pass
#                     else:
#                         invalid_files.append(file)
#             package = {
#                 'valid_files': valid_files,
#                 'invalid_files': invalid_files,
#                 'disabled_files': disabled_files
#             }
#             return package
#         except Exception as e:
#             terminal.log.CRITICAL(f'{e}')
#             return None

# async def load_extensions(discordBot:commands.Bot, cogDirectory : str, systemCogs: bool = False): # discordBot: commands.Bot, debug_mode: bool = False, systemCogs: bool = False
	#     '''
	#     Scans through the directory provided, automatically sorts via file types into Valid, Invalid, and Disabled filetypes. Attempts to load any files ending in '.py'
	#     '''
		
	#     async def _loadCogs(_cogs, _directory: str, _system: bool = False):
	#         if _cogs is not None:
	#             if len(_cogs['disabled_files']) > 0: # Skip any files ending in .disabled
	#                 for _cog in _cogs['disabled_files']:
	#                     terminal.log.INFO(f' └ Found Disabled file {_cog}, Skipping.')
				
	#             if len(_cogs['invalid_files']) > 0:
	#                 for _cog in _cogs['invalid_files']: # Skip any file not ending in .py or .disabled
	#                     if _cog == '__pycache__' or '__init__':
	#                         pass
	#                     else:
	#                         terminal.log.INFO(f' └ Found invalid file {_cog}, Skipping.')
				
	#             if len(_cogs['valid_files']) > 0: # attempt to load the .py files we located in our directory. 
	#                 for _cog in _cogs['valid_files']:
	#                     terminal.log.INFO(f' └ Found {_cog}')
	#                     try:
	#                         await discordBot.load_extension(f'{_directory}.{_cog[:-3]}')
	#                     except Exception as _error:
	#                         terminal.log.ERROR(f'{_error}\n\n{traceback.format_exc()}')
	#                     else:
	#                         if _system:
	#                             terminal.log.INFO(f'  └ successfully loaded system module: {_cog}')
	#                         else:
	#                             terminal.log.INFO(f'  └ successfully loaded module: {_cog}')

		
	#     _coglist = os.listdir(cogDirectory)
		
	#     if not hangoutcore.SILENT and hangoutcore.SystemCogs:
		
	#         terminal.print_hr(title='Looking for System Modules')
	#         if systemCogs:
	#             _systemcogPath = str(Path(os.path.dirname(__file__)).parent.joinpath('SystemCogs').absolute())
	#             _systemCogList = os.listdir(_systemcogPath)
				
	#             if len(_systemCogList) >= 1:
					
	#                 for _scog in _systemCogList:
	#                     if not _coglist.__contains__(_scog) and not _scog.endswith(".disabled"):
	#                         if terminal.confirm(f"System module '{_scog}' does not appear to be in your cog directory, would you like to make a local copy of it now?"):
	#                             shutil.copyfile(f"{_systemcogPath}/{_scog}", f"{cogDirectory}/{_scog}", follow_symlinks = True)
	#                             terminal.log.INFO(f"Successfully copied '{_scog}' to '{cogDirectory}'")
	#                         else:
	#                             continue
		
	#     # Load Local cogs after handling system cogs
		
	#     terminal.print_hr(title=f"Looking for Modules in '/{cogDirectory}'")
	#     cogs = await GetCogs(cogDirectory)
	#     await _loadCogs(cogs, cogDirectory)
		