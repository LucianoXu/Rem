import numpy as np

from textual.app import App

from .opening import Opening
from .editor import Editor
from .handbook import Handbook

class Rem(App):

    CSS_PATH = "Rem.tcss"

    MODES = {
        "opening" : Opening,
        "editor" : Editor,
        "handbook" : Handbook,
    }

    def on_mount(self) -> None:

        self.switch_mode("opening")
        self.dark = False

def app_run(opts: dict[str, np.ndarray]):
    rem = Rem()
    rem.run()