from __future__ import annotations
from typing import Type

from qplcomp import IQOpt, QVar, IQOpt
from qplcomp.env import TypedTerm, Var, Types

from qplcomp.qexpr.eiqopt import *
from qplcomp.qexpr.eiqopt import EIQOpt, Env

from ..error import ValueError

INDENT = "  "

class QWhileType(Types, ABC):
    def __str__(self) -> str:
        return "QWhile"

class QWhileAst(TypedTerm):

    def __init__(self):
        super().__init__(QWhileType())

    @abstractmethod
    def eval(self, env: Env) -> QWhileAst:
        pass

    @property
    def definite(self) -> bool:
        '''
        Whether this program is definite. In other words, whether there is no prescription statements in this program.
        '''
        raise NotImplementedError()

    
    def prefix_str(self, prefix = "") -> str:
        raise NotImplementedError()

    def __str__(self) -> str:
        return self.prefix_str()
    
    @property
    def extract(self) -> QWhileAst:
        '''
        Extract the refinement result as a program syntax (without refinement proofs).
        '''
        raise NotImplementedError()
    
    def get_prescription(self) -> list[AstPres]:
        '''
        Return the unsolved prescriptions.
        '''
        raise NotImplementedError()
    
    def wlp(self, post : IQOpt, env: Env) -> IQOpt:
        '''
        Calculate the weakest liberal precondition.
        '''
        raise NotImplementedError()
    
    def sp_ex(self, pre : EIQOpt, env: Env) -> EIQOpt:
        '''
        Calculate the strongest postcondition (expression).
        '''
        raise NotImplementedError()


#####################################################################
# different program structures

class AstSubprog(QWhileAst):
    def __init__(self, subprog : Var):
        super().__init__()
        subprog.type_checking(QWhileType())

        self.subprog = subprog

    def eval(self, env: Env) -> QWhileAst:
        east = self.subprog.eval(env)
        if not isinstance(east, QWhileAst):
            raise ValueError("The variable '" + str(self.subprog) + "' is not a program.")
        return east.eval(env)

    @property
    def definite(self) -> bool:
        return False

    
    def prefix_str(self, prefix = "") -> str:
        return prefix + "proc " + str(self.subprog)

    
    @property
    def extract(self) -> QWhileAst:
        return self
    
    def get_prescription(self) -> list[AstPres]:
        return []
    
    def wlp(self, post : IQOpt, env: Env) -> IQOpt:
        return self.eval(env).wlp(post, env)
    
    def sp_ex(self, pre: EIQOpt, env: Env) -> EIQOpt:
        return self.eval(env).sp_ex(pre, env)


class AstAbort(QWhileAst):
    def __init__(self):
        super().__init__()

    def eval(self, env: Env) -> QWhileAst:
        return self

    @property
    def definite(self) -> bool:
        return True
    
    def prefix_str(self, prefix="") -> str:
        return prefix + "abort"
    
    @property
    def extract(self) -> QWhileAst:
        return self
    
    def get_prescription(self) -> list[AstPres]:
        return []

    def wlp(self, post: IQOpt, env: Env) -> IQOpt:
        return IQOpt.identity(False)


class AstSkip(QWhileAst):
    def __init__(self):
        super().__init__()

    def eval(self, env: Env) -> QWhileAst:
        return self

    @property
    def definite(self) -> bool:
        return True
    
    def prefix_str(self, prefix="") -> str:
        return prefix + "skip"
    
    @property
    def extract(self) -> QWhileAst:
        return self

    def get_prescription(self) -> list[AstPres]:
        return []
    
    def wlp(self, post: IQOpt, env: Env) -> IQOpt:
        return post

class AstInit(QWhileAst):
    def __init__(self, eqvar : EQVar):
        super().__init__()
        eqvar.type_checking(QVarType())
        self.eqvar = eqvar

    def eval(self, env: Env) -> QWhileAst:
        return self

    @property
    def definite(self) -> bool:
        return True
    
    def prefix_str(self, prefix="") -> str:
        return prefix + str(self.eqvar) + ":=0"

    @property
    def extract(self) -> QWhileAst:
        return self

    def get_prescription(self) -> list[AstPres]:
        return []
    
    def wlp(self, post: IQOpt, env: Env) -> IQOpt:
        return post.initwlp(self.eqvar.eval(env).qvar)

    
