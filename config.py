from inspect import indentsize
import json
import logging
import os

COG_DIRECTORY_PATH = "cogs" #Name of directory where cogs will be stored.
LOG_DIRECTORY_PATH = "logs" #Name of directory where log files will be stored.
CONFIG_PATH = "config.json" #Name of config file.
EXAMPLE_CONFIG = { # Changing this will only matter when the bot creates a new config. If you're looking for your normal config to change then please go to the file referenced in CONFIG_PATH
    "bot" : {
        "prefixes" : ["!"], #Bot uses this array for prefixes. Add as many as you want, and keep in mind you can include spaces but be careful not to over complicate your prefixes.
        "token" : "", # if you have multiple tokens change this from "token" to ["token","token2"]
        "status" : {
            "type" : "listening" # Valid Options are listening, playing
        },
        "name" : "Bot Name", # Bot name
        "version" : "0.0.0", # Bot version
        "description" : "Bot Description would go here.",
        "developer_guild_id" : "", # Developer guild id for bot. Used for test commands.
        "contributers" : [
            {
                "name":"Contributer Name",
                "discord_id": "Contributer Discord ID", 
                "owner" : True # Set this to true if they're an owner. otherwise set it to false
            },
            {
                "name":"Contributer Name",
                "discord_id": "Contributer Discord ID",
                "owner" : False
            }
            ],
        "apis" : [
            {
                "name" : "Api Name",
                "token" : "Api Token",
                "header" : {"Authorization": ""} 
            }
        ]
    },
    "music" : {
        "max_volume" : 250,
        "vote_skip" : True, #whether vote skip is enabled or not.
        "vote_skip_ratio" : 0.5 #minimum ratio needed for vote skip
    }
}

def load_config(path=CONFIG_PATH):
    """Loads the config from `path`"""
    if os.path.exists(path) and os.path.isfile(path):
        with open(path) as file:
            config = json.load(file)
        return config
    else:
        with open(path, "w") as config:
            json.dump(EXAMPLE_CONFIG, config, indent=4)
            logging.warn(
                f"No config file found. Creating a default config file at {path}."
            )
        if not os.path.exists("cogs"):
            os.mkdir("cogs")
        if not os.path.exists(LOG_DIRECTORY_PATH):
            os.mkdir(LOG_DIRECTORY_PATH)
        return load_config(path=path)