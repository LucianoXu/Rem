from __future__ import annotations
from typing import Type

from ...qplcomp import IQOpt, QVar, IQOpt
from ...mTLC.env import TypedTerm, Var, Types

from ...qplcomp.qexpr.eiqopt import *

from ..error import ValueError

INDENT = "  "

class QProgType(Types, ABC):
    def __str__(self) -> str:
        return "QProg"

class QProgAst(TypedTerm):

    def __init__(self):
        super().__init__(QProgType())

    @abstractmethod
    def eval(self, env: Env) -> QProgAst:
        pass

    def definite(self, env: Env) -> bool:
        '''
        Whether this program is definite. In other words, whether there is no prescription statements in this program.
        '''
        raise NotImplementedError()

    
    def prefix_str(self, prefix = "") -> str:
        raise NotImplementedError()

    def __str__(self) -> str:
        return self.prefix_str()
    
    @property
    def extract(self) -> QProgAst:
        '''
        Extract the refinement result as a program syntax (without refinement proofs).
        '''
        raise NotImplementedError()
    
    def get_prescription(self) -> list[AstPres]:
        '''
        Return the unsolved prescriptions.
        '''
        raise NotImplementedError()
    
    

#####################################################################
# different program structures

class AstAbort(QProgAst):
    def __init__(self):
        super().__init__()

    def eval(self, env: Env) -> QProgAst:
        return self

    def definite(self, env: Env) -> bool:
        return True
    
    def prefix_str(self, prefix="") -> str:
        return prefix + "abort"
    
    @property
    def extract(self) -> QProgAst:
        return self
    
    def get_prescription(self) -> list[AstPres]:
        return []


class AstSkip(QProgAst):
    def __init__(self):
        super().__init__()

    def eval(self, env: Env) -> QProgAst:
        return self

    def definite(self, env: Env) -> bool:
        return True
    
    def prefix_str(self, prefix="") -> str:
        return prefix + "skip"
    
    @property
    def extract(self) -> QProgAst:
        return self

    def get_prescription(self) -> list[AstPres]:
        return []
    

class AstInit(QProgAst):
    def __init__(self, eqvar : EQVar):
        super().__init__()
        self.eqvar = eqvar

    def eval(self, env: Env) -> QProgAst:
        return self

    def definite(self, env: Env) -> bool:
        return True
    
    def prefix_str(self, prefix="") -> str:
        return prefix + str(self.eqvar) + ":=0"

    @property
    def extract(self) -> QProgAst:
        return self

    def get_prescription(self) -> list[AstPres]:
        return []
    
    
class AstUnitary(QProgAst):
    def __init__(self, U : EIQOptAbstract):
        super().__init__()

        self.U = U

    def eval(self, env: Env) -> QProgAst:
        
        # check whether this is a unitary
        if not self.U.eval(env).iqopt.qval.is_unitary:
            raise ValueError("The operator '" + str(self.U) + "' for unitary statement is not unitary.")
        
        return self

    def definite(self, env: Env) -> bool:
        return True
    
    def prefix_str(self, prefix="") -> str:
        return prefix + str(self.U) + ";"

    @property
    def extract(self) -> QProgAst:
        return self

    def get_prescription(self) -> list[AstPres]:
        return []

    
class AstAssert(QProgAst):
    def __init__(self, P : EIQOptAbstract):
        super().__init__()

        self.P = P

    def eval(self, env: Env) -> QProgAst:
        
        # check whether this is a projector
        if not self.P.eval(env).iqopt.qval.is_projector:
            raise ValueError("The operator '" + str(self.P) + "' for assertion statement is not projective.")
        
        return self

    def definite(self, env: Env) -> bool:
        return True
    
    def prefix_str(self, prefix="") -> str:
        return prefix + "assert " + str(self.P)
    
    @property
    def extract(self) -> QProgAst:
        return self

    def get_prescription(self) -> list[AstPres]:
        return []

    

class AstPres(QProgAst):
    def __init__(self, P : EIQOptAbstract, Q : EIQOptAbstract, SRefined: QProgAst|None = None):
        '''
        This `SRefined` attribute can refer to the subsequent refined programs for this program. If `None`, then the current program is used.
        '''
        super().__init__()
        self.SRefined : QProgAst | None = SRefined
        
        self.P = P
        self.Q = Q

    def eval(self, env: Env) -> QProgAst:
        # check whether P and Q are projectors
        if not self.P.eval(env).iqopt.qval.is_projector:
            raise ValueError("The operator '" + str(self.P) + "' for assertion statement is not projective.")
        if not self.Q.eval(env).iqopt.qval.is_projector:
            raise ValueError("The operator '" + str(self.Q) + "' for assertion statement is not projective.")
        
        return self
        



    #############################################################

    def definite(self, env: Env) -> bool:
        if self.SRefined is None:
            return False
        else:
            return self.SRefined.definite(env)
        
    def pres_str(self) -> str:
        return "< " + str(self.P) + ", " + str(self.Q) + " >"
    
    def prefix_str(self, prefix="") -> str:
        res = prefix + self.pres_str()
        if self.SRefined is None:
            return res
        else:
            res += "\n" + prefix + INDENT + "<= (\n"
            res += self.SRefined.prefix_str(prefix + INDENT) + "\n"
            res += prefix + ")"
            return res


    @property
    def extract(self) -> QProgAst:
        if self.SRefined is not None:
            return self.SRefined.extract
        else:
            return self

    def get_prescription(self) -> list[AstPres]:
        if self.SRefined is not None:
            return self.SRefined.get_prescription()
        else:
            return [self]
    


