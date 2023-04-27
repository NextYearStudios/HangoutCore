"""
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    Bot Module for HangoutCore
        › Please do not modify any of the following content unless you know what you're doing. Modifying the following code and not updating the rest of the bot code to match can/will cause issues.
        › If you do decide to modify the following code please understand that HangoutCore's Dev team, Discord.py's Dev Team nor Python's Dev team are obligated to help you.
        › By Modifying the following code you acknowledge and agree to the text above.
    Module Last Updated: January 6, 2023
    Module Last Updated by: Lino
    License: Refer to LICENSE.md
    Notes:
        None
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import discord

from hangoutcore.util import Audio, Config, Database, Local, Terminal
from aiohttp import ClientSession
from datetime import datetime
from discord.ext import commands
from typing import List, Optional

class HangoutCoreBot(commands.Bot):  # Sub class bot so we can have more customizability
    def __init__(
            self,
            *args,
            activity,
            test_Guild_ID: Optional[int] = None,
            web_client,
            db_pool = None,
            debug_mode: Optional[bool] = False,
            config,
            terminal,
            **kwargs):
        super().__init__(*args, **kwargs)

        # Setup variables that we may need later on

        self.start_time = None  # Add the start_time variable so that we may access it for debugging or information display purposes.
        self.debug_mode = debug_mode

        self.web_client = web_client
        self.db_pool = db_pool
        self.config: Config = config
        self.terminal: Terminal = terminal
        self.log: Terminal.Log = terminal.Log()

        self.audio: Audio = Audio()
        self.database: Database = Database()
        self.local: Local = Local()
        self.activity = activity


        self.BotSynced = False
        # BotSynced = False
        # ViewsAdded = False

    async def is_user_blacklisted(self, user) -> bool:
        _user = None
        if type(user) == int:
            _user = discord.Object(id=user)
        elif type(user) == discord.Member or type(user) == discord.User:
            _user = user
            
        if _user is not None:
            userData = await self.database.retrieveUser(user)
            _userData = None
            if userData is not None:
                _userData = userData[2]
                return bool(_userData['bot']['blacklisted'])
        else:
            return True # Default to true if we can't retrieve user status

    async def is_user_staff(self, guild, user):
        if guild is None or user is None:
            return 0
        else:
            guildData = await self.database.retrieveGuild(interaction.guild)

            if guildData is not None:
                _guildData = guildData[2]
                _trialModerator = _guildData['roles']['guild_trial_moderator']
                _moderator = _guildData['roles']['guild_moderator']
                _administrator = _guildData['roles']['guild_administrator']
                _owner = _guildData['roles']['guild_owner']
                if _owner != 0:
                    # _role = guild.get_role(id=_owner)
                    for role in user.roles:
                        if role.id == _owner:
                            return 4
                        elif role.id == _administrator:
                            return 3
                        elif role.id == _moderator:
                            return 2
                        elif role.id == _trialModerator:
                            return 1
                    else:
                        return 0

    async def syncBot(self):
        if not self.BotSynced:
            if self.debug_mode:
                devGuildID = int(self.config.CONFIG['bot']['developer_guild_id'])
                devGuild = discord.Object(devGuildID)
                if int(devGuildID) != 0:
                    await self.log.DEBUG(f"Syncing to guild ID: {devGuildID}")
                    self.tree.copy_global_to(guild=devGuild)
                    await self.tree.sync() # guild=devGuild
                else:
                    await self.log.ERROR(f"Unable to sync to developer guild. Please provide your Guild ID in your config file.")
            else:
                await self.tree.sync()

    async def setup_hook(self) -> None:

        # here, we are loading extensions prior to sync to ensure we are syncing interactions defined in those extensions.
        self.start_time = '{0:%d%b%Y %Hh:%Mm}'.format(datetime.now())

        
        await self.audio.setConfig(self.config)
        await self.audio.setTerminal(self.terminal)
        await self.database.setConfig(self.config)
        await self.database.setTerminal(self.terminal)
        await self.database.setPool(self.db_pool)
        await self.local.setConfig(self.config)
        await self.local.setTerminal(self.terminal)

        await self.log.INFO(f"Checking for preloaded bot modules...")

        for cog in self.cogs.keys():
            await self.log.INFO(f"Found {cog}")

        await self.log.INFO(f"Looking for bot modules in '/{self.config.COG_DIRECTORY_PATH}'...")
        await self.local.load_extensions(self, self.debug_mode, False)  # Scan cog directory and enable cogs.
        await self.log.INFO(f"Looking for system bot modules")
        await self.local.load_extensions(self, self.debug_mode, True)
        await self.audio.verify_opus()  # Looks for opus and loads it if found.

        await self.syncBot()
        

        await self.log.INFO(f"Logged in as {self.user} (ID: {self.user.id}).")

        guild_ids = await self.database.retrieveTableColumn('guilds', 'id')

    async def on_ready(self):
        # self.add_view(utils.bot.CustomViews.autoroleView())
        await self.wait_until_ready()
        
        await self.terminal.print_hr()
        await self.terminal.print_center(f"Bot Is Ready and Logged in as {self.user} (ID: {self.user.id})")
        await self.terminal.print_hr()

        # await self.log.WARNING("Updating Guild Database")
        
        stored_guild_ids = await self.database.retrieveTableColumn('guilds', 'id')
        stored_user_ids = await self.database.retrieveTableColumn('users', 'id')

        if stored_guild_ids is not None:
            for guild in self.guilds:
                if guild.id not in stored_guild_ids:
                    await self.database.registerGuild(guild)

                for member in guild.members:
                    if not member.bot:
                        if stored_user_ids is not None:
                            if member.id not in stored_user_ids:
                                await self.database.registerUser(member)
                        else:
                            await self.database.registerUser(member)

        else:
            for guild in self.guilds:
                await self.database.registerGuild(guild)
                for member in guild.members:
                    await self.database.registerUser(member)
        
    