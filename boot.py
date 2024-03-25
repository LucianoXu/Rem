import numpy as np

from quire import app_run

from quire import predefined

# this is for example 'sec5_1'
opts = { "Rz" : predefined.Rz(np.arccos(3/5)) }

if __name__ == "__main__":
    app_run(opts)