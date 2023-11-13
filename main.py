import numpy as np
from quire import quire_server, predefined
opts = { "Rz" : predefined.Rz(np.arccos(3/5)) }
quire_server("./examples/sec7", "./output", opts)