<<<<<<< HEAD
# HangoutCore V2.0
###### Welcome to HangoutCore's Repository! Provided here is a little more than the basic code required to run a discord bot using [Discord.py](https://discordpy.readthedocs.io/en/master/index.html)! You'll find our bot to be easily configurable and ready for you to add your [cogs](https://discordpy.readthedocs.io/en/stable/ext/commands/cogs.html)!
=======
# HangoutCore Bot Framework
##### HangoutCore Version: [![HangoutCore](https://img.shields.io/pypi/v/hangoutcore?label=Version)](https://pypi.org/project/hangoutcore/) | using [![Discord.py](https://img.shields.io/pypi/v/Discord.py?label=Discord.py)](https://pypi.org/project/discord.py/) | License [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
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
- Add per bot(config) directory specification. (each bot should be alowed to have it's own cog, log directory to avoid mixing bots)
## Features
- Config Support: Quickly swap bot information such as Description, Tokens, Intents, Prefixes, etc.
- Config File Setup Process: HangoutCore streamlines config file creation by walking the user through a short setup process, allowing the user to quickly and efficiently create multiple config files for quick bot swapping.
- Automated config Swapping: By simply running ```py hangoutcore -config ConfigName``` HangoutCore will automatically swap over to the desired config and store the selection for future use.
Once you run the command above you can simply run the bot like normal until you're ready to swap once again.
- Automated Token Swapping: Multiple tokens in your config file? HangoutCore will automatically prompt the user to ensure the right token is chosen every time. Want to skip the prompt? Simply run ```py hangoutcore -token [INTEGER]``` to choose from the list of tokens.
- Detailed Terminal Output: With a simple glance you're able to tell if your bot is running as it should. With colored terminal classes you can very easily tell apart Errors from normal output.

## Installation
###### Please note it is assumed you already have Python, and VirtualEnv installed prior to this installation. If you do not have both installed please do so before continuing.
1. ### *Environment Setup:*
    1. Create and CD into your desired directory via ```cd /path/to/directory```
    2. [Create a Virtual Environment](https://docs.python.org/3/library/venv.html#creating-virtual-environments) via ```python -m venv --upgrade-deps /path/to/venv```
    - [Linux] Activate your Virtual Environment via ```source venv/bin/activate```
    - [Windows] Activate your Virtual Environment via ```.\venv\Scripts\activate```
    4. Install hangoutcore via ```pip install hangoutcore```
1. ### *HangoutCore Bot Setup:*
    1. Start HangoutCore via ```hangoutcore```
    2. The initial prompt will ask you to start the setup process
    <img src="https://i.imgur.com/FhPp3o4.png" width="500">

    1. The setup process will ask you various questions pertaining to the handling of your bot.
    2. Once you've entered the necessary info the bot will ask you to verify the information one last time before proceeding
    <img src="https://i.imgur.com/ldQBEwB.png" width="500">

    3. After confirming, the bot will then create the necessary directories and add your provided info to the config file that you named.
    <img src="https://i.imgur.com/sDkQA0R.png" width="500">
    
    4. The bot will now attempt to login with the provided token
    <img src="https://i.imgur.com/pHO95TW.png" width="500">
1. ### *Starting HangoutCore*
    - Starting HangoutCore with one token specified in your config will not require any other input before starting.
    - Starting HangoutCore normally with more than one token specified will cause HangoutCore to prompt you in the terminal to specify which token you'd like to use.
    <img src="https://i.imgur.com/SOYHY1T.png" width="500">
    
    - Starting HangoutCore Via ```hangoutcore -t int``` or ```hangoutcore --token int``` 
    will use the number specifed to choose which token to start with ultimately skipping the prompt for token choice.
    
        If setting up HangoutCore to be run automatically or with no human interaction with the terminal please make sure to:
        1. Specify which token to use if multiple tokens are present in your config
        2. Start HangoutCore in silent mode using '-S True' or '-Silent True'
        
## Contributers
##### A special thank you to the following for contributing to this project.
- [Alec J](https://github.com/alec-jensen)
- [Lino H](https://github.com/Its-Lino)
>>>>>>> d6d60c6c1efc3623cd975c3e8879719339f8eee6
