from __future__ import annotations
from typing import Type

from qplcomp import IQOpt
from qplcomp import Expr, Variable, QVar, IQOpt, expr_type_check

from ..error import type_check, QPVError

INDENT = "  "

class Ast:

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
    def extract(self) -> Ast:
        '''
        Extract the refinement result as a program syntax (without refinement proofs).
        '''
        raise NotImplementedError()
    
    def get_prescription(self) -> list[AstPres]:
        '''
        Return the unsolved prescriptions.
        '''
        raise NotImplementedError()
    
    def wlp(self, post : IQOpt) -> IQOpt:
        '''
        Calculate the weakest liberal precondition.
        '''
        raise NotImplementedError()


class AstSubprog(Ast):
    def __init__(self, esubprog : Variable):
        self.__esubprog = esubprog

    @property
    def subgprog(self) -> Ast:
        east = self.__esubprog.eval()
        if not isinstance(east, Ast):
            raise Exception()
        
        return east


    @property
    def definite(self) -> bool:
        return self.subgprog.definite

    
    def prefix_str(self, prefix = "") -> str:
        return prefix + "Prog " + str(self.__esubprog)

    
    @property
    def extract(self) -> Ast:
        return self
    
    def get_prescription(self) -> list[AstPres]:
        return []
    
    def wlp(self, post : IQOpt) -> IQOpt:
        '''
        Calculate the weakest liberal precondition.
        '''
        return self.subgprog.wlp(post)
    

class AstAbort(Ast):
    def __init__(self):
        pass

    @property
    def definite(self) -> bool:
        return True
    
    def prefix_str(self, prefix="") -> str:
        return prefix + "abort"
    
    def get_prescription(self) -> list[AstPres]:
        return []

    def wlp(self, post: IQOpt) -> IQOpt:
        return IQOpt.identity(False)


class AstSkip(Ast):
    def __init__(self):
        pass

    @property
    def definite(self) -> bool:
        return True
    
    def prefix_str(self, prefix="") -> str:
        return prefix + "skip"
    
    @property
    def extract(self) -> Ast:
        return self

    def get_prescription(self) -> list[AstPres]:
        return []
    
    def wlp(self, post: IQOpt) -> IQOpt:
        return post


class AstInit(Ast):
    def __init__(self, eqvar : Expr):
        expr_type_check(eqvar, QVar)
        self._eqvar = eqvar

    @property
    def qvar(self) -> QVar:
        return self._eqvar.eval()   # type: ignore

    @property
    def definite(self) -> bool:
        return True
    
    def prefix_str(self, prefix="") -> str:
        return prefix + str(self._eqvar) + ":=0"

    @property
    def extract(self) -> Ast:
        return self

    def get_prescription(self) -> list[AstPres]:
        return []
    
    def wlp(self, post: IQOpt) -> IQOpt:
        return post.initwlp(self.qvar)

    
class AstUnitary(Ast):
    def __init__(self, eU : Expr):
        expr_type_check(eU, IQOpt)

        # check whether this is a unitary
        if not eU.eval().qval.is_unitary:   # type: ignore
            raise QPVError("The operator '" + str(eU) + "' for unitary statement is not unitary.")
        
        self._eU = eU

    @property
    def U(self) -> IQOpt:
        return self._eU.eval()  # type: ignore

    @property
    def definite(self) -> bool:
        return True
    
    def prefix_str(self, prefix="") -> str:
        return prefix + str(self._eU)

    @property
    def extract(self) -> Ast:
        return self

    def get_prescription(self) -> list[AstPres]:
        return []

    def wlp(self, post: IQOpt) -> IQOpt:
        U = self.U
        return U.dagger() @ post @ U
    

class AstAssert(Ast):
    def __init__(self, eP : Expr):
        expr_type_check(eP, IQOpt)

        # check whether this is a projector
        if not eP.eval().qval.is_projector: # type: ignore
            raise QPVError("The operator '" + str(eP) + "' for assertion statement is not projective.")
        
        self._eP = eP

    @property
    def P(self) -> IQOpt:
        return self._eP.eval()  # type: ignore

    @property
    def definite(self) -> bool:
        return True
    
    def prefix_str(self, prefix="") -> str:
        return prefix + "assert " + str(self._eP)
    
    @property
    def extract(self) -> Ast:
        return self

    def get_prescription(self) -> list[AstPres]:
        return []

    def wlp(self, post: IQOpt) -> IQOpt:
        return self.P.Sasaki_imply(post)

    

