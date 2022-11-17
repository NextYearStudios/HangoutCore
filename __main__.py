"""
    HangoutCore Main File
    › Please do not modify any of the following content unless you know what you're doing. Modifying the following code and not updating the rest of the bot code to match can/will cause issues.
    › If you do decide to modify the following code please understand that HangoutCore's Dev team, Discord.py's Dev Team nor Python's Dev team are obligated to help you.
    › By Modifying the following code you acknowledge and agree to the text above.
    Last Updated: November 15, 2022
    Last Updated by: Lino
    Notes:
        None
"""

import asyncio
import hangoutcore
import sys
# Local modules
from util import terminal

if __name__ == "__main__":
    try:
        asyncio.run(hangoutcore.main())
    except KeyboardInterrupt:
        print("") # Clear line just incase user closes while inputting
        terminal.log.CRITICAL(f"Please refrain from using CTRL+C to shutdown bot.")
        terminal.log.CRITICAL(f"Shutting Down...")
        sys.exit(0)