class AstUnitary(QWhileAst):
    def __init__(self, U : EIQOptAbstract):
        super().__init__()
        U.type_checking(IQOptType())

        self.U = U

    def eval(self, env: Env) -> QWhileAst:
        
        # check whether this is a unitary
        if not self.U.eval(env).iqopt.qval.is_unitary:
            raise ValueError("The operator '" + str(self.U) + "' for unitary statement is not unitary.")
        
        return self

    @property
    def definite(self) -> bool:
        return True
    
    def prefix_str(self, prefix="") -> str:
        return prefix + str(self.U)

    @property
    def extract(self) -> QWhileAst:
        return self

    def get_prescription(self) -> list[AstPres]:
        return []

    def wlp(self, post: IQOpt, env: Env) -> IQOpt:
        U = self.U.eval(env).iqopt
        return U.dagger() @ post @ U
    
class AstAssert(QWhileAst):
    def __init__(self, P : EIQOptAbstract):
        super().__init__()
        P.type_checking(IQOptType())

        self.P = P

    def eval(self, env: Env) -> QWhileAst:
        
        # check whether this is a projector
        if not self.P.eval(env).iqopt.qval.is_projector:
            raise ValueError("The operator '" + str(self.P) + "' for assertion statement is not projective.")
        
        return self

    @property
    def definite(self) -> bool:
        return True
    
    def prefix_str(self, prefix="") -> str:
        return prefix + "assert " + str(self.P)
    
    @property
    def extract(self) -> QWhileAst:
        return self

    def get_prescription(self) -> list[AstPres]:
        return []

    def wlp(self, post: IQOpt, env: Env) -> IQOpt:
        return self.P.eval(env).iqopt.Sasaki_imply(post)

    

