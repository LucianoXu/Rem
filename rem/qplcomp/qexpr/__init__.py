'''
QPLComp.qexpr
=====

This package provides the data structure and methods for quantum expressions.

A quantum expression is a quantum operator with the corresponding quantum variable. Many methods on the operator level, such as contraction and addition, also exists for quantum expressions. The methods of this package takes care of the details.
'''

from ..qval import qvallib, QOpt, QSOpt
from .eqopt import EQOpt
from .eqso import EQSOpt

from ...mTLC import Env

def prepare_env() -> Env:
    '''
    Append the environment with predefined quantum values.
    '''
    env = Env()
    for key in qvallib:
        val = qvallib[key]
        
        if isinstance(val, QOpt):
            env[key] = EQOpt(val)
        elif isinstance(val, QSOpt):
            env[key] = EQSOpt(val)
        else:
            raise Exception("Unexpected Exception.")
    
    return env