import numpy as np

from textual.app import App

from .opening import Opening
from .editor import Editor

class Rem(App):

    MODES = {
        "opening" : Opening,
        "editor" : Editor
    }

    def on_mount(self) -> None:

        self.switch_mode("opening")

def app_run(opts: dict[str, np.ndarray]):
    rem = Rem()
    rem.run()