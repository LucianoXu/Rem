from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Footer, Placeholder

from time import time

from textual.app import ComposeResult, RenderableType # type: ignore
from textual.containers import Container
from textual.renderables.gradient import LinearGradient
from textual.widgets import Static, Button

from .colors import *

COLORS = [
    rem_blue,
    "white",
    rem_pink,
]
STOPS = [(i / (len(COLORS) - 1), color) for i, color in enumerate(COLORS)]


class Splash(Container):
    """Custom widget that extends Container."""

    DEFAULT_CSS = """
    Splash {
        align: center middle;
    }
    Static {
        width: 40;
        padding: 2 4;
    }
    """

    def on_mount(self) -> None:
        self.auto_refresh = 1 / 30

    def compose(self) -> ComposeResult:
        yield Static("Rem\nQuantum Program Refinement", id="title")
        yield Button("Editor", id="to_editor")
        yield Button("Handbook", id="to_handbook")
        # yield Static("created with ♥")

    def render(self) -> RenderableType:
        return LinearGradient(time(), STOPS)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id
        if button_id == "to_editor":
            self.app.switch_mode("editor")
        elif button_id == "to_handbook":
            self.app.switch_mode("handbook")
        

class Opening(Screen):
    def compose(self) -> ComposeResult:
        yield Splash()