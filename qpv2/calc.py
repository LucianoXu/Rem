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

def calc(prog : Ast, rho : IQOpt) -> IQOpt:
    '''
    The method for initiating a execution calculation.
    Check of program and input state is implemented here.
    '''

    rho.rho_extend = True

    extracted_prog = prog.extract

    # check whether the program can be calculated
    if not extracted_prog.definite:
        raise ValueError("This program is not definite therefore cannot calculate.")
    
    # check whether rho is a partial density
    if not rho.qval.is_pdo:
        raise ValueError("The input rho is not a partial density operator.")
    
    return calc_iter(extracted_prog, rho)
    


def calc_iter(prog : Ast, rho : IQOpt) -> IQOpt:
    '''
    Calculate the execution result of program `prog` on input state `rho`.

    Returns: `IQOpt`, the result of execution.
    '''
    rho.rho_extend = True

    # return zero if the input is zero
    if rho == IQOpt.zero(is_rho=True):
        return IQOpt.zero(is_rho=True)

    if isinstance(prog, AstAbort):
        return IQOpt.zero(is_rho=True)
    
    elif isinstance(prog, AstSkip):
        return rho
    
    elif isinstance(prog, AstInit):
        res = rho
        for q in prog.qvar:
            IESet0 = IQSOpt(ESet0, QVar([q]))
            res = IESet0.apply(res)
        return res
    
    elif isinstance(prog, AstUnitary):
        U = prog.U
        return U @ rho @ U.dagger()
    
    elif isinstance(prog, AstAssert):
        P = prog.P
        return P @ rho @ P
    
    elif isinstance(prog, AstSeq):
        rho1 = calc_iter(prog.S0, rho)
        return calc_iter(prog.S1, rho1)
    
    elif isinstance(prog, AstProb):
        rho_0 = calc_iter(prog.S0, rho)
        rho_1 = calc_iter(prog.S1, rho)
        return prog.p * rho_0 + (1 - prog.p) * rho_1
    
    elif isinstance(prog, AstIf):
        # branch of res == 1
        P = prog.P
        rho_1 = calc_iter(prog.S1, P @ rho @ P)
        
        # branch of res == 0
        P_comp = ~ P
        rho_0 = calc_iter(prog.S0, P_comp @ rho @ P_comp)

        return rho_1 + rho_0
    
    elif isinstance(prog, AstWhile):
        P = prog.P
        P_comp = ~ P

        # branch of `break`
        rho_break = P_comp @ rho @ P_comp

        # branch of `continue`
        new_prog = AstSeq(prog.S, prog)
        rho_continue = calc_iter(new_prog, P @ rho @ P)

        return rho_break + rho_continue
    
    else:
        raise Exception()