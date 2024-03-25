import numpy as np

from textual.app import App

from ..prover import Prover

from .opening import Opening
from .editor import Editor

class Rem(App):
    MODES = {
        "opening" : Opening,
        "editor" : Editor
    }
    def set_opts(self, opts:dict[str, np.ndarray]):
        self.opts = opts

    def on_mount(self) -> None:
        self.switch_mode("opening")


def app_run(opts: dict[str, np.ndarray]):
    rem = Rem()
    rem.set_opts(opts)
    rem.run()