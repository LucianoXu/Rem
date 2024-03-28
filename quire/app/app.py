import numpy as np

from textual.app import App

from qplcomp import prepare_env


from .opening import Opening
from .editor import Editor

class Rem(App):

    MODES = {
        "opening" : Opening,
        "editor" : Editor
    }

    def on_mount(self) -> None:

        # prepare the quantum operator environment
        prepare_env()
        self.switch_mode("opening")

from .backends import set_opts

def app_run(opts: dict[str, np.ndarray]):
    rem = Rem()
    set_opts(opts)
    rem.run()