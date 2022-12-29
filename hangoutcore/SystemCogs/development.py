import discord
import typing
import math

from datetime import datetime
from discord import app_commands, ui
from discord.ext import commands

from hangoutcore.bot import HangoutCoreBot
from hangoutcore.util import Config, CommonUI, Database, Local, Terminal

class Development(commands.Cog):
    """Commands meant to be used by bot staff. Syncs to the guild provided in the config."""

    def __init__(self, bot: HangoutCoreBot) -> None:
        self.bot = bot
        self.loggerName = "Cog_Development"
        self.config: Config = bot.config
        self.database: Database =  bot.database
        self.terminal: Terminal = Terminal()
        self.log = self.terminal.Log()
        self.log.setLoggerName("Cog_Development")
        self.development = True
        self.hidden = True

        self.local = Local()
        super().__init__()

    def is_owner(interaction: discord.Interaction):
        if interaction.user.id == 272230336656834560:
            return True
        else:
            return False

    developmentGroup = app_commands.Group(name="development", description="Development command group.")
    
    @developmentGroup.command()
    async def ping(self, interaction: discord.Interaction):
        """Test command."""
        await interaction.response.send_message("Pong", ephemeral=True)
        await self.log.INFO(f"Recieved Ping, Sending Pong")

    extensionsGroup = app_commands.Group(parent=developmentGroup, name="extensions", description="Extension related commands.")

    @extensionsGroup.command(name="list")
    @app_commands.check(is_owner)
    async def extensionList(self, interaction: discord.Interaction):
        """Retrieves and displays a list of every extension currently loaded."""
        await interaction.response.defer(ephemeral=True, thinking=True)
        extensionEmbed = discord.Embed(title = "Loaded Extensions", color = discord.Color.from_rgb(47, 49, 54), timestamp=datetime.now())
        extensionEmbed.set_footer(text="Bot Development")
        extensionEmbed.description = ""
        botCogs = list(self.bot.cogs)
        botExtensions = list(self.bot.extensions)
        for cog in botCogs:
            extensionEmbed.description = extensionEmbed.description + f"· {cog.capitalize()}\n"
        await interaction.followup.send(embed=extensionEmbed,ephemeral=True)

    @extensionsGroup.command(name="reload")
    async def extensionReload(self, interaction: discord.Interaction, extension: str):
        """Reloads the provided extension if valid."""
        await interaction.response.defer(thinking=True,ephemeral=True)
        extensionEmbed = discord.Embed(title = "Loaded Extensions", color = discord.Color.from_rgb(47, 49, 54), timestamp=datetime.now())
        extensionEmbed.set_footer(text="Bot Development")
        
        if extension in list(self.bot.extensions):
            #extensionObject = self.bot.cogs.get(extension)
            extensionSplit = extension.split(".")
            extensionEmbed.description = f"{extensionSplit[len(extensionSplit) - 1].capitalize()}"
            try:
                await self.bot.reload_extension(extension)
                await self.bot.syncBot()
            except Exception as e:
                extensionEmbed.title = "Failed to Load The Following Extension:"
                extensionEmbed.description = f"{extensionEmbed.description} \n\n{e}"
                await interaction.followup.send(embed=extensionEmbed,ephemeral=True)
            finally:
                extensionEmbed.title = "Successfully Reloaded The Following Extension:"
                await interaction.followup.send(embed=extensionEmbed,ephemeral=True)

    @extensionReload.autocomplete("extension")
    async def extensionReload_autoComplete(self, interaction: discord.Interaction, current: str) -> typing.List[app_commands.Choice[str]]:
        data = []
        for extension in list(self.bot.extensions):
            if current.lower() in extension.lower():
                extensionSplit = extension.split(".")
                data.append(app_commands.Choice(name=extensionSplit[len(extensionSplit) - 1], value=extension))
        return data

    @extensionsGroup.command(name="load")
    async def extensionLoad(self, interaction: discord.Interaction, extension:str):
        """Loads the provided extension if valid."""
        await interaction.response.defer(thinking=True,ephemeral=True)
        extensionEmbed = discord.Embed(color = discord.Color.from_rgb(47, 49, 54), timestamp=datetime.now())
        extensionEmbed.set_footer(text="Bot Development")

        botCogs = self.bot.cogs

        for cog in list(botCogs):
            if cog.lower() == extension.lower():
                extensionEmbed.title = f"Failed To Load: {extension.capitalize()}"
                extensionEmbed.color = discord.Color.red()
                extensionEmbed.description = self.config.CONFIG['bot']['messages']['error_dev_runningextensionname']
                await interaction.followup.send(embed=extensionEmbed, ephemeral=True)
                return
        
        cogs = await self.bot.local.GetCogs()

        for cog in cogs['valid_files']:
            if extension.lower() == cog[:-3].lower():
                try:
                    await self.bot.load_extension(f"{self.config.COG_DIRECTORY_PATH}.{cog[:-3]}")
                except Exception as e:
                    extensionEmbed.title = f"Failed To Load: {extension.capitalize()}"
                    extensionEmbed.color = discord.Color.red()
                    extensionEmbed.description = f"Exception: {e}"
                else:
                    extensionEmbed.title = f"Successfully Loaded: {extension.capitalize()}"
                    extensionEmbed.description = ""
                    await interaction.followup.send(embed=extensionEmbed, ephemeral=True)
                    return
        
        extensionEmbed.title = f"Failed To Load: {extension.capitalize()}"
        extensionEmbed.color = discord.Color.red()
        extensionEmbed.description = self.config.CONFIG['bot']['messages']['error_dev_invalidextensionname']
        await interaction.followup.send(embed=extensionEmbed, ephemeral=True)

    @extensionsGroup.command(name="unload")
    async def extensionUnload(self, interaction: discord.Interaction, extension:str):
        """Unloads the provided extension if valid."""
        await interaction.response.defer(thinking=True,ephemeral=True)
        extensionEmbed = discord.Embed(color = discord.Color.from_rgb(47, 49, 54), timestamp=datetime.now())
        extensionEmbed.set_footer(text="Bot Development")

        botCogs = self.bot.cogs
        if extension in list(self.bot.extensions):
            extensionSplit = extension.split(".")
            extensionEmbed.description = f"{extensionSplit[len(extensionSplit) - 1].capitalize()}"
            try:
                await self.bot.unload_extension(extension)
            except Exception as e:
                extensionEmbed.title = "Failed to Load The Following Extension:"
                extensionEmbed.description = f"{extensionEmbed.description} \n\nException: {e}"
                await interaction.followup.send(embed=extensionEmbed,ephemeral=True)
            finally:
                extensionEmbed.title = "Successfully Loaded The Following Extension:"
                await interaction.followup.send(embed=extensionEmbed,ephemeral=True)

    @extensionUnload.autocomplete("extension")
    async def extensionUnload_autoComplete(self, interaction: discord.Interaction, current: str) -> typing.List[app_commands.Choice[str]]:
        data = []
        for extension in list(self.bot.extensions):
            if current.lower() in extension.lower():
                extensionSplit = extension.split(".")
                data.append(app_commands.Choice(name=extensionSplit[len(extensionSplit) - 1], value=extension))
        return data

async def setup(bot: HangoutCoreBot):
    devGuildID = int(bot.config.CONFIG['bot']['developer_guild_id'])
    devGuild = discord.Object(devGuildID)
    await bot.add_cog(Development(bot), guild=devGuild)
    await Development(bot).terminal.Log().WARNING(f"Development has been loaded.")
    
    
async def teardown(bot: HangoutCoreBot):
    await bot.remove_cog(Development(bot))
    await Development(bot).terminal.Log().WARNING(f"Development has been unloaded.")