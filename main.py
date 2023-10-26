
import numpy as np

import qpv2
from qpv2 import *

from qplcomp.qval import predefined
from qplcomp import QOpt, Env

from qplcomp.qexpr.eqopt import EQOpt

if __name__ == "__main__":
    
    opts = {
        "Rztheta" : predefined.Rz(np.arccos(3/5))
    }

    qpv2_server("./code", "output.txt", opts)