class AstPres(Ast):
    def __init__(self, eP : Expr, eQ : Expr):
        '''
        This `SRefined` attribute can refer to the subsequent refined programs for this program. If `None`, then the current program is used.
        '''
        self.SRefined : Ast | None = None

        expr_type_check(eP, IQOpt)
        expr_type_check(eQ, IQOpt)

        # check whether P and Q are projectors
        if not eP.eval().qval.is_projector: # type: ignore
            raise QPVError("The operator '" + str(eP) + "' for assertion statement is not projective.")
        if not eQ.eval().qval.is_projector: # type: ignore
            raise QPVError("The operator '" + str(eQ) + "' for assertion statement is not projective.")
        
        self._eP = eP
        self._eQ = eQ

    @property
    def P(self) -> IQOpt:
        return self._eP.eval()  # type: ignore

    @property
    def Q(self) -> IQOpt:
        return self._eQ.eval()  # type: ignore


    def refine(self, SRefined: Ast) -> None:
        '''
        For prescriptions, it checks the weakest precondition.
        '''
        if not self.P <= SRefined.wlp(self.Q):
            msg = "Refinement failed. The relation P <= wlp.S.Q is not satisfied for: \n"
            msg += "P = \n" + str(self.P) + "\n"
            msg += "Q = \n" + str(self.Q) + "\n"
            raise QPVError(msg)
        
        self.SRefined = SRefined

    @property
    def definite(self) -> bool:
        return False
    
    def prefix_str(self, prefix="") -> str:
        res = prefix + "[ pre: " + str(self._eP) + ", post: " + str(self._eQ) + " ]"
        if self.SRefined is None:
            return res
        else:
            res += "\n" + prefix + INDENT + "==> {\n"
            res += self.SRefined.prefix_str(prefix + INDENT) + "\n"
            res += prefix + "}"
            return res


    @property
    def extract(self) -> Ast:
        if self.SRefined is not None:
            return self.SRefined.extract
        else:
            return self

    def get_prescription(self) -> list[AstPres]:
        return [self]
    
    def wlp(self, post: IQOpt) -> IQOpt:
        if post == IQOpt.identity(False):
            return IQOpt.identity(False)
        elif self.Q <= post:
            return self.P
        else:
            return IQOpt.zero(False)


class AstSeq(Ast):
    def __init__(self, S0 : Ast, S1 : Ast):
        self._S0 = S0
        self._S1 = S1

    @property
    def S0(self) -> Ast:
        return self._S0

    @property
    def S1(self) -> Ast:
        return self._S1
    
    @property
    def definite(self) -> bool:
        return self._S0.definite and self._S1.definite
    
    def prefix_str(self, prefix="") -> str:
        return self._S0.prefix_str(prefix) + ";\n" + self._S1.prefix_str(prefix)
    
    @property
    def extract(self) -> Ast:
        return AstSeq(self.S0.extract, self.S1.extract)
    
    def get_prescription(self) -> list[AstPres]:
        return self.S0.get_prescription() + self.S1.get_prescription()
    
    def wlp(self, post: IQOpt) -> IQOpt:
        return self.S0.wlp(self.S1.wlp(post))

