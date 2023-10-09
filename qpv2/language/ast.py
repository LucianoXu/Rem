
from ..qplcomp import Expr, QVar, IQOpt, expr_type_check

INDENT = "  "

class Ast:
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

class AstAbort(Ast):
    def __init__(self):
        pass

    @property
    def definite(self) -> bool:
        return True
    
    def prefix_str(self, prefix="") -> str:
        return prefix + "abort"


class AstSkip(Ast):
    def __init__(self):
        pass

    @property
    def definite(self) -> bool:
        return True
    
    def prefix_str(self, prefix="") -> str:
        return prefix + "skip"
    

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
    
class AstUnitary(Ast):
    def __init__(self, eU : Expr):
        expr_type_check(eU, IQOpt)

        # check whether this is a unitary
        if not eU.eval().qval.is_unitary:   # type: ignore
            raise ValueError("The operator '" + str(eU) + "' for unitary statement is not unitary.")
        
        self._eU = eU

    @property
    def U(self) -> IQOpt:
        return self._eU.eval()  # type: ignore

    @property
    def definite(self) -> bool:
        return True
    
    def prefix_str(self, prefix="") -> str:
        return prefix + str(self._eU)
    

class AstAssert(Ast):
    def __init__(self, eP : Expr):
        expr_type_check(eP, IQOpt)

        # check whether this is a projector
        if not eP.eval().qval.is_projector: # type: ignore
            raise ValueError("The operator '" + str(eP) + "' for assertion statement is not projective.")
        
        self._eP = eP

    @property
    def P(self) -> IQOpt:
        return self._eP.eval()  # type: ignore

    @property
    def definite(self) -> bool:
        return True
    
    def prefix_str(self, prefix="") -> str:
        return prefix + "assert " + str(self._eP)
    

class AstPres(Ast):
    def __init__(self, eP : Expr, eQ : Expr):
        expr_type_check(eP, IQOpt)
        expr_type_check(eQ, IQOpt)

        # check whether P and Q are projectors
        if not eP.eval().qval.is_projector: # type: ignore
            raise ValueError("The operator '" + str(eP) + "' for assertion statement is not projective.")
        if not eQ.eval().qval.is_projector: # type: ignore
            raise ValueError("The operator '" + str(eQ) + "' for assertion statement is not projective.")
        
        self._eP = eP
        self._eQ = eQ

    @property
    def definite(self) -> bool:
        return False
    
    def prefix_str(self, prefix="") -> str:
        return prefix + "[ pre: " + str(self._eP) + ", post: " + str(self._eQ) + " ]"

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
    

class AstProb(Ast):
    def __init__(self, S0 : Ast, S1 : Ast, p : float):
        self._S0 = S0
        self._S1 = S1
        
        if p < 0 or p > 1:
            raise ValueError("Invalid probability: '" + str(p) + "'.")
        
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
    

class AstIf(Ast):
    def __init__(self, eP : Expr, S1 : Ast, S0 : Ast):
        expr_type_check(eP, IQOpt)

        # check whether P is a projector
        if not eP.eval().qval.is_projector: # type: ignore
            raise ValueError("The operator '" + str(eP) + "' for assertion statement is not projective.")
        
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


class AstWhile(Ast):
    def __init__(self, eP : Expr, S : Ast):
        expr_type_check(eP, IQOpt)

        # check whether P is a projector
        if not eP.eval().qval.is_projector: # type: ignore
            raise ValueError("The operator '" + str(eP) + "' for assertion statement is not projective.")
        
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


