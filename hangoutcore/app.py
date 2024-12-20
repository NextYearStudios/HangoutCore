import asyncio
import hangoutcore
import sys
import textual
import time

from hangoutcore.utils import terminal

from rich.console import Console
from rich.text import Text

from textual import events, RenderableType
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import *
from textual.events import Mount
from textual.reactive import reactive
from textual.screen import ModalScreen, Screen
from textual.widgets import *

class LoadingDisplay(Static):
    def compose(self) -> ComposeResult:
        yield LoadingIndicator(id = "loading_indicator")
        # yield Label(self.title, id = "loading_label", expand = True)
        yield Label("Loading...", id = "loading_label", expand = True)
        

class appLoadingScreen(Screen):
    CSS_PATH = "./tcss/loading.tcss"
    def compose(self) -> ComposeResult:
        yield Header(True)
        yield LoadingDisplay()
        yield Footer()

# class OutConsole(ScrollView):
#     prev = Text("")

#     async def eval(self, text_input):
#         pre_y = self.y
#         with console.capture() as capture:
#             try:
#                 console.print(eval(text_input))
#             except Exception:
#                 console.print_exception(show_locals=True)
#         self.prev.append(Text.from_ansi(capture.get() + "\n"))
#         await self.update(self.prev)
#         self.y = pre_y
#         self.animate("y", self.window.virtual_size.height, duration=1, easing="linear")


# class InConsole(TextInput):
#     def __init__(self, out):
#         super(InConsole, self).__init__()
#         self.out = out

#     async def on_key(self, event: events.Key) -> None:
#         if event.key == "enter":
#             await self.out.eval(self.value)
#             self.value = ""

class appDashboardScreen(Screen):
    def flush(self):
        pass

    def write(self, txt:str):
        self.query_one(RichLog).write(txt.rstrip())
    
    def compose(self) -> ComposeResult:
        yield Header(True)
        yield RichLog()
        yield Footer()
        sys.stdout = self
    
    def on_key(self, event: events.Key):
        # self.query_one(RichLog).write(event)
        print("Test On Dashboard")
        
class appSettingsScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Header(True)
        yield Placeholder("Settings Screen")
        yield Footer()
        
class appHelpScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Header(True)
        yield Placeholder("Help Screen")
        yield Footer()
        
    def on_key(self, event: events.Key):
        print("Test On Help Screen")

class HangoutCoreApp(App):
    '''Main Textual application for Hangoutcore; Will fill details later'''
    # CSS_PATH = ""
    BINDINGS = [
        Binding(key = "escape", action = "quit", description = "Quit the app."),
        Binding(key = "question_mark", action = "help", description = "Show help screen", key_display = "?"),
        ("ctrl+l", "switch_mode('loading')", "Loading"),
        ("ctrl+d", "switch_mode('dashboard')", "Dashboard"),
        ("ctrl+s", "switch_mode('settings')", "Settings"),
        ("full_stop", "toggle_dark", "Toggle Dark Mode"),
        ("question_mark", "switch_mode('help')", "Help")
    ]
    TITLE = "HangoutCore Bot"
    SUB_TITLE = "Created By Lino"
    MODES = {
        "loading": appLoadingScreen,
        "dashboard": appDashboardScreen,
        "settings": appSettingsScreen,
        "help": appHelpScreen
    }
    def action_toggle_dark(self) -> None:
        self.dark = not self.dark
        
    def on_mount(self) -> None:
        # pass
        self.switch_mode('loading')
    
    async def on_ready(self) -> None:
        # pass
        if self.current_mode == 'loading':
            await asyncio.sleep(5)
            self.switch_mode('dashboard')
        
    # def on_key(self, event: events.Key) -> None:
    #     self.query_one(RichLog).write(event)
    
    