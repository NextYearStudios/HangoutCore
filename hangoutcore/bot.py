import discord
import os
import shutil
import traceback
from aiohttp import ClientSession
from datetime import datetime
from discord import app_commands
from discord.ext import commands
from pathlib import Path
from typing import Optional

import hangoutcore
from hangoutcore.utils import terminal, loggerHangoutCore

class HangoutCoreBot(commands.Bot):
    """Customized bot class for HangoutCore."""

    def __init__(
        self,
        *args,
        activity: discord.Activity,
        web_client: ClientSession,
        db_pool,
        init_time,
        DeveloperGuild_ID,
        **kwargs
    ):
        super().__init__(*args, **kwargs)

        self.activity = activity
        self.web_client = web_client
        self.db_pool = db_pool
        self.init_time = init_time
        self.DeveloperGuild_ID = DeveloperGuild_ID

        self.terminal = terminal(f"{hangoutcore.terminal.module}.Bot", loggerHangoutCore)
        self.log = self.terminal.Log(f"{hangoutcore.terminal.module}.Bot", loggerHangoutCore)

        self.tree: app_commands.CommandTree = self.tree
        self.BotSynced = False

    async def load_extensions(self, extension: Optional[str] = None) -> None:
        """Loads bot extensions from the cog directory."""
        cog_directory = hangoutcore.DIRECTORY_COGS
        system_cog_directory = Path(__file__).parent / "SystemCogs"

        try:
            local_cogs = [f for f in os.listdir(cog_directory) if f.endswith(".py")]
            system_cogs = [f for f in os.listdir(system_cog_directory) if f.endswith(".py")]
        except Exception as err:
            self.log.ERROR(f"Error reading cog directories: {err}")
            return

        # Load system cogs if not already loaded
        for system_cog in system_cogs:
            if system_cog not in local_cogs:
                src = system_cog_directory / system_cog
                dst = Path(cog_directory) / system_cog
                self.log.INFO(f"Copying system cog '{system_cog}'")
                shutil.copy(src, dst)

        cogs_to_load = [extension] if extension else local_cogs

        for cog in cogs_to_load:
            cog_path = f"cogs.{Path(cog).stem}"
            if cog_path in self.extensions:
                self.log.WARNING(f"Cog '{cog}' is already loaded.")
                continue

            try:
                await self.load_extension(cog_path)
                self.log.INFO(f"Successfully loaded cog: {cog}")
            except Exception as err:
                self.log.ERROR(f"Error loading cog '{cog}': {err}\n{traceback.format_exc()}")

    async def is_user_bot_staff(self, interaction: discord.Interaction) -> bool:
        """Checks if a user has bot staff permissions."""
        self.log.DEBUG(f"Checking bot staff permissions for {interaction.user.id}")
        contributors = hangoutcore.CONFIG_BOT['bot']['contributors']

        for contributor in contributors:
            if (
                contributor['discord_id'] == interaction.user.id
                and contributor['owner']
                and contributor['developer']
            ):
                return True

        await interaction.user.send(
            "You attempted to use a command reserved for bot staff. Continued attempts may result in a blacklist."
        )
        return False

    def create_error_embed(self, error_key: str | int, **kwargs) -> discord.Embed:
        """Creates an error embed from a predefined error configuration."""
        errors = hangoutcore.CONFIG_BOT['bot']['messages']['errors']

        error_data = (
            errors.get(str(error_key))
            or errors.get(int(error_key))
            or errors['error_bot']
        )

        description = error_data['error_message'].format(**kwargs)
        embed = discord.Embed(
            title=error_data['error_title'],
            description=description,
            color=discord.Color.red(),
            timestamp=datetime.now()
        )
        embed.add_field(name="Error Number", value=f"`{error_data['error_number']}`", inline=False)
        return embed

    async def setup_hook(self) -> None:
        self.log.INFO("Starting setup hook.")

        try:
            await self.load_extensions()
        except Exception as e:
            self.log.ERROR(f"Error during setup hook: {e}")

        self.log.INFO("Setup hook complete.")

    async def on_ready(self):
        await self.wait_until_ready()
        await self.change_presence(activity=self.activity)
        self.log.INFO("Bot is ready and logged in.")

    async def close(self):
        self.log.INFO("Shutting down bot.")
        if self.db_pool and not self.db_pool.closed:
            self.log.WARNING("Closing database connection.")
            await self.db_pool.close()


class HangoutCoreCog(commands.Cog):
    """Base class for all cogs in HangoutCore."""

    def __init__(self, bot: HangoutCoreBot):
        self.bot = bot
        self.module = self.qualified_name

        self.terminal = terminal(f"{hangoutcore.terminal.module}.{self.module}", loggerHangoutCore)
        self.log = self.terminal.Log(f"{hangoutcore.terminal.module}.{self.module}", loggerHangoutCore)

        # Optional metadata for cog behavior
        self.development = False
        self.hidden = False
        self.owner_only = False
        self.guild_owner_only = False
        self.guild_admin_only = False
        self.guild_mod_only = False
