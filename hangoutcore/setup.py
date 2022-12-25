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
import aiofiles
import os
import sys

from datetime import datetime
from hangoutcore import util
from questionnaire import Questionnaire

def AppConfigExists() -> dict[bool, list]:
    """
    Scan current directory for 'hangoutcore.properties'. We will use this to store necessary information such as config locations.
    """
    util.terminal.log.INFO(f"Scanning for 'hangoutcore.properties'.") # Notify the user that we will be scanning the directory. This is to make sure they're up to date with any action we perform on their system.
    path = os.getcwd()
    pFiles = []
    dict = {
        "exists": False,
        "files": []
    }
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.properties'):
                pFiles.append(file)
    if len(pFiles) > 0:
        dict["exists"] = True
        dict["files"] = pFiles
        return dict
    else:
        dict["exists"] = False
        return dict

def setup():
    """
    Run through the process of setting up the necessary files for HangoutCore to operate.
    """
    init_time = '{0:%d%b%Y %Hh:%Mm}'.format(datetime.now()) # This time is used for bot reference
    util.terminal.initiate(init_time, debug=False)
    ACE = AppConfigExists()
    if ACE["exists"]:
        pass
    else:
        util.terminal.log.INFO(f"Could not find")


def beginsetup():
    try:
        setup()
    except KeyboardInterrupt:
        print("") # Clear line just incase user closes while inputting
        util.terminal.log.CRITICAL(f"Please refrain from using CTRL+C to shutdown bot.")
        util.terminal.log.CRITICAL(f"Shutting Down...")
    else:
        print("") # Clear line just incase user closes while inputting
        util.terminal.log.CRITICAL(f"Shutting Down...")

if __name__ == "__main__":
    beginsetup()