

from ..prover import Prover

import numpy as np


# the prover used by the App
prover : Prover = Prover({})

# the operators for the prover engine
operators : dict[str, np.ndarray] = {}

def set_opts(opts:dict[str, np.ndarray]):
    global operators
    operators = opts