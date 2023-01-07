import discord
import typing
import math

from datetime import datetime
from discord import app_commands, ui
from discord.ext import commands
from typing import Optional

from hangoutcore.bot import HangoutCoreBot
from hangoutcore.util import Config, Database, CommonUI, Local, Terminal

class General(commands.Cog):
    """Commands meant to be used by the public for general purposes."""

    def __init__(self, bot: HangoutCoreBot) -> None:
        self.bot = bot
        self.config: Config = bot.config
        self.database: Database = bot.database
        self.local: Local = Local()
        self.terminal: Terminal = Terminal()
        self.log: Terminal.Log = self.terminal.Log()
        self.log.setLoggerName("Cog_General")
        self.development = False
        self.hidden = False

        super().__init__()

    async def updateUserRank(self, guild, user, amount: int):
        if not await self.bot.is_user_blacklisted(user):
            userData = await self.database.retrieveUser(user)
            _userData = None
            if userData is not None:
                _userData = userData[2]
                _rankEntry = None
                
                if len(_userData['rank']['guild']) > 0:
                    for entry in _userData['rank']['guild']:
                        if entry['id'] == guild.id:
                            _rankEntry = entry

                if _rankEntry is None:
                    _levelXP = 1500 * 1 # Amount of experience required to level up
                    _newLevel = 1
                    while amount > _levelXP:
                        _levelXP = 1500 * _newLevel # Update to new level
                        _newLevel += 1

                    _userData['rank']['guild'].append({"id": guild.id, "experience": amount, "level": _newLevel})
                else:
                    _rankEntry['experience'] += amount
                    _levelXP = 1500 * _rankEntry['level'] # Amount of experience required to level up

                    while _rankEntry['experience'] > _levelXP:
                        _levelXP = 1500 * _rankEntry['level'] # Update to new level
                        _rankEntry['level'] += 1

                await self.database.updateUser(user, _userData)
        

    async def helpData(self, administrator: bool = False, developer: bool = False, developerGuild: bool = False):
        cogs = self.bot.cogs
        pageLimit = 10
        data = []
        
        nsfwEmoji = "<:nsfw:1056285352723230751>"
        helpFooter = f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n*Commands with the following emoij are NSFW: {nsfwEmoji}*"
        
        def processItem(item, description, subItems):
            _data = {
                "dataName": item,
                "dataDescription": description,
                "dataValue": []}
            for subItem in subItems:
                _data["dataValue"].append(subItem)
            _data["dataValue"].append(helpFooter)
            data.append(_data)

        for cog in sorted(list(cogs)):
            cogObject = cogs.get(cog)

            if cogObject.hidden and not administrator:
                continue

            if cogObject.development and not developer:
                continue
            
            if cogObject.development and not developerGuild:
                continue
            
            
            commands = []
            for command in cogObject.walk_app_commands():
                if type(command) == app_commands.commands.Group:
                    continue
                else:
                    commandInfo = f"/**"
                    if command.parent is not None:
                        parent = command.parent
                        while parent.parent is not None:
                            parent = parent.parent
                            if parent is not None:
                                commandInfo = f"{commandInfo}{parent.name} "

                        commandInfo = f"{commandInfo}{command.parent.name} {command.name}"
                    else:
                        commandInfo = f"{commandInfo}{command.name}"

                    if command.nsfw:
                        commandInfo = f"{commandInfo}**: {nsfwEmoji}"
                    else:
                        commandInfo = f"{commandInfo}**:"

                    commandInfo = f"{commandInfo}\n- *{command.description}*\n"
                    commands.append(commandInfo)

            if len(commands) > pageLimit:
                _count = 0
                _countMult = 0
                _maxCount = math.ceil(len(commands)/pageLimit)
                _data = []
                processing = True

                while processing:

                    if _count == pageLimit or _count + _countMult == len(commands):
                        if _countMult > 0:
                            processItem(f"{self.config.CONFIG['bot']['name']} {cog} Extension (cont'd)", f"```{cogObject.description}```\n**Commands**:", _data)
                        else:
                            processItem(f"{self.config.CONFIG['bot']['name']} {cog} Extension", f"```{cogObject.description}```\n**Commands**:", _data)
                        _countMult += pageLimit
                        _count = 0
                        _data = []
                        _maxCount -= 1
                    else:
                        _data.append(commands[_count+_countMult])
                        _count += 1

                    if _maxCount == 0:
                        processing = False
            else:
                processItem(f"{cog}", f"```{cogObject.description}```\n**Commands**:", commands)

        return data

    @app_commands.command(description = f"Help command used to display the commands supported by this bot.")
    async def help(self, interaction: discord.Interaction, extension: Optional[str], command: Optional[str]):
        userData = await self.database.retrieveUser(interaction.user)
        _userData = None
        if userData is not None:
            _userData = userData[2]
        if not _userData['bot']['blacklisted']:
            administrator = False
            developer = False
            developerGuild = False

            if interaction.user.guild_permissions.administrator:
                administrator = True

            for contributer in self.config.CONFIG['bot']['contributers']:
                if contributer['discord_id'] == interaction.user.id:
                    developer = True

            if interaction.guild_id == self.config.CONFIG['bot']['developer_guild_id']:
                developerGuild = True

            data = await self.helpData(administrator, developer, developerGuild) # administrator: bool = False, developer: bool = False, developerGuild: int = 0

            
            pageView = CommonUI.PaginationView(data, "System Response", "dataName", "dataDescription", "dataValue", interaction, None)
            await interaction.response.send_message(ephemeral=True, view=pageView)
            await pageView.update_message()
            
        else:
            await interaction.response.send_message(f"You're blacklisted from using this bot. If you believe this is an error please contact a bot staff member.", ephemeral=True)


    @app_commands.command(description = f"...")
    async def stats(self, interaction: discord.Interaction, user: Optional[discord.User]):
        await interaction.response.defer(thinking=True, ephemeral=True)
        _user = interaction.user
        if user is not None:
            _user = user
        if not await self.bot.is_user_blacklisted(_user):
            userData = await self.database.retrieveUser(_user)
            _userData = None
            if userData is not None:
                _userData = userData[2]

                _embed = discord.Embed(title = f"{_user.name}'s Stats", color = discord.Color.from_rgb(47, 49, 54), timestamp=datetime.now())
                _embed.set_footer(text=f"System Response")
                # _embed.description(f"")
                
                for entry in _userData['rank']['guild']:
                    if entry['id'] == interaction.guild.id:
                        _embed.add_field(
                            name = f"Level",
                            value = f"{entry['level']}",
                            inline = True)
                        _embed.add_field(
                            name = f"Experience",
                            value = f"{entry['experience']}",
                            inline = True)
                await interaction.followup.send(embed=_embed, ephemeral=False)
        else:
            await interaction.followup.send(content="config message", ephemeral=True)

    @commands.Cog.listener()
    async def on_app_command_completion(self, interaction: discord.Interaction, command):
        if not await self.bot.is_user_blacklisted(interaction.user):
            await self.database.updateCommandUse(interaction.user, command.module.split('.')[-1], command.name)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.content == "<@753399339669520406>":
            await message.reply(f"For help please use the /help command.")
        else:
            # Process user xp/cash
            _matchesPrevious = False
            async for item in message.channel.history(limit=3, before=message.created_at):
                if item.content.lower() == message.content.lower():
                    _matchesPrevious = True

            if _matchesPrevious == False:
                if not message.author.bot and not message.is_system():
                    if not await self.bot.is_user_blacklisted(message.author):
                        _filter = ['.','!','@','<','>',',','?','/','\\','|','[',']','{','}','(',')','\n']
                        _words = message.content
                        for filter in _filter:
                            if filter == "\n":
                                _words:str = _words.replace(filter, ' ')
                            else:
                                _words:str = _words.replace(filter, '')

                        _words = _words.split(' ')
                        _alphaWords = []
                        for word in _words:
                            if word.isalpha():
                                _alphaWords.append(word)

                        _alphaWords = set(_alphaWords)
                        _wordCount = 0
                        _charCount = 0
                        for word in _alphaWords:
                            _charCount += len(word)
                            _wordCount += 1

                        await self.updateUserRank(message.guild, message.author, _wordCount*_charCount)


    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        # TODO: Add check for voice lobbies, Assistance Lobbies
        
        if before.channel is not None and before.channel.guild is not None:
            guildData = await self.database.retrieveGuild(before.channel.guild)

            if guildData is not None:
                _guildData = guildData[2]

                if _guildData['extras']['guild_voice_lobby']['enabled'] and _guildData['extras']['guild_voice_lobby']['channel'] != 0:
                    _pvcChannel = before.channel.guild.get_channel(_guildData['extras']['guild_voice_lobby']['channel'])
                    _pvcCategory = _pvcChannel.category

                    if _pvcCategory.id == before.channel.category.id:
                        if _pvcChannel.id != before.channel.id:
                            if len(before.channel.members) == 0:
                                await before.channel.delete(reason="No Users in Private Chat")

        if after.channel is not None and after.channel.guild is not None:
            guildData = await self.database.retrieveGuild(after.channel.guild)

            if guildData is not None:
                _guildData = guildData[2]

                if _guildData['extras']['guild_voice_lobby']['enabled'] and _guildData['extras']['guild_voice_lobby']['channel'] != 0:
                    _pvcChannel = after.channel.guild.get_channel(_guildData['extras']['guild_voice_lobby']['channel'])
                    _pvcCategory = _pvcChannel.category

                    if _pvcChannel.id == after.channel.id:
                        _memberPVC = await _pvcCategory.create_voice_channel(name = f"{member.name}'s VC")
                        await member.move_to(_memberPVC, reason=f"Private Voice Channel Creation.")
                        await _memberPVC.set_permissions(after.channel.guild.default_role, reason = "Private Voice Channel", connect=False)
                        if _guildData['extras']['guild_verification']['enabled'] and _guildData['extras']['guild_verification']['role'] != 0:
                            _baseRole = after.channel.guild.get_role(_guildData['extras']['guild_verification']['role'])
                            await _memberPVC.set_permissions(_baseRole, reason = "Private Voice Channel", connect=False)
                    # # Add permissions etc.
            

async def setup(bot: HangoutCoreBot):
    await bot.add_cog(General(bot))
    await Terminal().Log().WARNING(f"General has been loaded.")
    
    
async def teardown(bot: HangoutCoreBot):
    await bot.remove_cog(General(bot))
    await Terminal().Log().WARNING(f"General has been unloaded.")