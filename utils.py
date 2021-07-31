""" Utility Module designed to be the main library for HangoutCore """

import logging
import shutil
import discord
import os
import config
import sys
import traceback

from colorama import *
from os import system, name

cfg = config.load_config()

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ↓ Cog Loading ↓ : WIP
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def GetCogs():
    valid_files = []
    disabled_files = []
    invalid_files = []
    for file in os.listdir(config.COG_DIRECTORY_PATH):
        if file.endswith('.py'):
            valid_files.append(file)
        elif file.endswith('.disabled'):
            disabled_files.append(file)
        else:
            if file == "__pycache__" or "__init__":
                pass
            else:
                invalid_files.append(file)
    package = {
        "valid_files": valid_files,
        "invalid_files": invalid_files,
        "disabled_files": disabled_files
    }
    return package
    

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ↓ Error Processing ↓ : WIP
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class ErrorProcessing():

    def CogLoadError(file, error, debug_mode):
        """ Error Processing tailored to display the specific error when loading a cog, 
            designed to minimise clutter and lines not relevant."""
        ErrorTraceback = traceback.format_exception(type(error), error, error.__traceback__)
        if debug_mode:
            log("ERROR", "\n" + "".join(ErrorTraceback))
        else:
            FilteredTraceback = None
            for string in ErrorTraceback:
                str(string).replace("\n", "")
            log("ERROR", f"""  └ Failed to load {file}.
            {Back.RED}{ErrorTraceback[0]}{Back.RESET}
            {Back.RED}{ErrorTraceback[5]}{Back.RESET}
            {Back.RED}{ErrorTraceback[6]}{Back.RESET}""")
            #log("ERROR", f"{Back.RED}    {ErrorTraceback[0]}{Back.RESET}")
            #log("ERROR", f"{Back.RED}    {ErrorTraceback[5]}{Back.RESET}")
            #log("ERROR", f"{Back.RED}    {ErrorTraceback[6]}{Back.RESET}")
            
            #for i in range(len(ErrorTraceback)):
            #    log("ERROR", f"{Fore.RED}    {ErrorTraceback[i]}{Fore.RESET}")

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ↓ Color ↓ : WIP
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

#def color(style: colorama.Style, fore: colorama.Fore, back: colorama.Back, content):
#    processedContent = f"{style}{fore}{back}{content}{Style.RESET_ALL}{Fore.RESET}{Back.RESET}"
#    return processedContent

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ↓ Logging ↓
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def log(level:str, log):                                                                                                        # More Logging functionality
    if level == "DEBUG":                                                                                                        #
        logging.debug(log)                                                                                                      #
        print(f"[{Fore.BLUE}DEBUG{Fore.RESET}] {log}")                                                                          #

    if level == "INFO":                                                                                                         #
        logging.info(log)                                                                                                       #
        print(f"[{Fore.GREEN}INFO{Fore.RESET}] {log}")                                                                          #

    if level == "WARNING":                                                                                                      #
        logging.warning(log)                                                                                                    #
        print(f"[{Fore.YELLOW}WARNING{Fore.RESET}] {log}")                                                                      #
        
    if level == "ERROR":                                                                                                        #
        logging.error(log)                                                                                                      #
        print(f"[{Fore.RED}ERROR{Fore.RESET}] {log}")                                                                           #

    if level == "CRITICAL":                                                                                                     #
        logging.critical(log)                                                                                                   #
        print(f"[{Style.BRIGHT}{Back.RED}CRITICAL{Style.RESET_ALL}{Back.RESET}] {log}")                                         #

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ↓ Terminal ↓
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class terminal:
        
    def print_center(s):
        print(s.center(shutil.get_terminal_size().columns))

    def print_hr():
        print('━'.center(shutil.get_terminal_size().columns, '━'))

    def clear():
        if name =='nt':
            _ = system('cls')    
        else: 
            _ = system('clear')

    def initiate(start_time, debug:bool=False):
        terminal.clear()
        if debug:
            print(Style.BRIGHT + Back.RED,end="\r")
        else:
            print(Style.NORMAL + Fore.BLACK + Back.WHITE,end="\r")
        terminal.print_center(str(cfg["bot"]["name"]))
        terminal.print_center(str(cfg["bot"]["version"]))
        terminal.print_center(str(start_time))
        if debug:
            terminal.print_center(f'// Debug Mode Enabled \\\ ')
            terminal.print_center('SYS Version ' + str(sys.version))
            terminal.print_center('API Version ' + str(sys.api_version))
            terminal.print_center('Discord Version ' + str(discord.__version__))
        print(Style.RESET_ALL + Back.RESET,end="\r")
        terminal.print_hr()

    def refresh(start_time, debug:bool=False):
        terminal.clear()
        if debug:
            print(Style.BRIGHT + Back.RED,end="\r")
        else:
            print(Style.NORMAL + Fore.BLACK + Back.WHITE,end="\r")
        terminal.print_center(str(cfg["bot"]["name"]))
        terminal.print_center(str(cfg["bot"]["version"]))
        terminal.print_center(str(start_time))
        if debug:
            terminal.print_center(f'// Debug Mode Enabled \\\ ')
            terminal.print_center('SYS Version ' + str(sys.version))
            terminal.print_center('API Version ' + str(sys.api_version))
            terminal.print_center('Discord Version ' + str(discord.__version__))
        print(Style.RESET_ALL + Back.RESET,end="\r")
        terminal.print_hr()

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ↓ FFMPEG and Youtube_DL Stuff ↓
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class GuildState:
    """Helper class managing per-guild state."""

    def __init__(self):
        self.volume = 1.0 # volume is config max_volume / 100
        self.playlist = []
        self.skip_votes = set()
        self.now_playing = None
