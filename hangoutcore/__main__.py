import asyncio
import sys, os, pathlib, logging
# sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "../")))
# print(sys.path)
import hangoutcore
from hangoutcore import utils

hangoutcore.terminal[os.getpid()] = utils.terminal("HC.Main", hangoutcore.logger["HangoutCore"])
terminal = hangoutcore.terminal[os.getpid()]
log = terminal.log = terminal.Log("HC.Main", hangoutcore.logger["HangoutCore"])
# hangoutcore.terminal = terminal
# hangoutcore.log = log

async def __main__():
	_logFormatter = logging.Formatter("""[%(name)s][%(levelname)s] %(message)s""", "%m/%d/%Y %I:%M:%S %p")
	_fileHandler = logging.FileHandler(
		filename = fr"{os.getcwd()}\\init.log",
		mode = "w",
		encoding = "utf-8",
		delay = False,
		errors = None
	)
	_fileHandler.setFormatter(_logFormatter)

	hangoutcore.logger["HangoutCore"].addHandler(_fileHandler)
	hangoutcore.logger["HangoutCore"].setLevel(logging.NOTSET)

	# print(os.getcwd())
	log.DEBUG("[b]test[/b]")
	log.DEBUG("Starting...")
	log.DEBUG(os.getpid())
	log.DEBUG(os.getppid())
	log.DEBUG(hangoutcore.terminal)
	log.DEBUG(f"{os.getcwd()}\\init.log")
	log.DEBUG(os.path.exists(f"{os.getcwd()}\\init.log"))
	log.DEBUG(sys.argv)

def __init__():
	try:
		log.INFO("Starting...")
		asyncio.run(__main__())
	except Exception as err:
		log.ERROR(f"[b]{err}[/b]")
		raise err

if __name__ == "__main__":
	__init__()