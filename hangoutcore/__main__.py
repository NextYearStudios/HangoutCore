"""
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    HangoutCore Main Script
        › Please do not modify any of the following content unless you know what you're doing. Modifying the following code and not updating the rest of the bot code to match can/will cause issues.
        › If you do decide to modify the following code please understand that HangoutCore's Dev team, Discord.py's Dev Team nor Python's Dev team are obligated to help you.
        › By Modifying the following code you acknowledge and agree to the text above.
    Module Last Updated: December 7, 2022
    Module Last Updated by: Lino
    License: Refer to LICENSE.md
    Notes:
        None
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
import anyio
import asyncio
import click
import sys

from hangoutcore.util import *
from hangoutcore.bot import HangoutCoreBot

# @click.command()
# @click.option('--debug','-d', default=False, help="Enable bot debug mode.")
# @click.option('--config','-c', default=None, help="Specify which config the bot should use.")
# @click.option('--token','-t', default=-1, help="Specify which token the bot should use from the config.")
async def main():
    debug = False
    config = None
    token = -1
    if '-h' in sys.argv[1:] or '--help' in sys.argv[1:]:
        print(f"""

    ██╗░░██╗░█████╗░███╗░░██╗░██████╗░░█████╗░██╗░░░██╗████████╗░█████╗░░█████╗░██████╗░███████╗
    ██║░░██║██╔══██╗████╗░██║██╔════╝░██╔══██╗██║░░░██║╚══██╔══╝██╔══██╗██╔══██╗██╔══██╗██╔════╝
    ███████║███████║██╔██╗██║██║░░██╗░██║░░██║██║░░░██║░░░██║░░░██║░░╚═╝██║░░██║██████╔╝█████╗░░
    ██╔══██║██╔══██║██║╚████║██║░░╚██╗██║░░██║██║░░░██║░░░██║░░░██║░░██╗██║░░██║██╔══██╗██╔══╝░░
    ██║░░██║██║░░██║██║░╚███║╚██████╔╝╚█████╔╝╚██████╔╝░░░██║░░░╚█████╔╝╚█████╔╝██║░░██║███████╗
    ╚═╝░░╚═╝╚═╝░░╚═╝╚═╝░░╚══╝░╚═════╝░░╚════╝░░╚═════╝░░░░╚═╝░░░░╚════╝░░╚════╝░╚═╝░░╚═╝╚══════╝
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[-c, --config : string  ] Load the specified config, Also sets as default. If the specified config cannot be found, return to previous config as a precaution.
[-d, --debug  : bool    ] Enable debug mode for more information to be displayed in the terminal. Changes log mode to DEBUG.
[-n, --new    : empty   ] Manually put HangoutCore in a setup state in order to create a new configuration. Sets the new config as default.
[-s, --silent : bool    ] Enable/Disable to have information sent to log only, or terminal and log(). Useful for running as a service since there's no access to terminal.
[-t, --token  : integer ] Specify which token to use if you're using multiple. Allows user to skip token choice prompt.
        """)
        sys.exit(0)
    if len(sys.argv[1:]) >= 2:
        pass
    print(sys.argv[1:])
    print(len(sys.argv[1:]))
    print('test')


def init():
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        Terminal().Log().CRITICAL(f"Please refrain from using CTRL+C to shutdown bot.")
        Terminal().Log().CRITICAL(f"Shutting Down...")
        sys.exit(0)
    except:
        Terminal().Log().CRITICAL(f"Shutting Down...")
        sys.exit(0)

if __name__ == "__main__":
    init()