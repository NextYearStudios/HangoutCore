import hangoutcore; from hangoutcore import utils
import logging
import subprocess
import threading
import sys, os

# sys.path.append(os.getcwd())

from rich.console import Group
from rich.logging import RichHandler
from rich.panel import Panel

terminal = hangoutcore.terminal[os.getpid()]
log = terminal.log
# hangoutcore.terminal = terminal
# hangoutcore.log = log

def __init__():
	
	# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	# Section Description: Logging config
	_logFormatter = logging.Formatter("""[%(name)s][%(levelname)s] %(message)s""", "%m/%d/%Y %I:%M:%S %p")
	_fileHandler = logging.FileHandler(
		filename = fr"init.log",
		mode = "w",
		encoding = "utf-8",
		delay = False,
		errors = None
	)
	_fileHandler.setFormatter(_logFormatter)

	hangoutcore.logger["HangoutCore"].addHandler(_fileHandler)
	hangoutcore.logger["HangoutCore"].setLevel(logging.NOTSET)

	# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	# Section Description: Main process
	def start_main_process():
		process = subprocess.Popen(
			[f"{sys.executable}", f"{os.path.dirname(os.path.abspath(__file__))}\\__main__.py"],
			cwd=os.getcwd(),
			# encoding="UTF-8",
			env=os.environ.copy(),
			stdout=subprocess.PIPE,
			stderr=subprocess.STDOUT,
			text=False
		)
		for line in process.stdout:
			terminal.console.print(line, end="")
		process.wait()
		if process.returncode == 0:
			log.INFO("Subprocess finished successfully.")
		else:
			log.INFO(f"Subprocess finished with return code {process.returncode}.")

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
				hangoutcore.config.app_config.name = _arg_appconfig['value']
			else:
				_invalidArgs.append({'arg': '--app-config', 'value': 2})

		if _arg_botconfig['exists']:
			if _arg_botconfig['value'] is not None:
				hangoutcore.config.bot_config = _arg_botconfig['value']
			else:
				_invalidArgs.append({'arg': '--bot-config', 'value': 2})

		if _arg_debug['exists']:
			if _arg_debug['value'] is not None:
				hangoutcore.DEBUG = _arg_debug['value']
				if _arg_debug['value']:
					hangoutcore.logger["HangoutCore"].setLevel(logging.DEBUG)
					hangoutcore.logger["Discord"].setLevel(logging.DEBUG)
				else:
					hangoutcore.logger["HangoutCore"].setLevel(logging.INFO)
					hangoutcore.logger["Discord"].setLevel(logging.INFO)
			else:
				_invalidArgs.append({'arg': '--debug', 'value': 3})

		if _arg_new['exists']:
			if _arg_new['value'] is not None:
				hangoutcore.fresh_install = _arg_new['value']
			else:
				_invalidArgs.append({'arg': '--new', 'value': 3})

		if _arg_silent['exists']:
			if _arg_silent['value'] is not None:
				hangoutcore.silent = _arg_silent['value']
				terminal.__setsilent__(_arg_silent['value'])
				log.__setsilent__(_arg_silent['value'])
			else:
				_invalidArgs.append({'arg': '--silent', 'value': 3})

		if _arg_systemcogs['exists']:
			if _arg_systemcogs['value'] is not None:
				hangoutcore.system_cogs = _arg_systemcogs['value']
			else:
				_invalidArgs.append({'arg': '--system-cogs', 'value': 3})

		if _arg_token['exists']:
			if _arg_token['value'] is not None:
				hangoutcore.token = _arg_token['value']
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

	if hangoutcore.token is not None:
		can_continue = True

	# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	# Section Description: Setup title

	terminal.clear()
	# terminal.print_hr()
	terminal.print(Panel(Group(
		"██╗░░██╗░█████╗░███╗░░██╗░██████╗░░█████╗░██╗░░░██╗████████╗░█████╗░░█████╗░██████╗░███████╗",
		"██║░░██║██╔══██╗████╗░██║██╔════╝░██╔══██╗██║░░░██║╚══██╔══╝██╔══██╗██╔══██╗██╔══██╗██╔════╝",
		"███████║███████║██╔██╗██║██║░░██╗░██║░░██║██║░░░██║░░░██║░░░██║░░╚═╝██║░░██║██████╔╝█████╗░░",
		"██╔══██║██╔══██║██║╚████║██║░░╚██╗██║░░██║██║░░░██║░░░██║░░░██║░░██╗██║░░██║██╔══██╗██╔══╝░░",
		"██║░░██║██║░░██║██║░╚███║╚██████╔╝╚█████╔╝╚██████╔╝░░░██║░░░╚█████╔╝╚█████╔╝██║░░██║███████╗",
		"╚═╝░░╚═╝╚═╝░░╚═╝╚═╝░░╚══╝░╚═════╝░░╚════╝░░╚═════╝░░░░╚═╝░░░░╚════╝░░╚════╝░╚═╝░░╚═╝╚══════╝",
		"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
		"Attention: Please note that 'HC' is the official abbreviation for our name and may be used interchangeably in our communications and materials.",
	)), justify="center", alt = "Program Title")
	# terminal.print_hr()

	# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	# Section Description: Begin main process

	for directory in hangoutcore.directory:
		if not os.path.isdir(directory):
			log.CRITICAL(f"{directory} does not exist, creating.")
			os.makedirs(directory)

	if can_continue:
		log.DEBUG("Starting Main Process")
		thread = threading.Thread(target=start_main_process)
		thread.start()
		thread.name = "HangoutCore (Main Process)"
		log.DEBUG("Started Main Process")

if __name__ == "__main__":
	__init__()
