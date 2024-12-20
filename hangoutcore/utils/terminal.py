"""
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
	Terminal Manipulation/Handling
	━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	WARNING: This is a Core Script
		› Please do not modify any of the following content unless you know what you're doing. Modifying the following code and not updating the rest of the bot 
			code to match can/will cause issues.
		› If you do decide to modify the following code please understand that HangoutCore's Dev team, Discord.py's Dev Team nor Python's Dev team are obligated
			to help you.
		› By Modifying the following code you acknowledge and agree to the text above.
	━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
import logging
import shutil
import sys

from rich.align import AlignMethod
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.rule import Rule
from rich.style import Style
from rich.text import Text, TextType

class Terminal(object):

	class ExtensionAlreadyLoadedError(Exception):
		"""Exception raised for attempting to load duplicate extensions.

		Attributes:
			extension -- extension which caused the error
			message -- explanation of the error
		"""

		def __init__(self, extension, message = None):
			if message is None:
				message = f"Failed to load extension '{extension}', It is already loaded."
			self.extension = extension
			self.message = message
			super().__init__(self.message)


	def __init__(self, module = None, logger = None) -> None:
		self.module = module
		self.logger: logging.Logger = logger
		self.silent: bool = False
		self.colorBG = "rgb(32,32,32)"
		self.colorFG = ""
		self.log = self.Log()

		self.console = Console(
			record = False,
			# style = f"{colorFG} on {colorBG}"
		)
		self.Log.console = self.console
		self.Log.module = self.module
		self.Log.logger = self.logger

	def __setsilent__(self, value: bool):
		self.silent = value
		
	class Log(object):
		console = None
		module = None
		logger = None
		silent = False

		def __init__(self, module = None, logger = None, silent: bool = False) -> None:
			self.module = module
			self.logger = logger
			self.silent = silent
			self.colors = {
				"debug":"cyan",
				"info":"green",
				"warning":"red",
				"error":"on red",
				"critical":"on red"
			}

		def __setsilent__(self, value: bool):
			self.silent = value

		def __checklogger__(self) -> bool:
			if self.logger is None:
				return False

			if type(self.logger) == str:
				self.logger = logging.getLogger(self.logger)

			if type(self.logger) == logging.Logger:
				return True

		def __checklevel__(self, level) -> bool:
			if level >= self.logger.level:
				return True
			else:
				return False

		def DEBUG(self, log: str):
			_prefix = f"[[{self.colors['debug']}]DEBUG[/{self.colors['debug']}]]"
			_suffix = f""
			
			if self.module is not None:
				_prefix = f"[[b]{self.module}[/b]]{_prefix}"
			
			if self.__checklogger__():
				self.logger.debug(f"Printed: {log}")
			
			if self.__checklevel__(logging.DEBUG) and not self.silent:
				self.console.print(f"{_prefix} {log} {_suffix}", justify = "left")

		def INFO(self, log: str):
			_prefix = f"[[{self.colors['info']}]INFO[/{self.colors['info']}]]"
			_suffix = f""
			
			if self.module is not None:
				_prefix = f"[[b]{self.module}[/b]]{_prefix}"
			
			if self.__checklogger__():
				self.logger.info(f"Printed: {log}")
			
			if self.__checklevel__(logging.INFO) and not self.silent:
				self.console.print(f"{_prefix} {log} {_suffix}", justify = "left")

		def WARNING(self, log: str):
			_prefix = f"[[{self.colors['warning']}]WARNING[/{self.colors['warning']}]]"
			_suffix = f""
			
			if self.module is not None:
				_prefix = f"[[b]{self.module}[/b]]{_prefix}"
			
			if self.__checklogger__():
				self.logger.warning(f"Printed: {log}")
			
			if self.__checklevel__(logging.WARNING) and not self.silent:
				self.console.print(f"{_prefix} {log} {_suffix}", justify = "left")

		def ERROR(self, log: str):
			_prefix = f"[{self.colors['error']}][ERROR][/{self.colors['error']}]"
			_suffix = f""
			
			if self.module is not None:
				_prefix = f"[[b]{self.module}[/b]]{_prefix}"
			
			if self.__checklogger__():
				self.logger.error(f"Printed: {log}")
			
			if self.__checklevel__(logging.ERROR) and not self.silent:
				self.console.print(f"{_prefix} {log} {_suffix}", justify = "left")

		def CRITICAL(self, log: str):
			_prefix = f"[CRITICAL]"
			_suffix = f""
			
			if self.module is not None:
				_prefix = f"[[b]{self.module}[/b]]{_prefix}"
			
			if self.__checklogger__():
				self.logger.critical(f"Printed: {log}")
			
			if self.__checklevel__(logging.CRITICAL) and not self.silent:
				self.console.print(f"[{self.colors['critical']}]{_prefix} {log} {_suffix}", justify = "left")

	def clear(self):
		"""Clears the terminal."""
		# os.system("clear || cls")
		if not self.silent:
			self.logger.debug(f"Cleared the terminal.")
			self.console.clear()

	def print(self, message: object, alt: str = None, **kwargs):
		if not self.silent:
			if alt is None:
				self.logger.debug(f"Printed: {message}")
			else:
				self.logger.debug(f"Printed: {alt}")
			self.console.print(message, **kwargs,)

	def print_center(self, message: str, fill_char: str = " "):
		self.print(message.center(shutil.get_terminal_size().columns, fill_char), alt = f"{message}")

	def print_hr(self, title: str|Text = "", *, characters: str = "─", style: str|Style = f"white", end: str = "\n",align: AlignMethod = "center", **kwargs):
		if not self.silent:
			if title != "":
				_suffix = f" with the title {title}"
			else:
				_suffix = f""
			self.logger.debug(f"Printed a horizontal line{_suffix}.")
			self.console.print(Rule(title=title, characters=characters, style=style, end=end, align=align, **kwargs))

	def input(self, prompt: TextType, **kwargs):
		if not self.silent:
			self.logger.debug(f"Requested user input with the following prompt: {prompt}")
			try:
				_response = Prompt.ask(prompt, console = self.console, **kwargs)
			except:
				self.logger.debug(f"Input recieved None.")
				return None
			finally:
				if _response is not None:
					if kwargs.get("password"):
						self.logger.debug(f"Recieved input: (PROTECTED) {self.obfuscate(_response, 0, 0, '*')}.")
					else:
						self.logger.debug(f"Recieved input: {_response}.")
					return _response
		else:
			self.logger.critical("Input required, Could not request input in silent mode.")
			sys.exit(1)

	def confirm(self, prompt: object, **kwargs):
		if not self.silent:
			self.logger.debug(f"Requested user confirmation with the following prompt: {prompt}")
			_response = Confirm.ask(prompt, console = self.console, **kwargs)
			self.logger.debug(f"Recieved confirmation: {_response}.")
			return _response
		else:
			self.logger.critical("Confirmation required, Could not request input in silent mode.")
			sys.exit(1)

	def obfuscate(self, inputString:str, start:int=0, end:int=4, obfuscateChar:str='#'):
		"""
		Used for allowing our user to recognize a string/token while keeping the rest of it hidden from prying eyes such as a twitch stream, a screen recording or any other public environment.
		"""

		outputString = ""
		for i in range(len(inputString)):

			if (start + end) >= len(inputString):
				outputString = inputString
				break

			if (i + 1) < start and i < len(inputString) - end:
				outputString += inputString[i]
				continue

			if (i + 1) > start and i < len(inputString) - end:
				if inputString[i] == '.':
					outputString = outputString + inputString[i]
				else:
					outputString = outputString + obfuscateChar
			# elif i == len(inputString) - amount:
			#     outputString = outputString + "-" + inputString[i]
			else:
				outputString = outputString + inputString[i]
		return outputString