class AstPres(QWhileAst):
    def __init__(self, P : EIQOptAbstract, Q : EIQOptAbstract, SRefined: QWhileAst|None = None):
        '''
        This `SRefined` attribute can refer to the subsequent refined programs for this program. If `None`, then the current program is used.
        '''
        super().__init__()
        self.SRefined : QWhileAst | None = SRefined

        P.type_checking(IQOptType())
        Q.type_checking(IQOptType())

        
        self.P = P
        self.Q = Q

    def eval(self, env: Env) -> QWhileAst:
        # check whether P and Q are projectors
        if not self.P.eval(env).iqopt.qval.is_projector:
            raise ValueError("The operator '" + str(self.P) + "' for assertion statement is not projective.")
        if not self.Q.eval(env).iqopt.qval.is_projector:
            raise ValueError("The operator '" + str(self.Q) + "' for assertion statement is not projective.")
        
        return self
        

    ############################################################
    # Refinement Steps


    def refine_wlp(self, SRefined: QWhileAst, env: Env) -> None:
        '''
        == Refinement Rule ==
        ```
            P ⊑ wlp.S.Q
            ------------
            [P, Q] ⊑ S
        ```

        It checks the weakest liberal precondition.
        '''
        if not self.P.eval(env).iqopt <= SRefined.wlp(self.Q.eval(env).iqopt, env):
            msg = "Refinement failed. The relation P <= wlp.S.Q is not satisfied for: \n"
            msg += "P = \n\t" + str(self.P) + "\n"
            msg += "Q = \n\t" + str(self.Q) + "\n"
            msg += "S = \n" + SRefined.prefix_str("\t") + "\n"
            raise ValueError(msg)
        
        self.SRefined = SRefined

    def refine_weaken_pre(self, R : EIQOptAbstract, env: Env) -> None:
        '''
        == Refinement Rule ==
        ```
            P ⊑ R
            ----------------
            [P, Q] ⊑ [R, Q]
        ```
        '''
        R.type_checking(IQOptType())
        if not self.P.eval(env).iqopt <= R.eval(env).iqopt:
            msg = "Refinement failed. The relation P ⊑ R is not satisfied for: \n"
            msg += "P = \n\t" + str(self.P) + "\n"
            msg += "R = \n\t" + str(R) + "\n"
            raise ValueError(msg)
        
        self.SRefined = AstPres(R, self.Q)


    def refine_strengthen_post(self, R : EIQOptAbstract, env: Env) -> None:
        '''
        == Refinement Rule ==
        ```
            R ⊑ Q
            ----------------
            [P, Q] ⊑ [P, R]
        ```
        '''
        R.type_checking(IQOptType())
        if not R.eval(env).iqopt <= self.Q.eval(env).iqopt:
            msg = "Refinement failed. The relation R ⊑ Q is not satisfied for: \n"
            msg += "R = \n\t" + str(R) + "\n"
            msg += "Q = \n\t" + str(self.Q) + "\n"
            raise ValueError(msg)
        
        self.SRefined = AstPres(self.P, R)


    
    def refine_seq_break(self, middle: EIQOptAbstract) -> None:
        '''
        == Refinement Rule == 
        ```
            -----------------------
            [P, Q] ⊑ [P, R]; [R, Q]
        ```
        '''
        middle.type_checking(IQOptType())

        self.SRefined = AstSeq(
            AstPres(self.P, middle),
            AstPres(middle, self.Q)
        )

    def refine_if(self, R : EIQOptAbstract) -> None:
        '''
        == Refinement Rule == 
        ```
            ---------------------------------------------------
            [P, Q] ⊑ if R then [R ⋒ P,Q] else [R^⊥ ⋒ P, Q] end
        ```
        '''
        R.type_checking(IQOptType())

        S1 = AstPres(
            EIQOptSasakiConjunct(R, self.P),
            self.Q
        )
        S0 = AstPres(
            EIQOptSasakiConjunct(EIQOptComplement(R), self.P),
            self.Q
        )
        self.SRefined = AstIf(R, S1, S0)

    def refine_while(self, R : EIQOptAbstract, Inv : EIQOptAbstract, env: Env) -> None:
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

        if not self.P.eval(env).iqopt <= Inv.eval(env).iqopt:
            msg = "Refinement failed. The relation P <= Inv is not satisfied for: \n"
            msg += "P = \n\t" + str(self.P) + "\n"
            msg += "Inv = \n\t" + str(Inv) + "\n"
            raise ValueError(msg)
        
        post = EIQOptSasakiConjunct(EIQOptComplement(R), Inv)
        
        if not post.eval(env).iqopt <= self.Q.eval(env).iqopt:
            msg = "Refinement failed. The relation R^⊥ ⋒ Inv <= Q is not satisfied for: \n"
            msg += "R = \n\t" + str(R) + "\n"
            msg += "Inv = \n\t" + str(Inv) + "\n"
            msg += "Q = \n\t" + str(self.Q) + "\n"
            raise ValueError(msg)

        self.SRefined = AstWhile(
            R, 
            AstPres(
                EIQOptSasakiConjunct(R, Inv),
                Inv
            )
        )



    #############################################################

    @property
    def definite(self) -> bool:
        if self.SRefined is None:
            return False
        else:
            return self.SRefined.definite
        
    def pres_str(self) -> str:
        return "< " + str(self.P) + ", " + str(self.Q) + " >"
    
    def prefix_str(self, prefix="") -> str:
        res = prefix + self.pres_str()
        if self.SRefined is None:
            return res
        else:
            res += "\n" + prefix + INDENT + "<= {\n"
            res += self.SRefined.prefix_str(prefix + INDENT) + "\n"
            res += prefix + "}"
            return res


    @property
    def extract(self) -> QWhileAst:
        if self.SRefined is not None:
            return self.SRefined.extract
        else:
            return self

    def get_prescription(self) -> list[AstPres]:
        if self.SRefined is not None:
            return self.SRefined.get_prescription()
        else:
            return [self]
    
    def wlp(self, post: IQOpt, env: Env) -> IQOpt:
        if post == IQOpt.identity(False):
            return IQOpt.identity(False)
        elif self.Q.eval(env).iqopt <= post:
            return self.P.eval(env).iqopt
        else:
            return IQOpt.zero(False)


class AstSeq(QWhileAst):
    def __init__(self, S0 : QWhileAst, S1 : QWhileAst):
        super().__init__()

        # restructure the sequential composition, so that it is always associated to the right
        if isinstance(S0, AstSeq):
            S0, S1 = S0.S0, AstSeq(S0.S1, S1)

        self.S0 = S0
        self.S1 = S1

    def eval(self, env: Env) -> QWhileAst:
        return AstSeq(
            self.S0.eval(env),
            self.S1.eval(env)
        )

    @property
    def definite(self) -> bool:
        return self.S0.definite and self.S1.definite
    
    def prefix_str(self, prefix="") -> str:
        return self.S0.prefix_str(prefix) + ";\n" + self.S1.prefix_str(prefix)
    
    @property
    def extract(self) -> QWhileAst:
        return AstSeq(self.S0.extract, self.S1.extract)
    
    def get_prescription(self) -> list[AstPres]:
        return self.S0.get_prescription() + self.S1.get_prescription()
    
    def wlp(self, post: IQOpt, env: Env) -> IQOpt:
        return self.S0.wlp(self.S1.wlp(post, env), env)
    
