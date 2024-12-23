import discord

import hangoutcore, hangoutcore.utils, hangoutcore.bot, hangoutcore.setup

async def main():
    async def process_args():
        pass

    async def format_terminal():
        pass

    async def establish_logger():
        pass

    async def establish_db_conn():
        pass

    async def start_bot():
        pass

    pass

def init():
    debug = True
    print(hangoutcore.__version__)
    hangoutcore.utils.terminal.print("Test")

    if debug:
        print(hangoutcore.version)
    else:
        try:
            pass
        except KeyboardInterrupt:
            pass
        except Exception as err:
            pass
        pass

if __name__ == "__main__":
    init()