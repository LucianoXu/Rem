from ..ast import *

def wlp(prog: QProgAst, post: IQOpt, env: Env) -> IQOpt:
    '''
    Compute the weakest liberal precondition.
    '''
    if isinstance(prog, AstSubprog):
        return wlp(prog.eval(env), post, env)
    
    elif isinstance(prog, AstAbort):
        return IQOpt.identity(False)
    
    elif isinstance(prog, AstSkip):
        return post
    
    elif isinstance(prog, AstInit):
        return post.initwlp(prog.eqvar.eval(env).qvar)
    
    elif isinstance(prog, AstUnitary):
        U = prog.U.eval(env).iqopt
        return U.dagger() @ post @ U
    
    elif isinstance(prog, AstAssert):
        return prog.P.eval(env).iqopt.Sasaki_imply(post)
    
    elif isinstance(prog, AstPres):
        if post == IQOpt.identity(False):
            return IQOpt.identity(False)
        elif prog.Q.eval(env).iqopt <= post:
            return prog.P.eval(env).iqopt
        else:
            return IQOpt.zero(False)
        
    elif isinstance(prog, AstSeq):
        return wlp(prog.S0, wlp(prog.S1, post, env), env)
    
    elif isinstance(prog, AstProb):
        return wlp(prog.S0, post, env) & wlp(prog.S1, post, env)
    
    elif isinstance(prog, AstIf):
        P = prog.P.eval(env).iqopt
        return P.Sasaki_imply(wlp(prog.S1, post, env)) &\
              (~ P).Sasaki_imply(wlp(prog.S0, post, env))
    
    elif isinstance(prog, AstWhile):
        '''
        This will terminate because the lattice has finite height.
        '''
        flag = True
        Rn = IQOpt.identity(False)
        Rn_1 = IQOpt.identity(False)

        P = prog.P.eval(env).iqopt

        # this is guaranteed to terminate
        while flag:
            Rn = Rn_1
            Rn_1 = P.Sasaki_imply(wlp(prog.S, Rn, env)) & (~ P).Sasaki_imply(post)

            flag = not Rn == Rn_1

        return Rn    
    

    else:
        raise ValueError(f"Unsupported type: {prog}")


def sp_ex(prog: QProgAst, pre : EIQOpt, env: Env) -> EIQOpt:
    '''
    Calculate the strongest postcondition (expression).
    '''
    
    if isinstance(prog, AstSubprog):
        return sp_ex(prog.eval(env), pre, env)
    
    else:
        raise ValueError(f"Unsupported type: {prog}")