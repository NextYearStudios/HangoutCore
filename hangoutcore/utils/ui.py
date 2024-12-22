"""
    HangoutCore Module Script.
    ----------
    Last Updated: June 24, 2024
    Last Updated by: Lino
    License: Refer to LICENSE.md
    Notes:
        None
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    This script handles the following:
    ----------
    Common Discord UI Classes such as Embeds, Views, etc
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    WARNING: This is a Core Script
        › Please do not modify any of the following content unless you know what you're doing. Modifying the following code and not updating the rest of the bot 
            code to match can/will cause issues.
        › If you do decide to modify the following code please understand that HangoutCore's Dev team, Discord.py's Dev Team nor Python's Dev team are obligated
            to help you.
        › By Modifying the following code you acknowledge and agree to the text above.
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Section Title: Dependencies

import math
from datetime import datetime
from typing import Optional

import discord

import hangoutcore
from hangoutcore.utils import database, terminal

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Section Title: Generic Discord UI Functions and Classes


class Confirm(discord.ui.View):
    def __init__(
        self, confirmation: str = "Confirming.", cancellation: str = "Cancelling."
    ):
        self.confirmation = confirmation
        self.cancellation = cancellation
        super().__init__()
        self.value = None

    # When the confirm button is pressed, set the inner value to `True` and
    # stop the View from listening to more input.
    # We also send the user an ephemeral message that we're confirming their choice.
    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.green)
    async def confirm(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await interaction.response.send_message(self.confirmation, ephemeral=True)
        self.value = True
        self.confirm.style = discord.ButtonStyle.grey
        self.stop()

    # This one is similar to the confirmation button except sets the inner value to `False`
    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.grey)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(self.cancellation, ephemeral=True)
        self.value = False
        self.confirm.style = discord.ButtonStyle.grey
        self.stop()


class PaginationView(discord.ui.View):
    def __init__(
        self, data, interaction: discord.Interaction, timeout: Optional[float] = 180
    ):
        super().__init__(timeout=timeout)
        self.originalInteraction = interaction

        if data is None:
            terminal.log.ERROR(f"Attempted to create pageView with no data.")
            return

        if data["embed"] is None:
            terminal.log.ERROR(f"Attempted to create pageView with invalid embed data.")
            return

        _dataTmplate: dict = {
            "embed": {
                "title": "",
                "description": "",
                "footer": "",
                "author": {"name": "", "url": "", "icon_url": ""},
                "image": "",
                "color": discord.Color.dark_embed(),
                "pageItemLimit": 5,
            },
            "pageData": [
                # {
                #     "title": "",
                #     "description": "",
                #     "sections": []
                # }
            ],
        }

        self.data = data

        self.embedTitle: str
        self.embedDescription: str
        self.embedFooter: str
        self.embedColor: discord.Color

        self.sectionLimit: int = data["embed"]["pageItemLimit"]
        self.currentPage: int = 0
        self.pages: list = []

    def processData(self):
        self.embedTitle: str = self.data["embed"]["title"]
        self.embedDescription: str = self.data["embed"]["description"]
        self.embedFooter: str = self.data["embed"]["footer"]
        self.embedColor: discord.Color = self.data["embed"]["color"]

        self.embedAuthor = self.data["embed"]["author"]

        self.pages = []

        for page in self.data["pageData"]:
            _sectionMultiple = math.ceil(len(page["sections"]) / self.sectionLimit)
            _sections = page["sections"]

            if len(page["sections"]) > self.sectionLimit:
                for m in range(_sectionMultiple):
                    _mm = m + 1

                    _startMult = self.sectionLimit * m
                    _endMult = self.sectionLimit * _mm

                    _page = {
                        "title": page["title"],
                        "description": page["description"],
                        "footer": page["footer"],
                        "sections": [],
                    }

                    if m > 0:
                        _page["title"] = _page["title"] + " (cont'd)"

                    for x in range(_startMult, _endMult):
                        _xm = x

                        if _xm < len(page["sections"]):
                            try:
                                _section = _sections[_xm]
                                _page["sections"].append(_section)

                            except IndexError as e:
                                terminal.log.ERROR(f"{e}")

                    self.pages.append(_page)
            else:
                self.pages.append(page)

    def createEmbed(self):
        _embed = discord.Embed(
            title=self.embedTitle,
            description=self.embedDescription,
            color=self.embedColor,  # discord.Color.from_rgb(47, 49, 54)
            timestamp=datetime.now(),
        )

        if self.embedAuthor is not None:
            _embed.set_author(
                name=self.embedAuthor["name"],
                url=self.embedAuthor["url"],
                icon_url=self.embedAuthor["icon_url"],
            )

        _embed.set_footer(
            text=f"Page: {self.currentPage+1} of {len(self.pages)} - {self.embedFooter}"
        )

        _page = self.pages[self.currentPage]
        _pT = _page["title"]
        _pD = _page["description"]
        _pF = _page["footer"]

        if _pT is not None:
            _embed.title = f"{self.embedTitle}: {_pT}"
        else:
            _embed.title = self.embedTitle

        if _pD is not None:
            _embed.description = f"{self.embedDescription}{_pD}"
        else:
            _embed.description = self.embedDescription

        if _pF is not None:
            _embed.description = f"{_embed.description}{self.embedFooter}"
            _embed.set_footer(
                text=f"Page: {self.currentPage+1} of {len(self.pages)} - {_pF}"
            )
        else:
            _embed.set_footer(
                text=f"Page: {self.currentPage+1} of {len(self.pages)} - {self.embedFooter}"
            )

        for section in _page["sections"]:
            _embed.add_field(
                name=section["name"], value=section["description"], inline=False
            )

        #     _tempPage = []

        #     for _section in _page['sections']:
        #         if len(_tempPage) < self.sectionLimit:
        #             _tempPage.append(_section)
        #         else:
        #             self.pages.append(_tempPage)
        #             _tempPage = []

        # for value in self.data[self.currentPage][self.dataValue]:
        #     _embed.description = f"{_embed.description} {value}\n"
        return _embed

    async def update_message(self):
        self.updateButtons()
        await self.originalInteraction.edit_original_response(
            embed=self.createEmbed(), view=self
        )

    def updateButtons(self):
        if len(self.pages) <= 1:
            self.first.disabled = True
            self.first.style = discord.ButtonStyle.gray
            self.previous.disabled = True
            self.previous.style = discord.ButtonStyle.gray
            self.last.disabled = True
            self.last.style = discord.ButtonStyle.gray
            self.next.disabled = True
            self.next.style = discord.ButtonStyle.gray
            self.count.label = f"Page: {self.currentPage + 1}"
            return

        if self.currentPage == 0:
            self.first.disabled = True
            self.first.style = discord.ButtonStyle.gray
            self.previous.disabled = True
            self.previous.style = discord.ButtonStyle.gray
        else:
            self.first.disabled = False
            self.first.style = discord.ButtonStyle.blurple
            self.previous.disabled = False
            self.previous.style = discord.ButtonStyle.gray

        if self.currentPage == (len(self.pages) - 1):
            self.last.disabled = True
            self.last.style = discord.ButtonStyle.gray
            self.next.disabled = True
            self.next.style = discord.ButtonStyle.gray
        else:
            self.last.disabled = False
            self.last.style = discord.ButtonStyle.blurple
            self.next.disabled = False
            self.next.style = discord.ButtonStyle.gray

        self.count.label = f"Page: {self.currentPage + 1}"

    @discord.ui.button(
        label="|<", style=discord.ButtonStyle.blurple, custom_id="persistent_help:first"
    )
    async def first(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)
        self.currentPage = 0
        await self.update_message()

    @discord.ui.button(
        label="<", style=discord.ButtonStyle.gray, custom_id="persistent_help:backward"
    )
    async def previous(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await interaction.response.defer(ephemeral=True)
        if self.currentPage != 0:
            self.currentPage -= 1
            await self.update_message()

    @discord.ui.button(
        label=f"Page: ",
        style=discord.ButtonStyle.gray,
        disabled=True,
        custom_id="persistent_help:page_num",
    )
    async def count(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)
        pass  # Do whatever your button needs to do here.

    @discord.ui.button(
        label=">", style=discord.ButtonStyle.gray, custom_id="persistent_help:forward"
    )
    async def next(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)
        if self.currentPage != (len(self.pages) - 1):
            self.currentPage += 1
            await self.update_message()

    @discord.ui.button(
        label=">|", style=discord.ButtonStyle.blurple, custom_id="persistent_help:last"
    )
    async def last(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)
        self.currentPage = len(self.pages) - 1
        await self.update_message()
