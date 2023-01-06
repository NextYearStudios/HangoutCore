import discord
import typing
import traceback

from datetime import datetime
from discord import app_commands, ui
from discord.ext import commands
from discord.utils import get
from typing import Optional

from hangoutcore.bot import HangoutCoreBot
from hangoutcore.util import Config, Database, CommonUI, Local, Terminal

        
class System(commands.Cog):
    """System commands used to setup/manipulate the bot specific to the guild."""

    def __init__(self, bot: HangoutCoreBot) -> None:
        self.bot = bot
        self.config: Config = bot.config
        self.database: Database = bot.database
        self.local: Local = Local()
        self.terminal: Terminal = Terminal()
        self.log: Terminal.Log = self.terminal.Log()
        self.log.setLoggerName("Cog_System")
        self.development = False
        self.hidden = True

        self.contextMenu_Setup = app_commands.ContextMenu(
            name='Setup Bot',
            callback=self.contextmenu,
        )
        self.bot.tree.add_command(self.contextMenu_Setup)
        super().__init__()

    class Feedback(discord.ui.Modal, title='Feedback'):
        # Our modal classes MUST subclass `discord.ui.Modal`,
        # but the title can be whatever you want.

        # This will be a short input, where the user can enter their name
        # It will also have a placeholder, as denoted by the `placeholder` kwarg.
        # By default, it is required and is a short-style input which is exactly
        # what we want.
        name = discord.ui.TextInput(
            label='Name',
            placeholder='Your name here...',
        )

        # This is a longer, paragraph style input, where user can submit feedback
        # Unlike the name, it is not required. If filled out, however, it will
        # only accept a maximum of 300 characters, as denoted by the
        # `max_length=300` kwarg.
        feedback = discord.ui.TextInput(
            label='What do you think of this new feature?',
            style=discord.TextStyle.long,
            placeholder='Type your feedback here...',
            required=False,
            max_length=300,
        )

        async def on_submit(self, interaction: discord.Interaction):
            await interaction.response.send_message(f'Thanks for your feedback, {self.name.value}!', ephemeral=True)

        async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
            await interaction.response.send_message('Oops! Something went wrong.', ephemeral=True)

            # Make sure we know what the error actually is
            traceback.print_tb(error.__traceback__)

    async def contextmenu(self, interaction: discord.Interaction, message: discord.Message):
        await interaction.response.send_modal(self.Feedback())
    
    setupGroup = app_commands.Group(name="setup", description="Bot setup commands.")

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    roleGroup = app_commands.Group(parent=setupGroup, name="role", description=f"Roles used by HangoutCore.")

    @roleGroup.command(description="Setup Mute Role.")
    async def muted(self, interaction: discord.Interaction, role: discord.Role):
        await interaction.response.defer(thinking=True,ephemeral=True)
        guildData = await self.database.retrieveGuild(interaction.guild)

        if guildData is not None:
            data = guildData[2]
            data['roles']['guild_muted'] = role.id
            await self.database.updateGuild(interaction.guild, data)
            await interaction.followup.send(f"Role has been set to {role.mention}")
        else:
            await interaction.followup.send(f"Failed to retrieve database entry for guild: {interaction.guild.name}.")
        
    @roleGroup.command(description="Setup Trial Moderator Role.")
    async def trial_moderator(self, interaction: discord.Interaction, role: discord.Role):
        await interaction.response.defer(thinking=True,ephemeral=True)
        guildData = await self.database.retrieveGuild(interaction.guild)

        if guildData is not None:
            data = guildData[2]
            data['roles']['guild_trial_moderator'] = role.id
            await self.database.updateGuild(interaction.guild, data)
            await interaction.followup.send(f"Role has been set to {role.mention}")
        else:
            await interaction.followup.send(f"Failed to retrieve database entry for guild: {interaction.guild.name}.")
        
    @roleGroup.command(description="Setup Moderator Role.")
    async def moderator(self, interaction: discord.Interaction, role: discord.Role):
        await interaction.response.defer(thinking=True,ephemeral=True)
        guildData = await self.database.retrieveGuild(interaction.guild)

        if guildData is not None:
            data = guildData[2]
            data['roles']['guild_moderator'] = role.id
            await self.database.updateGuild(interaction.guild, data)
            await interaction.followup.send(f"Role has been set to {role.mention}")
        else:
            await interaction.followup.send(f"Failed to retrieve database entry for guild: {interaction.guild.name}.")
        
    @roleGroup.command(description="Setup Administrator Role.")
    async def administrator(self, interaction: discord.Interaction, role: discord.Role):
        await interaction.response.send_message(f"{role.mention}", ephemeral = True)
        await interaction.response.defer(thinking=True,ephemeral=True)
        guildData = await self.database.retrieveGuild(interaction.guild)

        if guildData is not None:
            data = guildData[2]
            data['roles']['guild_administrator'] = role.id
            await self.database.updateGuild(interaction.guild, data)
            await interaction.followup.send(f"Role has been set to {role.mention}")
        else:
            await interaction.followup.send(f"Failed to retrieve database entry for guild: {interaction.guild.name}.")
        
    @roleGroup.command(description="Setup Owner Role.")
    async def owner(self, interaction: discord.Interaction, role: discord.Role):
        await interaction.response.defer(thinking=True,ephemeral=True)
        guildData = await self.database.retrieveGuild(interaction.guild)

        if guildData is not None:
            data = guildData[2]
            data['roles']['guild_owner'] = role.id
            await self.database.updateGuild(interaction.guild, data)
            await interaction.followup.send(f"Role has been set to {role.mention}")
        else:
            await interaction.followup.send(f"Failed to retrieve database entry for guild: {interaction.guild.name}.")

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    autoroleGroup = app_commands.Group(parent=setupGroup, name="auto_role", description=f"Toggleable Features.")
        
    @autoroleGroup.command(description="Enable/Disable AutoRole locally.\nRunning command with no variable will return current status.")
    async def status(self, interaction: discord.Interaction, enable: Optional[bool]):
        await interaction.response.defer(thinking=True,ephemeral=True)
        guildData = await self.database.retrieveGuild(interaction.guild)

        if guildData is not None:
            data = guildData[2]
            if enable is None:
                role_string = ""
                if len(data['extras']['guild_autoroles']['roles']) > 0:
                    for role_id in data['extras']['guild_autoroles']['roles']:
                        role = interaction.guild.get_role(int(role_id))
                        role_string = f"{role_string}    - {role.mention}\n"
                else:
                    role_string = "    None."
                await interaction.followup.send(f"AutoRole is currently `{data['extras']['guild_autoroles']['enabled']}`.\nRoles:\n{role_string}")
            else:
                data['extras']['guild_autoroles']['enabled'] = enable
                await self.database.updateGuild(interaction.guild, data)
                await interaction.followup.send(f"AutoRole was set to `{data['extras']['guild_autoroles']['enabled']}`.")
        else:
            await interaction.followup.send(f"Failed to retrieve database entry for guild: {interaction.guild.name}.")

    @autoroleGroup.command(description="Add a role to AutoRole.")
    async def add(self, interaction: discord.Interaction, role: discord.Role, account_time_requirement: Optional[int], guild_time_requirement: Optional[int], level_requirement: Optional[int]):
        # Account time requirement = How long the account has to have existed on discord before they will recieve this role.
        # Guild time requirement = How long the account has to be in this guild to recieve this role.
        # Level requirement = How active this user has to be to recieve this role.

        await interaction.response.defer(thinking=True,ephemeral=True)
        guildData = await self.database.retrieveGuild(interaction.guild)

        if guildData is not None:
            data = guildData[2]
            data['extras']['guild_autoroles']['roles'].append(role.id)
            await self.database.updateGuild(interaction.guild, data)
            await interaction.followup.send(f"{role.mention} has been added to AutoRole.")
        else:
            await interaction.followup.send(f"Failed to retrieve database entry for guild: {interaction.guild.name}.")

    @autoroleGroup.command(description="Remove a role from AutoRole.")
    async def remove(self, interaction: discord.Interaction, role: discord.Role):
        await interaction.response.defer(thinking=True,ephemeral=True)
        guildData = await self.database.retrieveGuild(interaction.guild)

        if guildData is not None:
            data = guildData[2]
            if (role.id) in data['extras']['guild_autoroles']['roles']:
                data['extras']['guild_autoroles']['roles'].remove(role.id)
                await self.database.updateGuild(interaction.guild, data)
                await interaction.followup.send(f"{role.mention} has been removed from AutoRole.")
            else:
                await interaction.followup.send(f"The role you provided is not listed as an AutoRole.")
        else:
            await interaction.followup.send(f"Failed to retrieve database entry for guild: {interaction.guild.name}.")

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    @setupGroup.command(description="Enable/Disable Guild Economy. For More do `/help setup economy`")
    @app_commands.default_permissions(administrator=True)
    async def economy(self, interaction: discord.Interaction, enable: bool, channel: Optional[discord.TextChannel], bank_name: Optional[str], bank_currency_icon: Optional[str], bank_starting_balance: Optional[int]):
        await interaction.response.defer(thinking=True, ephemeral=True)
        guildData = await self.database.retrieveGuild(interaction.guild)
        if guildData is None:
            await interaction.followup.send(f"Failed to retrieve database entry for guild: {interaction.guild.name}.", ephemeral=True)
        else:
            data = guildData[2]

        if enable is None:
            await interaction.followup.send(f"Command Failed. Please notify bot staff.", ephemeral=True)

        if enable:
            data['extras']['guild_economy']['enabled'] = enable
            _bank_channel = None
            _bank_message = None
            _bank_name = f"{interaction.guild.name} Bank!"
            _bank_icon = "$"
            _bank_starting_amount = 1000

            if bank_name is not None:
                _bank_name = bank_name
            data['extras']['guild_economy']['name'] = _bank_name

            if bank_currency_icon is not None:
                _bank_icon = bank_currency_icon
            data['extras']['guild_economy']['currency'] = _bank_icon

            if bank_starting_balance is not None:
                _bank_starting_amount = bank_starting_balance
            data['extras']['guild_economy']['balance_start'] = _bank_starting_amount

            if channel is not None:
                _bank_channel = channel
            else:
                _bank_channel = await interaction.guild.create_text_channel(name=f"Guild Bank", reason=f"{self.config.CONFIG['bot']['name']} Economy Module")
                data['extras']['guild_economy']['channel'] = _bank_channel.id

                _bank_message = await _bank_channel.send("...")
                bankView = CommonUI.GuildBankView( _bank_message, self.database, data, "System Response", None)
                await _bank_channel.edit(content=None, view=bankView)
                await _bank_channel.set_permissions(interaction.guild.default_role, reason="Economy Module", send_messages=False, use_application_commands=True)
                data['extras']['guild_economy']['message'] = _bank_message.id
                
            await self.database.updateGuild(interaction.guild, data)

            await interaction.followup.send(f"Updated Database.")
            await bankView.update_message()
        else:
            data['extras']['guild_economy']['enabled'] = enable
            await self.database.updateGuild(interaction.guild, data)
            await interaction.followup.send(f"Updated Database.")

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    selfroleGroup = app_commands.Group(parent=setupGroup, name="self_role", description=f"Toggleable Features.")
        
    @selfroleGroup.command(description="Enable/Disable SelfRole locally.\nRunning command with no variable will return current status.")
    async def status(self, interaction: discord.Interaction):
        pass # TODO: Complete Command

    @selfroleGroup.command(description="Add a self assignable role.")
    async def add(self, interaction: discord.Interaction, role: discord.Role):
        pass # TODO: Complete Command

    @selfroleGroup.command(description="Remove a self assignable role.")
    async def remove(self, interaction: discord.Interaction, role: discord.Role):
        pass # TODO: Complete Command

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    @setupGroup.command(description="Enable/Disable Guild Statistics. For More do `/help setup statistics`")
    @app_commands.default_permissions(administrator=True)
    async def statistics(self, interaction: discord.Interaction, enable: bool, display_active_members: Optional[bool], display_total_members: Optional[bool], display_bot_members: Optional[bool]):
        await interaction.response.defer(thinking=True,ephemeral=True)
        if not await self.bot.is_user_blacklisted(interaction.user):
            pass
        else:
            await interaction.followup.send(content=f"You're blacklisted from this bot.")

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    @app_commands.default_permissions(administrator=True)
    @setupGroup.command(description="Enable/Disable Staff Announcements.\nSet Staff Announcement Channel.")
    async def staff_announcements(self, interaction: discord.Interaction, enable: bool, channel: Optional[discord.TextChannel], announce_user_ban: Optional[bool], announce_user_kick: Optional[bool], announce_user_mute: Optional[bool], announce_user_reported: Optional[bool], announce_user_warn: Optional[bool]):
        await interaction.response.defer(thinking=True,ephemeral=True)
        guildData = await self.database.retrieveGuild(interaction.guild)

        if guildData is not None:
            data = guildData[2]

            data['extras']['guild_staff_announcements']['enabled'] = enable
            if enable:
                if channel is not None:
                    data['extras']['guild_staff_announcements']['channel'] = channel.id
                else:
                    _staffannounce_channel = await interaction.guild.create_text_channel(name=f"Staff Announcements", reason=f"{self.config.CONFIG['bot']['name']} System Module.")
                    await _staffannounce_channel.set_permissions(interaction.guild.default_role, reason=f"{self.config.CONFIG['bot']['name']} System Module.", read_messages=False, use_application_commands=True)
                    if data['roles']['guild_muted'] != 0:
                        _role = interaction.guild.get_role(id=data['roles']['guild_muted'])
                        if _role is not None:
                            await _staffannounce_channel.set_permissions(_role, reason=f"{self.config.CONFIG['bot']['name']} System Module.", send_messages=False)

                    if data['roles']['guild_trial_moderator'] != 0:
                        _role = interaction.guild.get_role(id=data['roles']['guild_trial_moderator'])
                        if _role is not None:
                            await _staffannounce_channel.set_permissions(_role, reason=f"{self.config.CONFIG['bot']['name']} System Module.", read_messages=True, send_messages=True, use_application_commands=True)

                    if data['roles']['guild_moderator'] != 0:
                        _role = interaction.guild.get_role(id=data['roles']['guild_moderator'])
                        if _role is not None:
                            await _staffannounce_channel.set_permissions(_role, reason=f"{self.config.CONFIG['bot']['name']} System Module.", read_messages=True, send_messages=True, use_application_commands=True)

                    if data['roles']['guild_administrator'] != 0:
                        _role = interaction.guild.get_role(id=data['roles']['guild_administrator'])
                        if _role is not None:
                            await _staffannounce_channel.set_permissions(_role, reason=f"{self.config.CONFIG['bot']['name']} System Module.", read_messages=True, send_messages=True, use_application_commands=True)

                    if data['roles']['guild_owner'] != 0:
                        _role = interaction.guild.get_role(id=data['roles']['guild_owner'])
                        if _role is not None:
                            await _staffannounce_channel.set_permissions(_role, reason=f"{self.config.CONFIG['bot']['name']} System Module.", read_messages=True, send_messages=True, use_application_commands=True)
                    
                    data['extras']['guild_staff_announcements']['channel'] = _staffannounce_channel.id

                if announce_user_ban is not None:
                    data['extras']['guild_staff_announcements']['variables']['user_ban'] = announce_user_ban

                if announce_user_kick is not None:
                    data['extras']['guild_staff_announcements']['variables']['user_kick'] = announce_user_kick

                if announce_user_mute is not None:
                    data['extras']['guild_staff_announcements']['variables']['user_mute'] = announce_user_mute

                if announce_user_reported is not None:
                    data['extras']['guild_staff_announcements']['variables']['user_reported'] = announce_user_reported

                if announce_user_warn is not None:
                    data['extras']['guild_staff_announcements']['variables']['user_warn'] = announce_user_warn
            else:
                # Since this feature is being 'disabled' We reset every other value.
                data['extras']['guild_staff_announcements']['channel'] = 0
                data['extras']['guild_staff_announcements']['variables']['user_ban'] = False
                data['extras']['guild_staff_announcements']['variables']['user_kick'] = False
                data['extras']['guild_staff_announcements']['variables']['user_mute'] = False
                data['extras']['guild_staff_announcements']['variables']['user_reported'] = False
                data['extras']['guild_staff_announcements']['variables']['user_warn'] = False



            await self.database.updateGuild(interaction.guild, data)
            _embed = discord.Embed(title = f"Updated Staff Announcements", color = discord.Color.from_rgb(47, 49, 54), timestamp=datetime.now())
            _embed.set_footer(text=f"System Response")
            # _embed.description(f"Enabled: {data['extras']['guild_staff_announcements']['enabled']}\nChannel: {data['extras']['guild_staff_announcements']['channel']}")
            await interaction.followup.send(embed=_embed, ephemeral=True) # TODO: Add summary of updated variablese
        else:
            await interaction.followup.send(f"Failed to retrieve database entry for guild: {interaction.guild.name}.")

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    @setupGroup.command(description="Enable/Disable Guild Suggestions. For More do `/help setup suggestions`")
    @app_commands.default_permissions(administrator=True)
    async def suggestions(self, interaction: discord.Interaction, enable: bool, channel: Optional[discord.TextChannel], allow_vote: Optional[bool]):
        # channel = The channel where are able to be submitted by users in the guild
        # allow vote = When set to true, each message in the suggestions channel will recieve reactions for voting on submitted suggestions
        await interaction.response.defer(thinking=True,ephemeral=True)
        if not await self.bot.is_user_blacklisted(interaction.user):
            pass
        else:
            await interaction.followup.send(content=f"You're blacklisted from this bot.")

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    @setupGroup.command(description="Enable/Disable Guild Tickets. For More do `/help setup tickets`")
    @app_commands.default_permissions(administrator=True)
    async def tickets(self, interaction: discord.Interaction, enable: bool, category: Optional[discord.CategoryChannel], staff_role: Optional[discord.Role]):
        # category = The category where tickets are created and stored.
        # staff role = The role that is mention upon ticket creation. Ideally we'd like this to be staff in order to insure member's privacy is respected when submitting tickets.
        await interaction.response.defer(thinking=True,ephemeral=True)
        if not await self.bot.is_user_blacklisted(interaction.user):
            pass
        else:
            await interaction.followup.send(content=f"You're blacklisted from this bot.")

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    @setupGroup.command(description="Enable/Disable Guild Verification. For More do `/help setup verification`")
    @app_commands.default_permissions(administrator=True)
    async def verification(self, interaction: discord.Interaction, enable: bool, channel: Optional[discord.TextChannel], role: Optional[discord.Role]):
        # channel = Channel where verification process will be sent (button, reaction, etc.)
        # role = The role that is assigned upon completing the 'verification' process.
        await interaction.response.defer(thinking=True,ephemeral=True)
        if not await self.bot.is_user_blacklisted(interaction.user):
            pass
        else:
            await interaction.followup.send(content=f"You're blacklisted from this bot.")

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    @setupGroup.command(description="Enable/Disable Guild Voice Lobbies. For More do `/help setup voice_lobby`")
    @app_commands.default_permissions(administrator=True)
    async def voice_lobby(self, interaction: discord.Interaction, enable: bool, channel: Optional[discord.TextChannel]):
        await interaction.response.defer(thinking=True,ephemeral=True)
        if not await self.bot.is_user_blacklisted(interaction.user):
            guildData = await self.database.retrieveGuild(interaction.guild)

            if guildData is not None:
                _guildData = guildData[2]

                if enable:
                    _guildData['extras']['guild_voice_lobby']['enabled'] = enable

                    if channel is not None:
                        _guildData['extras']['guild_voice_lobby']['channel'] = channel.id
                    else:
                        # Create Category Voice Lobbies, with necessary permissions.
                        reason = f"{self.config.CONFIG['bot']['name']} System Module."
                        _vcCategory = await interaction.guild.create_category_channel(name=f"Voice Lobbies", reason=reason)
                        if _guildData['roles']['guild_muted'] != 0:
                            _role = interaction.guild.get_role(id=_guildData['roles']['guild_muted'])
                            if _role is not None:
                                await _vcCategory.set_permissions(_role, reason=reason, send_messages=False, speak=False, request_to_speak=False)

                        _vcLobby = await _vcCategory.create_voice_channel(name="Lobby", reason=reason)
                        _guildData['extras']['guild_voice_lobby']['channel'] = _vcLobby.id
                        
                else:
                    # Reset channel to 0 since this feature is now being disabled.
                    _guildData['extras']['guild_voice_lobby']['enabled'] = enable
                    _guildData['extras']['guild_voice_lobby']['channel'] = 0
            await self.database.updateGuild(interaction.guild, _guildData)
            # Create an embed to nicely display what we've just done.
            _embed = discord.Embed(
                title = f"Updated Voice Lobbies", 
                color = discord.Color.from_rgb(47, 49, 54), 
                timestamp = datetime.now(),
                description = f"Enabled: `{_guildData['extras']['guild_voice_lobby']['enabled']}`")
            _embed.set_footer(text=f"System Response")
            await interaction.followup.send(embed=_embed, ephemeral = True)
        else:
            await interaction.followup.send(content=f"You're blacklisted from this bot.")

    
        
async def setup(bot: HangoutCoreBot):
    await bot.add_cog(System(bot))
    await Terminal().Log().WARNING(f"System has been loaded.")
    
    
async def teardown(bot: HangoutCoreBot):
    await bot.remove_cog(System(bot))
    await Terminal().Log().WARNING(f"System has been unloaded.")