class AstProb(Ast):
    def __init__(self, S0 : Ast, S1 : Ast, p : float):
        self._S0 = S0
        self._S1 = S1
        
        if p < 0 or p > 1:
            raise QPVError("Invalid probability: '" + str(p) + "'.")
        
        self._p = p

    @property
    def S0(self) -> Ast:
        return self._S0

    @property
    def S1(self) -> Ast:
        return self._S1
    
    @property
    def p(self) -> float:
        return self._p


    @property
    def definite(self) -> bool:
        return self._S0.definite and self._S1.definite
    
    def prefix_str(self, prefix="") -> str:
        res = prefix + "(\n" + self._S0.prefix_str(prefix + INDENT) + "\n"
        res += prefix + "_" + str(self._p) + "⊗\n"
        res += self._S1.prefix_str(prefix + INDENT) + "\n"
        res += prefix + ")"
        return res
    
    @property
    def extract(self) -> Ast:
        return AstProb(self.S0.extract, self.S1.extract, self.p)
        
    def get_prescription(self) -> list[AstPres]:
        return self.S0.get_prescription() + self.S1.get_prescription()

    def wlp(self, post: IQOpt) -> IQOpt:
        return self.S0.wlp(post) & self.S1.wlp(post)
    

class AstIf(Ast):
    def __init__(self, eP : Expr, S1 : Ast, S0 : Ast):
        expr_type_check(eP, IQOpt)

        # check whether P is a projector
        if not eP.eval().qval.is_projector: # type: ignore
            raise QPVError("The operator '" + str(eP) + "' for assertion statement is not projective.")
        
        self._eP = eP
        self._S1 = S1
        self._S0 = S0
    
    @property
    def P(self) -> IQOpt:
        return self._eP.eval()  # type: ignore
    
    @property
    def S1(self) -> Ast:
        return self._S1

    @property
    def S0(self) -> Ast:
        return self._S0


    @property
    def definite(self) -> bool:
        return self._S1.definite and self._S0.definite
    
    def prefix_str(self, prefix="") -> str:
        res = prefix + "if " + str(self._eP) + " then\n"
        res += self._S1.prefix_str(prefix + INDENT) + "\n"
        res += prefix + "else\n"
        res += self._S0.prefix_str(prefix + INDENT) + "\n"
        res += prefix + "end"
        return res

    @property
    def extract(self) -> Ast:
        return AstIf(self._eP, self.S1.extract, self.S0.extract)

    def get_prescription(self) -> list[AstPres]:
        return self.S1.get_prescription() + self.S0.get_prescription()
    
    def wlp(self, post: IQOpt) -> IQOpt:
        return self.P.Sasaki_imply(self.S1.wlp(post)) &\
              (~ self.P).Sasaki_imply(self.S0.wlp(post))


class AstWhile(Ast):
    def __init__(self, eP : Expr, S : Ast):
        expr_type_check(eP, IQOpt)

        # check whether P is a projector
        if not eP.eval().qval.is_projector: # type: ignore
            raise QPVError("The operator '" + str(eP) + "' for assertion statement is not projective.")
        
        self._eP = eP
        self._S = S

    @property
    def P(self) -> IQOpt:
        return self._eP.eval()  # type: ignore

    @property
    def S(self) -> Ast:
        return self._S
    
    @property
    def definite(self) -> bool:
        return self._S.definite
    
    def prefix_str(self, prefix="") -> str:
        res = prefix + "while " + str(self._eP) + " do\n"
        res += self._S.prefix_str(prefix + INDENT) + "\n"
        res += prefix + "end"
        return res

    @property
    def extract(self) -> Ast:
        return AstWhile(self._eP, self.S.extract)

    def get_prescription(self) -> list[AstPres]:
        return self.S.get_prescription()
    
    def wlp(self, post: IQOpt) -> IQOpt:
        '''
        This will terminate because the lattice has finite height.
        '''
        flag = True
        Rn = IQOpt.identity(False)
        Rn_1 = IQOpt.identity(False)

        # this is guaranteed to terminate
        while flag:
            Rn = Rn_1
            Rn_1 = self.P.Sasaki_imply(self.S.wlp(Rn)) & (~ self.P).Sasaki_imply(post)

            flag = not Rn == Rn_1

        return Rn


######################################################################
# the Expr object for programs

class EAst(Expr):
    def __init__(self, ast : Ast):
        self.__ast = ast

    @property
    def ast(self) -> Ast:
        return self.__ast

    @property
    def T(self) -> Type:
        return Ast
    
    def eval(self) -> object:
        return self.__ast
    
    def __str__(self) -> str:
        return str(self.__ast)