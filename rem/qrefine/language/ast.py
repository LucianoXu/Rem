from __future__ import annotations
from typing import Type

from ...qplcomp import IQOpt, QVar, IQOpt
from ...mTLC.env import TypedTerm, Var, Types

from ...qplcomp.qexpr.eiqopt import *

from ..error import ValueError

INDENT = "  "

class QProgType(Types, ABC):
    symbol = "QProg"
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
    
    def get_prescription(self) -> list[AstPres]:
        '''
        Return the unsolved prescriptions.
        '''
        raise NotImplementedError()
    
    @property
    def all_qvar(self) -> QVar:
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
    
    def get_prescription(self) -> list[AstPres]:
        return []

    @property
    def all_qvar(self) -> QVar:
        return QVar([])
    
    def __hash__(self) -> int:
        return hash("abort")
    
    def __eq__(self, other : object) -> bool:
        return isinstance(other, AstAbort)

class AstSkip(QProgAst):
    def __init__(self):
        super().__init__()

    def eval(self, env: Env) -> QProgAst:
        return self

    def definite(self, env: Env) -> bool:
        return True
    
    def prefix_str(self, prefix="") -> str:
        return prefix + "skip"

    def get_prescription(self) -> list[AstPres]:
        return []
    
    @property
    def all_qvar(self) -> QVar:
        return QVar([])
    
    def __hash__(self) -> int:
        return hash("skip")
    
    def __eq__(self, other : object) -> bool:
        return isinstance(other, AstSkip)


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

    def get_prescription(self) -> list[AstPres]:
        return []
    
    @property
    def all_qvar(self) -> QVar:
        return self.eqvar.qvar
    
    def __hash__(self) -> int:
        return hash(("init", self.eqvar))
    
    def __eq__(self, other : object) -> bool:
        return isinstance(other, AstInit) and self.eqvar == other.eqvar

    

    
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

    def get_prescription(self) -> list[AstPres]:
        return []

    @property
    def all_qvar(self) -> QVar:
        return self.U.all_qvar
    
    def __hash__(self) -> int:
        return hash(("unitary", self.U))
    
    def __eq__(self, other : object) -> bool:
        return isinstance(other, AstUnitary) and self.U == other.U

    
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

    def get_prescription(self) -> list[AstPres]:
        return []

    @property
    def all_qvar(self) -> QVar:
        return self.P.all_qvar

    def __hash__(self) -> int:
        return hash(("assert", self.P))
    
    def __eq__(self, other : object) -> bool:
        return isinstance(other, AstAssert) and self.P == other.P
    

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

    def get_prescription(self) -> list[AstPres]:
        if self.SRefined is not None:
            return self.SRefined.get_prescription()
        else:
            return [self]
    
    @property
    def all_qvar(self) -> QVar:
        return self.P.all_qvar + self.Q.all_qvar

    def __hash__(self) -> int:
        return hash(("pres", self.P, self.Q))
    
    def __eq__(self, other : object) -> bool:
        return isinstance(other, AstPres) and self.P == other.P and self.Q == other.Q


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
    
    def get_prescription(self) -> list[AstPres]:
        return self.S0.get_prescription() + self.S1.get_prescription()
    
    @property
    def all_qvar(self) -> QVar:
        return self.S0.all_qvar + self.S1.all_qvar
    
    def __hash__(self) -> int:
        return hash(("seq", self.S0, self.S1))
    
    def __eq__(self, other : object) -> bool:
        return isinstance(other, AstSeq) and self.S0 == other.S0 and self.S1 == other.S1

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
        
    def get_prescription(self) -> list[AstPres]:
        return self.S0.get_prescription() + self.S1.get_prescription()

    @property
    def all_qvar(self) -> QVar:
        return self.S0.all_qvar + self.S1.all_qvar
    
    def __hash__(self) -> int:
        return hash(("prob", self.S0, self.S1, self.p))
    
    def __eq__(self, other : object) -> bool:
        return isinstance(other, AstProb) and self.S0 == other.S0 and self.S1 == other.S1 and self.p == other.p


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

    def get_prescription(self) -> list[AstPres]:
        return self.S1.get_prescription() + self.S0.get_prescription()
    
    @property
    def all_qvar(self) -> QVar:
        return self.P.all_qvar + self.S1.all_qvar + self.S0.all_qvar
    
    def __hash__(self) -> int:
        return hash(("if", self.P, self.S1, self.S0))
    
    def __eq__(self, other : object) -> bool:
        return isinstance(other, AstIf) and self.P == other.P and self.S1 == other.S1 and self.S0 == other.S0

    
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

    def get_prescription(self) -> list[AstPres]:
        return self.S.get_prescription()
    
    @property
    def all_qvar(self) -> QVar:
        return self.P.all_qvar + self.S.all_qvar
    
    def __hash__(self) -> int:
        return hash(("while", self.P, self.S))
    
    def __eq__(self, other : object) -> bool:
        return isinstance(other, AstWhile) and self.P == other.P and self.S == other.S
