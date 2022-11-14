# HangoutCore Bot Framework
##### Version: 2.85 | using [![Discord.py](https://img.shields.io/pypi/v/Discord.py?label=Discord.py)](https://pypi.org/project/discord.py/) | License [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
***
##### *Join the discord below for quicker support.*
[![Discord](https://img.shields.io/discord/514091020535857155?color=5865F2&label=Discord&logo=Discord&logoColor=fff)](https://discord.gg/xpwQvdeCN2)
## Installation
###### Please note it is assumed you already have Python, and VirtualEnv installed prior to this installation. If you do not have both installed please do so before continuing.
1. ### *Clone Repository Via Terminal:*
    1. CD into your desired directory via ```cd /path/to/directory```
    1. Clone this repository via ```git clone git@github.com:NextYearStudios/HangoutCore.git```
**This will create a directory named HangoutCore with the repository inside it**
1. ### *Clone Repository Via Github Website:*
    1. Click the 'Code' button towards the top right of the website.
    <img src="https://i.imgur.com/JaA9ld0.png" width="500">
    
    2. Click Download ZIP
    3. Drag the downloaded file named 'HangoutCore-main.zip' to the directory where you'd like your bot to run.
    4. Extract the compressed ZIP file to your directory.
1. ### *Environment Setup:*
    1. CD into your desired directory via ```cd /path/to/directory```
    2. [Create a Virtual Environment](https://docs.python.org/3/library/venv.html#creating-virtual-environments) via ```python -m venv --upgrade-deps /path/to/venv```
    - [Linux] Activate your Virtual Environment via ```source venv/bin/activate```
    - [Windows] Activate your Virtual Environment via ```.\venv\Scripts\activate```
    4. Install the required modules via ```pip install -r requirements.txt```
1. ### *HangoutCore Bot Setup:*
    1. Start HangoutCore via ```python hangoutcore.py```
    2. The initial prompt will ask you to start the setup process
    <img src="https://i.imgur.com/8pbRoX8.png" width="500">

    1. The setup process will ask you to enter the following info:
    Bot Name
    Bot Description
    Bot Prefix (Default: !)
    Bot Version (Default: 0.0.0)
    Bot Token (will ask again to verify)
    Your desired config name (Default: config.json)
    Where you'd like to store your config files (Default: /configs)
    Where you'd like to store your log files (Default: /logs)
    Where you'd like to store your cogs (Default: /cogs)
    2. Once you've entered the necessary info the bot will ask you to verify the information one last time before proceeding
    <img src="https://i.imgur.com/Jdl2XKs.png" width="500">

    3. After confirming, the bot will then create the necessary directories and add your provided info to the config file that you named.
    <img src="https://i.imgur.com/sDkQA0R.png" width="500">
    
    4. The bot will now attempt to login with the provided token
1. ### *Adjusting The HangoutCore Bot Config:*
    <img src="https://i.imgur.com/qkkS2Oj.png" width="500">

    1. ##### Prefixes
        Allows for single/multiple prefixes to be used with the bot.
        *Being phased out as discord moves to slash commands*
        ```json 
        "prefixes": [
            "prefix1",
            "prefix2",
            "prefix3"
        ]
        ```
    2. ##### Token
        Allows for single/multiple tokens to be used with the bot.
        Starting the bot with multiple tokens in the config will cause a prompt to allow the user to choose which bot to start allowing for quick swap between multiple bots.
        ```json 
        "token": [
            "token1",
            "token2",
            "token3"
        ]
        ```
    3. ##### Status
        Set what [activity](https://discordpy.readthedocs.io/en/stable/api.html?highlight=activity#discord.Activity) the bot will display once logged on.
        [Activity Types](https://discordpy.readthedocs.io/en/stable/api.html?highlight=activity#discord.ActivityType)
        Activity Name: String displayed on bot profile.
        Activity URL: URL Displayed to be used with Streaming Activity Type
        ```json 
        "status": [
            "type": "listening",
            "name": "!help",
            "url": ""
        ]
        ```
    4. ##### Name
        This variable is used to display the bot name on the terminal, and also serves as a unified access point for displaying the bot name in commands such as the help command or for displaying it on embeds.
    5. ##### Version
        This variable is used to display the bot version on the terminal, and also serves as a unified access point for displaying the bot version in commands where it might be useful such as a support command for staff.
    6. ##### Description
        This variable is used for displaying the bot description in various commands such as the help command or any support commands where it might be needed.
    7. ##### Developer Guild ID
        This variable is used for testing slash commands, or local commands that are not ready for public use in your dev/private guild.
    8. ##### Contributers
        ```json 
        "status": [
            "type": "listening",
            "name": "!help",
            "url": ""
        ]
        ```
    9. ##### Apis
    10. ##### Database
    11. ##### Music
    12. ##### Info
    
    
    
