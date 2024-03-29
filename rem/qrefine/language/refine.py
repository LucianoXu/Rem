
from .ast import *

from copy import deepcopy

from .semantics.assertion import wlp

#############################################################
# the refinement rules                                      #
#############################################################


def wlp_check(pres: AstPres, SRefined: QProgAst, env: Env) -> None:
    '''
        == Refinement Rule ==
        ```
            P ⊑ wlp.S.Q
            ------------
            [P, Q] ⊑ S
        ```

        It checks the weakest liberal precondition.
        (it is in the semantics level)
    '''
    if not pres.P.eval(env).iqopt <= wlp(SRefined, pres.Q.eval(env).iqopt, env):
        msg = "Refinement failed. The relation P <= wlp.S.Q is not satisfied for: \n"
        msg += "P = \n\t" + str(pres.P) + "\n"
        msg += "Q = \n\t" + str(pres.Q) + "\n"
        msg += "S = \n" + SRefined.prefix_str("\t") + "\n"
        raise ValueError(msg)
    
    pres.SRefined = SRefined

def weaken_pre(pres: AstPres, R: EIQOptAbstract, env: Env) -> None:
    '''
    == Refinement Rule ==
    ```
        P ⊑ R
        ----------------
        [P, Q] ⊑ [R, Q]
    ```
    '''
    R.type_checking(IQOptType())
    if not pres.P.eval(env).iqopt <= R.eval(env).iqopt:
        msg = "Refinement failed. The relation P ⊑ R is not satisfied for: \n"
        msg += "P = \n\t" + str(pres.P) + "\n"
        msg += "R = \n\t" + str(R) + "\n"
        raise ValueError(msg)
    
    pres.SRefined = AstPres(R, pres.Q)



def strengthen_post(pres: AstPres, R: EIQOptAbstract, env: Env) -> None:
    '''
    == Refinement Rule ==
    ```
        R ⊑ Q
        ----------------
        [P, Q] ⊑ [P, R]
    ```
    '''
    R.type_checking(IQOptType())
    if not R.eval(env).iqopt <= pres.Q.eval(env).iqopt:
        msg = "Refinement failed. The relation R ⊑ Q is not satisfied for: \n"
        msg += "R = \n\t" + str(R) + "\n"
        msg += "Q = \n\t" + str(pres.Q) + "\n"
        raise ValueError(msg)
    
    pres.SRefined = AstPres(pres.P, R)



def rule_seq_break(pres: AstPres, middle: EIQOptAbstract, env: Env) -> None:
    '''
    == Refinement Rule == 
    ```
        -----------------------
        [P, Q] ⊑ [P, R]; [R, Q]
    ```
    '''
    middle.type_checking(IQOptType())

    pres.SRefined = AstSeq(
        AstPres(pres.P, middle),
        AstPres(middle, pres.Q)
    )

def rule_if(pres: AstPres, R : EIQOptAbstract, env: Env) -> None:
    '''
    == Refinement Rule == 
    ```
        ---------------------------------------------------
        [P, Q] ⊑ if R then [R ⋒ P,Q] else [R^⊥ ⋒ P, Q] end
    ```
    '''
    R.type_checking(IQOptType())

    S1 = AstPres(
        EIQOptSasakiConjunct(R, pres.P),
        pres.Q
    )
    S0 = AstPres(
        EIQOptSasakiConjunct(EIQOptComplement(R), pres.P),
        pres.Q
    )
    pres.SRefined = AstIf(R, S1, S0)

def rule_while(pres: AstPres, R : EIQOptAbstract, Inv : EIQOptAbstract, env: Env) -> None:
    '''
    == Refinement Rule == 
    ```
        P ⊑ Inv
        R^⊥ ⋒ Inv ⊑ Q
        -------------------------------------------------
        [P, Q] ⊑ while R do [R ⋒ Inv, Inv] end
    ```
    '''
    R.type_checking(IQOptType())
    Inv.type_checking(IQOptType())

    if not pres.P.eval(env).iqopt <= Inv.eval(env).iqopt:
        msg = "Refinement failed. The relation P <= Inv is not satisfied for: \n"
        msg += "P = \n\t" + str(pres.P) + "\n"
        msg += "Inv = \n\t" + str(Inv) + "\n"
        raise ValueError(msg)
    
    post = EIQOptSasakiConjunct(EIQOptComplement(R), Inv)
    
    if not post.eval(env).iqopt <= pres.Q.eval(env).iqopt:
        msg = "Refinement failed. The relation R^⊥ ⋒ Inv <= Q is not satisfied for: \n"
        msg += "R = \n\t" + str(R) + "\n"
        msg += "Inv = \n\t" + str(Inv) + "\n"
        msg += "Q = \n\t" + str(pres.Q) + "\n"
        raise ValueError(msg)

    pres.SRefined = AstWhile(
        R, 
        AstPres(
            EIQOptSasakiConjunct(R, Inv),
            Inv
        )
    )



