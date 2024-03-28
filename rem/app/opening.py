from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Footer, Placeholder

from time import time

from textual.app import ComposeResult, RenderableType # type: ignore
from textual.containers import Container
from textual.renderables.gradient import LinearGradient
from textual.widgets import Static, Button

COLORS = [
    "#881177",
    "#aa3355",
    "#cc6666",
    "#ee9944",
    "#eedd00",
    "#99dd55",
    "#44dd88",
    "#22ccbb",
    "#00bbcc",
    "#0099cc",
    "#3366bb",
    "#663399",
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
        yield Static("Quantum Program Refinement with Rem")
        yield Button("New File", id="new-file")
        yield Button("Exit", id="exit")

    def render(self) -> RenderableType:
        return LinearGradient(time() * 90, STOPS)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id
        if button_id == "exit":
            self.app.exit()
        elif button_id == "new-file":
            self.app.switch_mode("editor")

class Opening(Screen):
    def compose(self) -> ComposeResult:
        yield Splash()