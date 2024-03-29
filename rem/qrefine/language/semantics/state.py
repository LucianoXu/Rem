'''
The (finite step) forward calculation of this language.
'''


from .. import *
import numpy as np
from ....qplcomp import QOpt, IQOpt, QSOpt, IQSOpt

from ...error import ValueError

P0 = QOpt(np.array([[1., 0.], [0., 0.]]))
E10 = QOpt(np.array([[0., 1.], [0., 0.]]))
ESet0 = QSOpt([P0, E10])

def calc(prog : QProgAst, rho : IQOpt, env: Env) -> IQOpt:
    '''
    The method for initiating a execution calculation.
    Check of program and input state is implemented here.
    '''

    rho.rho_extend = True

    extracted_prog = prog.extract

    # check whether the program can be calculated
    if not extracted_prog.definite(env):
        raise ValueError(f"The program\n\n{extracted_prog}\n\nis not definite therefore cannot calculate.")
    
    # check whether rho is a partial density
    if not rho.qval.is_pdo:
        raise ValueError("The input rho is not a partial density operator.")
    
    return calc_iter(extracted_prog, rho, env)
    


def calc_iter(prog : QProgAst, rho : IQOpt, env: Env) -> IQOpt:
    '''
    Calculate the execution result of program `prog` on input state `rho`.

    Returns: `IQOpt`, the result of execution.
    '''
    rho.rho_extend = True

    # return zero if the input is zero
    if rho == IQOpt.zero(is_rho=True):
        return IQOpt.zero(is_rho=True)

    if isinstance(prog, AstSubprog):
        return calc_iter(prog.eval(env), rho, env)
    
    elif isinstance(prog, AstAbort):
        return IQOpt.zero(is_rho=True)
    
    elif isinstance(prog, AstSkip):
        return rho
    
    elif isinstance(prog, AstInit):
        res = rho
        for q in prog.eqvar.eval(env).qvar:
            IESet0 = IQSOpt(ESet0, QVar([q]))
            res = IESet0.apply(res)
            res.rho_extend = True
        return res
    
    elif isinstance(prog, AstUnitary):
        U = prog.U.eval(env).iqopt
        return U @ rho @ U.dagger()
    
    elif isinstance(prog, AstAssert):
        P = prog.P.eval(env).iqopt
        return P @ rho @ P
    
    elif isinstance(prog, AstPres):
        if prog.SRefined is None:
            raise Exception()
        return calc_iter(prog.SRefined, rho, env)
    
    elif isinstance(prog, AstSeq):
        rho1 = calc_iter(prog.S0, rho, env)
        return calc_iter(prog.S1, rho, env)
    
    elif isinstance(prog, AstProb):
        rho_0 = calc_iter(prog.S0, rho, env)
        rho_1 = calc_iter(prog.S1, rho, env)
        return (1-prog.p) * rho_0 + prog.p * rho_1
    
    elif isinstance(prog, AstIf):
        # branch of res == 1
        P = prog.P.eval(env).iqopt
        rho_1 = calc_iter(prog.S1, P @ rho @ P, env)
        
        # branch of res == 0
        P_comp = ~ P
        rho_0 = calc_iter(prog.S0, P_comp @ rho @ P_comp, env)

        return rho_1 + rho_0
    
    elif isinstance(prog, AstWhile):
        P = prog.P.eval(env).iqopt
        P_comp = ~ P

        # branch of `break`
        rho_break = P_comp @ rho @ P_comp

        # branch of `continue`
        new_prog = AstSeq(prog.S, prog)
        rho_continue = calc_iter(new_prog, P @ rho @ P, env)

        return rho_break + rho_continue
    
    else:
        raise Exception()