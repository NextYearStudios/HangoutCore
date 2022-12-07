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
import asyncio
import sys

from hangoutcore.util import *
from hangoutcore.bot import HangoutCoreBot

async def main():
    print(sys.argv)

async def init():
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        Terminal().Log().CRITICAL(f"Please refrain from using CTRL+C to shutdown bot.")
        Terminal().Log().CRITICAL(f"Shutting Down...")
        sys.exit(0)