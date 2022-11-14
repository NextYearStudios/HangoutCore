# HangoutCore Bot Framework
##### Version: 2.85 | using [![Discord.py](https://img.shields.io/pypi/v/Discord.py?label=Discord.py)](https://pypi.org/project/discord.py/) | License [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
***
##### *Join the discord below for quicker support.*
[![Discord](https://img.shields.io/discord/514091020535857155?color=5865F2&label=Discord&logo=Discord&logoColor=fff)](https://discord.gg/xpwQvdeCN2)
## Installation
###### It is assumed you already have Python, and VirtualEnv installed prior to this installation. If you do not have both installed please do so before continuing.
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
    3. [Linux] Activate your Virtual Environment via ```source venv/bin/activate```
    4. [Windows] Activate your Virtual Environment via ```.\venv\Scripts\activate```
    5. Install the required modules via ```pip install -r requirements.txt```
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
