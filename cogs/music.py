import discord
import typing

from datetime import datetime
from discord import app_commands, ui
from discord.ext import commands

from hangoutcore.bot import HangoutCoreBot
from hangoutcore.util import Config, CommonUI, Local, Terminal

class Music(commands.Cog):
    """A Variety of commands for playing music."""

    def __init__(self, bot: HangoutCoreBot) -> None:
        self.bot = bot
        self.config = bot.config
        self.terminal = Terminal()
        self.log = self.terminal.Log()
        self.log.setLoggerName("Cog_Music")
        self.development = False
        self.hidden = False

        self.local = Local()
        super().__init__()

    @app_commands.command(description=f"Command used to make bot join a voice channel.")
    async def join(self, interaction: discord.Interaction):
        await interaction.response.send_message("Joining.", ephemeral=True)

    @app_commands.command(description=f"Command used to make bot leave a voice channel.")
    async def leave(self, interaction: discord.Interaction):
        await interaction.response.send_message("Leaving.", ephemeral=True)

    @app_commands.command(description=f"Command used to play music.")
    async def play(self, interaction: discord.Interaction):
        await interaction.response.send_message("Playing.", ephemeral=True)


async def setup(bot: HangoutCoreBot):
    await bot.add_cog(Music(bot))
    await Music(bot).terminal.Log().WARNING(f"Music has been loaded.")
    
    
async def teardown(bot: HangoutCoreBot):
    await bot.remove_cog(Music(bot))
    await Music(bot).terminal.Log().WARNING(f"Music has been unloaded.")