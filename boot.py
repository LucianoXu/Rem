import numpy as np

from rem import app_run, predefined

# this is for example 'sec5_1'
opts = { "Rz" : predefined.Rz(np.arccos(3/5)) }

if __name__ == "__main__":
    app_run(opts)