class AstSeq(QProgAst):
    def __init__(self, S0 : QProgAst, S1 : QProgAst):
        super().__init__()

        # restructure the sequential composition, so that it is always associated to the right
        if isinstance(S0, AstSeq):
            S0, S1 = S0.S0, AstSeq(S0.S1, S1)

        self.S0 = S0
        self.S1 = S1

    def eval(self, env: Env) -> QProgAst:
        return AstSeq(
            self.S0.eval(env),
            self.S1.eval(env)
        )

    def definite(self, env) -> bool:
        return self.S0.definite(env) and self.S1.definite(env)
    
    def prefix_str(self, prefix="") -> str:
        return self.S0.prefix_str(prefix) + "\n" + self.S1.prefix_str(prefix)
    
    @property
    def extract(self) -> QProgAst:
        return AstSeq(self.S0.extract, self.S1.extract)
    
    def get_prescription(self) -> list[AstPres]:
        return self.S0.get_prescription() + self.S1.get_prescription()
    
class AstProb(QProgAst):
    def __init__(self, S0 : QProgAst, S1 : QProgAst, p : float):
        super().__init__()
        self.S0 = S0
        self.S1 = S1
        
        if p < 0 or p > 1:
            raise ValueError("Invalid probability: '" + str(p) + "'.")
        
        self.p = p

    def eval(self, env: Env) -> QProgAst:
        return AstProb(
            self.S0.eval(env),
            self.S1.eval(env),
            self.p
        )


    def definite(self, env: Env) -> bool:
        return self.S0.definite(env) and self.S1.definite(env)
    
    def prefix_str(self, prefix="") -> str:
        res = prefix + "{\n" + self.S0.prefix_str(prefix + INDENT) + "\n"
        res += prefix + "[⊕ " + str(self.p) +"]\n"
        res += self.S1.prefix_str(prefix + INDENT) + "\n"
        res += prefix + "}"
        return res
    
    @property
    def extract(self) -> QProgAst:
        return AstProb(self.S0.extract, self.S1.extract, self.p)
        
    def get_prescription(self) -> list[AstPres]:
        return self.S0.get_prescription() + self.S1.get_prescription()

class AstIf(QProgAst):
    def __init__(self, P : EIQOptAbstract, S1 : QProgAst, S0 : QProgAst):
        super().__init__()
        
        self.P = P
        self.S1 = S1
        self.S0 = S0
    
    def eval(self, env: Env) -> QProgAst:
        # check whether P is a projector
        if not self.P.eval(env).iqopt.qval.is_projector:
            raise ValueError("The operator '" + str(self.P) + "' for assertion statement is not projective.")
        
        return AstIf(
            self.P.eval(env),
            self.S1.eval(env),
            self.S0.eval(env))


    def definite(self, env: Env) -> bool:
        return self.S1.definite(env) and self.S0.definite(env)
    
    def prefix_str(self, prefix="") -> str:
        res = prefix + "if " + str(self.P) + " then\n"
        res += self.S1.prefix_str(prefix + INDENT) + "\n"
        res += prefix + "else\n"
        res += self.S0.prefix_str(prefix + INDENT) + "\n"
        res += prefix + "end"
        return res

    @property
    def extract(self) -> QProgAst:
        return AstIf(self.P, self.S1.extract, self.S0.extract)

    def get_prescription(self) -> list[AstPres]:
        return self.S1.get_prescription() + self.S0.get_prescription()
    
class AstWhile(QProgAst):
    def __init__(self, P : EIQOptAbstract, S : QProgAst):
        super().__init__()

        self.P = P
        self.S = S

    def eval(self, env: Env) -> QProgAst:
        # check whether P is a projector
        if not self.P.eval(env).iqopt.qval.is_projector:
            raise ValueError("The operator '" + str(self.P) + "' for assertion statement is not projective.")
        
        return AstWhile(
            self.P.eval(env),
            self.S.eval(env)
        )

    
    def definite(self, env: Env) -> bool:
        return self.S.definite(env)
    
    def prefix_str(self, prefix="") -> str:
        res = prefix + "while " + str(self.P) + " do\n"
        res += self.S.prefix_str(prefix + INDENT) + "\n"
        res += prefix + "end"
        return res

    @property
    def extract(self) -> QProgAst:
        return AstWhile(self.P, self.S.extract)

    def get_prescription(self) -> list[AstPres]:
        return self.S.get_prescription()