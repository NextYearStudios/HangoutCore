# HangoutCore Bot Framework
##### HangoutCore Version: 2.87 | using [![Discord.py](https://img.shields.io/pypi/v/Discord.py?label=Discord.py)](https://pypi.org/project/discord.py/) | License [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
***
##### *Join the discord below for quicker support.*
###### Assign yourself the Bot Developer Role in the #pick-your-roles channel in order to access the #bot-support channel.
[![Discord](https://img.shields.io/discord/514091020535857155?color=5865F2&label=Discord&logo=Discord&logoColor=fff)](https://discord.gg/xpwQvdeCN2)
## TODO
- use slash commands
- Add support for various database types in util.database.
- Add support for specifying which config to load from like our current implementation for tokens.
- Further Optimize base script while prioritizing eazy readability for new developers.
- Create Example Cog for new developers to be able to build off of.
- Create webhook example.
- Add Guild registration function in util.database. to begin supporting database saved data.
- Add Ticket Cog for new devs to be able to build off of.
- Create static page to display more detailed information on HangoutCore Project Status
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
1. ### *Starting HangoutCore*
    - Starting HangoutCore with one token specified in your config will not require any other input before starting.
    - Starting HangoutCore normally with more than one token specified will cause HangoutCore to prompt you in the terminal to specify which token you'd like to use.
    - Starting HangoutCore Via ```python hangoutcore.py -t 1``` or ```python hangoutcore.py -token 1``` 
    will use the number specifed to choose which token to start with ultimately skipping the prompt for token choice.
    
        If setting up HangoutCore to be run automatically or with no human interaction with the terminal please make sure to:
        1. Specify which token to use if multiple tokens are present in your config
        2. Start HangoutCore in silent mode using '-S True' or '-Silent True'
1. ### *Adjusting The HangoutCore Bot Config:*
    ```json 
        {
        "bot": {
            "prefixes": [
                "!"
            ],
            "token": [
                "Token1",
                "Token2"
            ],
            "intents" : {
                "members" : True,
                "message_content" : True,
                "typing" : True,
                "presences" : True,
                "guilds" : True
            },
            "status": {
                "type": "listening",
                "name": "!help",
                "url": ""
            },
            "name": "HangoutCore",
            "version": "0.0.0",
            "description": "Bot Description",
            "developer_guild_id": 0,
            "contributers": [
                {
                    "name": "Contributer Name",
                    "discord_id": 0,
                    "owner": true
                },
                {
                    "name": "Contributer Name",
                    "discord_id": 0,
                    "owner": false
                }
            ],
            "apis": [
                {
                    "name": "Api Name",
                    "token": "Api Token",
                    "header": {
                        "Authorization": ""
                    }
                }
            ]
        },
        "database" : {
            "type": "mysql",
            "host": "localhost",
            "port": 3306,
            "name" : "database",
            "user" : "user",
            "password" : "pass"
        },
        "music": {
            "max_volume": 250,
            "vote_skip": true,
            "vote_skip_ratio": 0.5
        },
        "_info": {
            "version": 5.6,
            "update_reason": "Initial Creation"
        }
    }
    ```
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
    3. ##### Intents
        Set your bot intents in the config, allowing for quick and easy swap between multiple bots with different intents.
        ```json 
        "intents" : {
            "members" : True,
            "message_content" : True,
            "typing" : True,
            "presences" : True,
            "guilds" : True
        }
        ```
    4. ##### Status
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
    5. ##### Name
        This variable is used to display the bot name on the terminal, and also serves as a unified access point for displaying the bot name in commands such as the help command or for displaying it on embeds.
    6. ##### Version
        This variable is used to display the bot version on the terminal, and also serves as a unified access point for displaying the bot version in commands where it might be useful such as a support command for staff.
    7. ##### Description
        This variable is used for displaying the bot description in various commands such as the help command or any support commands where it might be needed.
    8. ##### Developer Guild ID
        This variable is used for testing slash commands, or local commands that are not ready for public use in your dev/private guild.
    9. ##### Contributers
        This variable is used for verifying bot staff members to avoid false claims potentially causing unnecessary problems.
        Name: Contributer name that should be displayed, such as username or first name
        Discord ID: This is used to compare against any discord member falsely claiming to be a staff member
        Owner: Specify wether the contributer is essentially an admin through this variable, Users with this set to true will be able to access dangerous commands such as stop,restart, These users will also override guild permissions and also manipulate guild data through database commands.
        ```json 
        "contributers": [
            {
                "name": "John Doe",
                "discord_id": 1234567890,
                "owner": true
            },
            {
                "name": "Jane Doe",
                "discord_id": 1234567890,
                "owner": false
            },
        ]
        ```
    10. ##### Apis
        This variable serves as an access point for commands to locate API info. 
        ```json 
        "apis": [
            {
                "name": "API Name",
                "token": API Token,
                "header": {
                    "Authorization": ""
                }
            },
            {
                "name": "API Name",
                "token": API Token,
                "header": {
                    "Authorization": ""
                }
            },
        ]
        ```
    11. ##### Database
        This serves as an access point for commands and scripts to easily access database info. utils.py primarily uses this variable for providing ease of access to database content such as guild specific info, permissions.
        ```json 
        "database" : {
            "type": "mysql",
            "host": "localhost",
            "port": 3306,
            "name" : "database",
            "user" : "user",
            "password" : "pass"
        }
        ]
        ```
    12. ##### Music
        Max Volume: Divided by 100. Used by audio commands when playing music.
        Vote Skip: Specifies wether vote skip is enabled for music commands.
        Vote Skip Ratio: The ratio required for vote skip to pass. 
        *Being moved out of config in favor of database stored data*
        ```json 
        "music": [
            {
                "max_volume": "250",
                "vote_skip": true,
                "vote_skip_ratio": 0.5
            }
        ]
        ```
    13. ##### Info
        Version: Config Version, used to identify config variations.
        Update Reason: This is essentially a comment variable used by the bot to describe when/why your config might've been updated. such as "update to contributer list" or "update to bot name"
        ```json 
        "_info": [
            {
                "version": 5.6,
                "update_reason": "Reason For Config Data Manipulation"
            }
        ]
        ```
    
## Contributers
##### A special thank you to the following for contributing to this project.
- [Alec J](https://github.com/alec-jensen)
- [Lino H](https://github.com/Its-Lino)
