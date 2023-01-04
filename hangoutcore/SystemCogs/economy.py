import discord
import typing

from datetime import datetime
from discord import app_commands, ui
from discord.ext import commands, tasks
from discord.utils import get

from hangoutcore.bot import HangoutCoreBot
from hangoutcore.util import Config, Database, CommonUI, Local, Terminal

class Economy(commands.Cog):
    """Commands pertaining to guild economy."""

    def __init__(self, bot: HangoutCoreBot) -> None:
        self.bot = bot
        self.config: Config = bot.config
        self.database: Database = bot.database
        self.local: Local = Local()
        self.terminal: Terminal = Terminal()
        self.log: Terminal.Log = self.terminal.Log()
        self.log.setLoggerName("Cog_Economy")
        self.development = False
        self.hidden = False
        self.updateBank.start()

        super().__init__()

    def cog_unload(self):
        self.updateBank.cancel()

    @tasks.loop(minutes=15)
    async def updateBank(self):
        for guild in self.bot.guilds:
            guildData = await self.database.retrieveGuild(guild)
            if guildData is not None:
                _guildData = guildData[2]
                if not _guildData['extras']['guild_economy']['enabled']:
                    continue
                else:
                    _bank_channel_id = int(_guildData['extras']['guild_economy']['channel'])
                    _bank_message_id = int(_guildData['extras']['guild_economy']['message'])
                    _bank_channel = guild.get_channel(_bank_channel_id)
                    if _bank_channel is not None:
                        _bank_message: discord.Message = await _bank_channel.fetch_message(_bank_message_id)
                        if _bank_message is not None:
                            bankView = CommonUI.GuildBankView( _bank_message, self.database, _guildData,"System Response", None)
                            await bankView.update_message()
                            await _bank_message.edit(content=None, view=bankView)

    @app_commands.command(description=f"Retrieves and displays user's balance.")
    async def balance(self, interaction: discord.Interaction):
        guildData = await self.database.retrieveGuild(interaction.guild)
        _guildData = guildData[2]
        userData = await self.database.retrieveUser(interaction.user)
        _userData = userData[2]

        if _guildData['extras']['guild_economy']['enabled']:
            _guildBalance = None
            for entry in _userData['economy']['guild']:
                if entry['id'] != interaction.guild.id:
                    continue
                else:
                    _guildBalance = entry['balance']
            if _guildBalance is not None:
                await interaction.response.send_message(f"Your Balance: {_guildData['extras']['guild_economy']['currency']}{_guildBalance}", ephemeral=True)
            else:
                _guildBalance = _guildData['extras']['guild_economy']['balance_start']
                _userData['economy']['guild'].append({"id":interaction.guild.id, "balance":_guildBalance})
                await self.database.updateUser(interaction.user, _userData)
                await interaction.response.send_message(f"Your Balance: {_guildData['extras']['guild_economy']['currency']}{_guildBalance}", ephemeral=True)

    @app_commands.command(description=f"Sends money to the user specified.")
    async def pay(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Sending Payment", ephemeral=True)

    



async def setup(bot: HangoutCoreBot):
    await bot.add_cog(Economy(bot))
    await Terminal().Log().WARNING(f"Economy has been loaded.")
    
    
async def teardown(bot: HangoutCoreBot):
    await bot.remove_cog(Economy(bot))
    await Terminal().Log().WARNING(f"Economy has been unloaded.")
