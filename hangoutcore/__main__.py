import os

import discord

import hangoutcore

# import hangoutcore.bot
# import hangoutcore.setup
import hangoutcore.utils


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
    # hangoutcore.terminal[os.getpid()] = hangoutcore.utils.terminal(
    #     "HC.Main", hangoutcore.logger["HangoutCore"]
    # )
    # terminal = hangoutcore.terminal[os.getpid()]
    # log = terminal.log = terminal.Log("HC.Main", hangoutcore.logger["HangoutCore"])

    print(hangoutcore.__version__)
    # log.DEBUG("Test")

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
