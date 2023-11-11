import numpy as np
from qpv2 import qpv2_server, predefined
opts = { "Rz" : predefined.Rz(np.arccos(3/5)) }
qpv2_server("./examples/sec7", "./output", opts)