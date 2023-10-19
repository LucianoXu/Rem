
import numpy as np

import qpv2
from qpv2 import *

from qplcomp.qval import predefined
from qplcomp import QOpt, Env

from qplcomp.qexpr.eqopt import EQOpt

opts = {
    "Rztheta" : predefined.Rz(np.arccos(3/5))
}

qpv("./code", "output.txt", opts)