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

    async def updateUserRank(self, user, amount: int):
        userData = await self.database.retrieveUser(user)
        _userData = None
        if userData is not None:
            _userData = userData[2]
        if not _userData['bot']['blacklisted']:
            _levelXP = 1500

            _userData['experience'] += amount

            if _userData['experience'] >= _levelXP * _userData['level']:
                _userData['level'] += 1

            await self.database.updateUser(user, _userData)
        

    async def helpData(self, administrator: bool = False, developer: bool = False, developerGuild: bool = False):
        cogs = self.bot.cogs
        pageLimit = 5
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

    @commands.Cog.listener()
    async def on_app_command_completion(self, interaction: discord.Interaction, command):
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

                    await self.updateUserRank(message.author, _wordCount*_charCount)


async def setup(bot: HangoutCoreBot):
    await bot.add_cog(General(bot))
    await Terminal().Log().WARNING(f"General has been loaded.")
    
    
async def teardown(bot: HangoutCoreBot):
    await bot.remove_cog(General(bot))
    await Terminal().Log().WARNING(f"General has been unloaded.")