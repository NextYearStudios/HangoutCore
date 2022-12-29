import discord
import typing

from datetime import datetime
from discord import app_commands, ui
from discord.ext import commands
from typing import Optional

from hangoutcore.bot import HangoutCoreBot
from hangoutcore.util import Config, CommonUI, Local, Terminal

class Moderation(commands.Cog):
    """Various commands meant to be used by staff for moderation purposes."""

    def __init__(self, bot: HangoutCoreBot) -> None:
        self.bot = bot
        self.config = bot.config
        self.terminal = Terminal()
        self.log = self.terminal.Log()
        self.log.setLoggerName("Cog_Moderation")
        self.development = False
        self.hidden = True

        self.local = Local()
        super().__init__()

    @app_commands.default_permissions(ban_members=True)
    @app_commands.command(description="Ban a member from the guild.")
    async def ban(self, interaction: discord.Interaction, user: discord.User, reason: Optional[str]):
        await interaction.guild.ban(user=user, reason=reason)
        await interaction.response.send_message(f"Banned {user.mention} for the following reason: \n{reason}", ephemeral=True)

    @app_commands.default_permissions(manage_messages=True)
    @app_commands.command(description="Delete the specified number of messages from this channel.")
    async def clear(self, interaction: discord.Interaction, amount: app_commands.Range[int, 1, 100], user: Optional[discord.User], reason: Optional[str]):
        await interaction.response.defer(ephemeral=True, thinking=True)
        def processmessage(message: discord.Message):
            if len(message.components) > 0 or len(message.embeds) > 0 or message.is_system() or message.pinned:
                return False
            if user is not None:
                return message.author == user
            else:
                return True
        try:
            clearmessages = await interaction.channel.purge(limit=amount, check=processmessage, reason=reason, bulk=True, before=datetime.now())
        except Exception as e:
            print(e)
            
        if len(clearmessages) > 0:
            if user is not None:
                if reason is not None:
                    await interaction.followup.send(f"Cleared {len(clearmessages)} messages posted by {user.mention}. For the following reason:\n{reason}", ephemeral=True)
                else:
                    await interaction.followup.send(f"Cleared {len(clearmessages)} messages posted by {user.mention}.\nNo Reason was provided.", ephemeral=True)
            else:
                await interaction.followup.send(f"Cleared {len(clearmessages)} messages.", ephemeral=True)
        else:
            await interaction.followup.send(f"Unable to clear the requested amount of messages.", ephemeral=True)

    @app_commands.default_permissions(manage_messages=True, manage_channels=True)
    @app_commands.command(description="Delete the specified number of messages from this channel regardless of content.")
    async def forceclear(self, interaction: discord.Interaction, amount: app_commands.Range[int, 1, 100], user: Optional[discord.User], reason: Optional[str]):
        await interaction.response.defer(ephemeral=True, thinking=True)
        def processmessage(message: discord.Message):
            if user is not None:
                return message.author == user
            else:
                return True
        clearmessages = await interaction.channel.purge(limit=amount, check=processmessage, reason=reason, bulk=True, before=datetime.now())

        if len(clearmessages) > 0:
            if user is not None:
                if reason is not None:
                    await interaction.followup.send(f"Cleared {len(clearmessages)} messages posted by {user.mention}. For the following reason:\n{reason}", ephemeral=True)
                else:
                    await interaction.followup.send(f"Cleared {len(clearmessages)} messages posted by {user.mention}.\nNo Reason was provided.", ephemeral=True)
            else:
                await interaction.followup.send(f"Cleared {len(clearmessages)} messages.", ephemeral=True)
        else:
            await interaction.followup.send(f"Unable to clear the requested amount of messages.", ephemeral=True)

    @app_commands.default_permissions(kick_members=True)
    @app_commands.command(description="Kick a member from the guild.")
    async def kick(self, interaction: discord.Interaction, user: discord.User, reason: Optional[str]):
        await interaction.guild.kick(user=user, reason=reason)
        await interaction.response.send_message(f"Kicked {user.mention} for the following reason: \n{reason}", ephemeral=True)

    @app_commands.default_permissions(administrator=True)
    @app_commands.command(description=f"WARNING: THIS CANNOT BE REVERSED. INTENDED TO BE USED WITH '/USE_TEMPLATE'!")
    async def guild_reset(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Confirmation request has been sent to guild owner.", ephemeral=True)
        confirmation = CommonUI.ConfirmationView()

        if interaction.user == interaction.guild.owner:
            await interaction.guild.owner.send(f"Please confirm you'd like to nuke guild {interaction.guild.name}? This action is not reversible and every role and channel will be deleted.",view=confirmation)
        else:
            await interaction.guild.owner.send(f"{interaction.user.mention} has attempted to nuke guild {interaction.guild.name}. Please confirm to proceed. This action is not reversible and every role and channel will be deleted.",view=confirmation)
        
        await confirmation.wait()
        if confirmation.value:
            if interaction.guild is not None:
                for channel in interaction.guild.channels:
                    if channel.id != 855439693306396693:
                        try:
                            await channel.delete(reason=f"Guild Owner Authorized Reset. - {self.config.CONFIG['bot']['name']}")
                        except Exception as e:
                            print(e)

        else:
            print("F")
        # if confirmation.value is None:
        #     await interaction.followup.send(f"Failed.")
        #     return
        # if confirmation.value:
        #     for channel in interaction.guild:
        #         print(f"Deleting Channel:{channel.name}:{channel.id}")
        #     await interaction.followup.send(f"Success.")
        # else:
        #     await interaction.followup.send(f"Cancelled.")

    @app_commands.default_permissions(administrator=True)
    @app_commands.command()
    async def use_template(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=True, ephemeral=True)
        
        GeneralCategory = await interaction.guild.create_category(name="GENERAL",position=0)
        GeneralTextChannel = await interaction.guild.create_channel

async def setup(bot: HangoutCoreBot):
    await bot.add_cog(Moderation(bot))
    await Terminal().Log().WARNING(f"Moderation has been loaded.")
    
    
async def teardown(bot: HangoutCoreBot):
    await bot.remove_cog(Moderation(bot))
    await Terminal().Log().WARNING(f"Moderation has been unloaded.")