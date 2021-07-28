import logging
import shutil
import discord
import colorama
import config
import sys

from colorama import *
from os import system, name

cfg = config.load_config()

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ↓ Terminal ↓
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def color(style: colorama.Style, fore: colorama.Fore, back: colorama.Back, content):
    processedContent = f"{style}{fore}{back}{content}{Style.RESET_ALL}{Fore.RESET}{Back.RESET}"
    return processedContent
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