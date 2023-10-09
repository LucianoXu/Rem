'''
The (finite step) forward calculation of this language.
'''
from typing import Tuple


from .language import *
import numpy as np
from .qplcomp import QOpt, IQOpt, QSOpt, IQSOpt

P0 = QOpt(np.array([[1., 0.], [0., 0.]]))
E10 = QOpt(np.array([[0., 1.], [0., 0.]]))
ESet0 = QSOpt([P0, E10])

def calc(prog : Ast, rho : IQOpt, step : int) -> Tuple[IQOpt, int]:
    '''
    Calculate the execution result of program `prog` on input state `rho`. It is limited to `step` steps.

    Returns: `Tuple[IQOpt, int]`, the first element is the result, and the second element is the remained step count.
    '''
    # check whether the program can be calculated
    if not prog.definite:
        raise ValueError("This program is not definite therefore cannot calculate.")
    
    # check whether rho is a partial density
    if not rho.qval.is_pdo:
        raise ValueError("The input rho is not a partial density operator.")
    
    # return zero is step is empty
    if step == 0:
        return IQOpt.zero(), 0

    if isinstance(prog, AstAbort):
        return IQOpt.zero(), step - 1
    elif isinstance(prog, AstSkip):
        return rho, step - 1
    elif isinstance(prog, AstInit):
        res = rho
        for q in prog.qvar:
            IESet0 = IQSOpt(ESet0, QVar([q]))
            res = IESet0.apply_rho(res)
        return res, step - 1
    elif isinstance(prog, AstUnitary):
        U = prog.U
        return U @ rho @ U.dagger(), step - 1
    elif isinstance(prog, AstAssert):
        P = prog.P
        return P @ rho @ P, step - 1
    elif isinstance(prog, AstSeq):
        rho1, step1 = calc(prog.S0, rho, step)
        return calc(prog.S1, rho1, step1)
    else:
        raise Exception()