import numpy as np
from quire import quire_server, predefined

# this is for example 'sec5_2'
opts = { "Rz" : predefined.Rz(np.arccos(3/5)) }

quire_server("./examples/sec7", "./output", opts)