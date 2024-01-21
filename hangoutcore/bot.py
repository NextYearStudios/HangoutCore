"""
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    Bot Module for HangoutCore
        › Please do not modify any of the following content unless you know what you're doing. Modifying the following code and not updating the rest of the bot code to match can/will cause issues.
        › If you do decide to modify the following code please understand that HangoutCore's Dev team, Discord.py's Dev Team nor Python's Dev team are obligated to help you.
        › By Modifying the following code you acknowledge and agree to the text above.
    Module Last Updated: Jan 21, 2024
    Module Last Updated by: Lino
    License: Refer to LICENSE.md
    Notes:
        None
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import discord
import wavelink

# from hangoutcore.util import Audio, Config, Database, Local, Terminal
import hangoutcore
from hangoutcore.utils import *

from aiohttp import ClientSession
from datetime import datetime
from discord.ext import commands
from typing import List, Optional

class HangoutCoreBot(commands.Bot):  # Sub class bot so we can have more customizability
    def __init__(
            self,
            *args,
            activity,
            web_client,
            db_pool,
            init_time,
            DeveloperGuild_ID,
            **kwargs):
        super().__init__(*args, **kwargs)

        # Setup variables that we may need later on

        self.activity = activity
        self.web_client = web_client
        self.db_pool = db_pool
        
        self.init_time = init_time  # Add the start_time variable so that we may access it for debugging or information display purposes.
        self.DeveloperGuild_ID = DeveloperGuild_ID


        self.BotSynced = False
        # BotSynced = False
        # ViewsAdded = False

    def botErrorEmbed(self, error: str|int, *args, **kwargs) -> discord.Embed:
        terminal.log.DEBUG(f"Args {args}\n KwArgs {kwargs}")
        
        def createEmbed(err: str, errNum: int):
            _embed = discord.Embed(
                # title = f"Error:",
                color = discord.Color.red(), #discord.Color.from_rgb(47,49,54)
                timestamp = datetime.now()
            )
            _embed.set_footer(text = f"System Response")
            _embed.add_field(
                name = "Error Number:",
                value = f"`{errNum}`",
                inline = True
            )
            _embed.add_field(
                name = "Error:",
                value = f"{err.format(*args,**kwargs)}",
                inline = True)
                
            return _embed
        
        _messages: dict = hangoutcore.CONFIG_BOT["bot"]["messages"]
        if type(error) == int:
            for _m in _messages.values():
                if _m[0] == error:
                    _embed = createEmbed(_m[1], _m[0])
                    return _embed
                
        if type(error) == str:
            for _m in _messages.keys():
                if _m == error.lower():
                    _error = _messages[f'{error}']
                    _embed = createEmbed(_error[1], _error[0])
                    return _embed
            
        # if we're still here then that means the error was not found
        terminal.log.ERROR(f"{self.botErrorEmbed.__name__} Failed. Invalid error provided: {error}")
        _error = _messages['error_bot_fail']
        _embed = createEmbed(_error[1], _error[0])
        return _embed

    # async def is_user_staff(self, guild, user):
    #     if guild is None or user is None:
    #         return 0
    #     else:
    #         guildData = await self.database.retrieveGuild(interaction.guild)

    #         if guildData is not None:
    #             _guildData = guildData[2]
    #             _trialModerator = _guildData['roles']['guild_trial_moderator']
    #             _moderator = _guildData['roles']['guild_moderator']
    #             _administrator = _guildData['roles']['guild_administrator']
    #             _owner = _guildData['roles']['guild_owner']
    #             if _owner != 0:
    #                 # _role = guild.get_role(id=_owner)
    #                 for role in user.roles:
    #                     if role.id == _owner:
    #                         return 4
    #                     elif role.id == _administrator:
    #                         return 3
    #                     elif role.id == _moderator:
    #                         return 2
    #                     elif role.id == _trialModerator:
    #                         return 1
    #                 else:
    #                     return 0

    async def setup_hook(self) -> None:

        terminal.log.INFO(f"Checking for preloaded bot modules...")
        if len(self.cogs.keys()) > 0:
            for cog in self.cogs.keys():
                terminal.log.INFO(f"Found module {cog}")
        else:
            terminal.log.INFO(f"No preloaded modules detected.")
            
        await local.load_extensions(self, hangoutcore.DIRECTORY_COGS, hangoutcore.SYSTEM_COGS)  # Scan cog directory and enable cogs.

        terminal.print_hr()
        terminal.print_center(f"Bot Is Ready and Logged in as {self.user.name} (ID: {self.user.id})")
        terminal.print_hr(title="Post-Load Output")
        
        # terminal.log.DEBUG(f"{hangoutcore.DEBUG}")

    #     await self.log.INFO(f"Looking for system bot modules")
    #     await self.local.load_extensions(self, self.debug_mode, True)
    #     await self.audio.verify_opus()  # Looks for opus and loads it if found.
        
    #     await self.log.INFO(f"Logged in as {self.user} (ID: {self.user.id}).")

        # guild_ids = await database.retrieveTableColumn('guilds', 'id')

    #     # Music (Wavelink)

    #     node: wavelink.Node = wavelink.Node(uri='', password='')
    #     await wavelink.NodePool.connect(client=self, nodes=[node])

    #     # import os
    #     # for file in os.path.join(os.path.dirname(__file__), 'SystemCogs'):
    #     #     print(file)
    async def on_ready(self):
    #     # self.add_view(utils.bot.CustomViews.autoroleView())
        await self.wait_until_ready()
        
        if hangoutcore.DB_POOL is not None:
            terminal.log.DEBUG("Fetching guild database")
            _stored_guild_ids = await database.retrieveTableColumn('guilds', 'id')
            terminal.log.DEBUG("Fetching user database.")
            _stored_user_ids = await database.retrieveTableColumn('users', 'id')

            if _stored_guild_ids is not None:
                terminal.log.DEBUG("Checking for guilds with no entry in database.")
                for guild in self.guilds:
                    if guild.id not in _stored_guild_ids:
                        terminal.log.DEBUG("Adding new guild to database.")
                        await database.registerGuild(guild)
                    
                    terminal.log.DEBUG(f"Checking for users in {guild} with no entry in database.")
                    for member in guild.members:
                        if not member.bot:
                            if _stored_user_ids is not None:
                                if member.id not in _stored_user_ids:
                                    terminal.log.DEBUG("Adding new user to database.")
                                    await database.registerUser(member)
                            else:
                                await database.registerUser(member)
            else:
                terminal.log.DEBUG("Could not find guild database. Creating new one.")
                if _stored_user_ids is None:
                    terminal.log.DEBUG("Could not find user database. Creating new one.")
                for guild in self.guilds:
                    await database.registerGuild(guild)
                    for member in guild.members:
                        await database.registerUser(member)
                    
    # async def on_error(self, event, *args, **kwargs):
    #     terminal.log.WARNING(f"{event}")
    
    async def close(self):
        terminal.log.WARNING(f"Bot is shutting down.")
        if hangoutcore.DB_POOL is None:
            return
        
        if not hangoutcore.DB_POOL.closed:
            terminal.log.WARNING(f"Database Connection Still Open.")
            await database.closePool()