class AstProb(QWhileAst):
    def __init__(self, S0 : QWhileAst, S1 : QWhileAst, p : float):
        super().__init__()
        self.S0 = S0
        self.S1 = S1
        
        if p < 0 or p > 1:
            raise ValueError("Invalid probability: '" + str(p) + "'.")
        
        self.p = p

    def eval(self, env: Env) -> QWhileAst:
        return AstProb(
            self.S0.eval(env),
            self.S1.eval(env),
            self.p
        )


    @property
    def definite(self) -> bool:
        return self.S0.definite and self.S1.definite
    
    def prefix_str(self, prefix="") -> str:
        res = prefix + "(\n" + self.S0.prefix_str(prefix + INDENT) + "\n"
        res += prefix + "[⊕ " + str(self.p) +"]\n"
        res += self.S1.prefix_str(prefix + INDENT) + "\n"
        res += prefix + ")"
        return res
    
    @property
    def extract(self) -> QWhileAst:
        return AstProb(self.S0.extract, self.S1.extract, self.p)
        
    def get_prescription(self) -> list[AstPres]:
        return self.S0.get_prescription() + self.S1.get_prescription()

    def wlp(self, post: IQOpt, env: Env) -> IQOpt:
        return self.S0.wlp(post, env) & self.S1.wlp(post, env)
    
class AstIf(QWhileAst):
    def __init__(self, P : EIQOptAbstract, S1 : QWhileAst, S0 : QWhileAst):
        super().__init__()
        P.type_checking(IQOptType())

        
        self.P = P
        self.S1 = S1
        self.S0 = S0
    
    def eval(self, env: Env) -> QWhileAst:
        # check whether P is a projector
        if not self.P.eval(env).iqopt.qval.is_projector:
            raise ValueError("The operator '" + str(self.P) + "' for assertion statement is not projective.")
        
        return AstIf(
            self.P.eval(env),
            self.S1.eval(env),
            self.S0.eval(env))



    @property
    def definite(self) -> bool:
        return self.S1.definite and self.S0.definite
    
    def prefix_str(self, prefix="") -> str:
        res = prefix + "if " + str(self.P) + " then\n"
        res += self.S1.prefix_str(prefix + INDENT) + "\n"
        res += prefix + "else\n"
        res += self.S0.prefix_str(prefix + INDENT) + "\n"
        res += prefix + "end"
        return res

    @property
    def extract(self) -> QWhileAst:
        return AstIf(self.P, self.S1.extract, self.S0.extract)

    def get_prescription(self) -> list[AstPres]:
        return self.S1.get_prescription() + self.S0.get_prescription()
    
    def wlp(self, post: IQOpt, env: Env) -> IQOpt:
        P = self.P.eval(env).iqopt
        return P.Sasaki_imply(self.S1.wlp(post, env)) &\
              (~ P).Sasaki_imply(self.S0.wlp(post, env))

class AstWhile(QWhileAst):
    def __init__(self, P : EIQOptAbstract, S : QWhileAst):
        super().__init__()
        P.type_checking(IQOptType())

        self.P = P
        self.S = S

    def eval(self, env: Env) -> QWhileAst:
        # check whether P is a projector
        if not self.P.eval(env).iqopt.qval.is_projector:
            raise ValueError("The operator '" + str(self.P) + "' for assertion statement is not projective.")
        
        return AstWhile(
            self.P.eval(env),
            self.S.eval(env)
        )

    
    @property
    def definite(self) -> bool:
        return self.S.definite
    
    def prefix_str(self, prefix="") -> str:
        res = prefix + "while " + str(self.P) + " do\n"
        res += self.S.prefix_str(prefix + INDENT) + "\n"
        res += prefix + "end"
        return res

    @property
    def extract(self) -> QWhileAst:
        return AstWhile(self.P, self.S.extract)

    def get_prescription(self) -> list[AstPres]:
        return self.S.get_prescription()
    
    def wlp(self, post: IQOpt, env: Env) -> IQOpt:
        '''
        This will terminate because the lattice has finite height.
        '''
        flag = True
        Rn = IQOpt.identity(False)
        Rn_1 = IQOpt.identity(False)

        P = self.P.eval(env).iqopt

        # this is guaranteed to terminate
        while flag:
            Rn = Rn_1
            Rn_1 = P.Sasaki_imply(self.S.wlp(Rn, env)) & (~ P).Sasaki_imply(post)

            flag = not Rn == Rn_1

        return Rn