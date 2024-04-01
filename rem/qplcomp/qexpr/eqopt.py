from __future__ import annotations
from typing import Type

from ...mTLC.env import TypedTerm, Env, Types

from .eqvec import EQVecAbstract, QVecType
from .eqso import QSOptType, EQSOptAbstract

from ..qval import QVec, QOpt, QSOpt, qproj_from_qvec

from abc import ABC, abstractmethod
import numpy as np

class QOptType(Types):
    symbol = "QOpt"
    
    def __init__(self, qnum: int):
        super().__init__()
        self.qnum = qnum

    def __str__(self) -> str:
        return f"QOpt[{self.qnum}]"

class EQOptAbstract(TypedTerm, ABC):
    '''
    The expression for Quantum Operators.
    '''
    def __init__(self, qnum: int):
        self.type : QOptType = QOptType(qnum)
    
    @abstractmethod
    def eval(self, env: Env) -> EQOpt:
        pass

class EQOpt(EQOptAbstract):
    '''
    The expression for Quantum Operators.

    Terminal.
    '''

    def __init__(self, qopt : QOpt):
        super().__init__(qopt.qnum)
        assert isinstance(qopt, QOpt), "ASSERTION FAILED"
        self.qopt = qopt

    def eval(self, env: Env) -> EQOpt:
        return self
    
    def __str__(self) -> str:
        return str(self.qopt)
    


class EQOptKetProj(EQOptAbstract):
    '''
    The experssion for quantum projective operators from kets.

    EQOptKetProj ::= '[' (v : QVec) ']'
    '''

    def __init__(self, vec : EQVecAbstract):
        vec.type_checking(QVecType)

        super().__init__(vec.type.qnum)

        self.vec = vec

    
    def eval(self, env) -> EQOpt:
        return EQOpt(qproj_from_qvec(self.vec.eval(env).qvec))

    def __str__(self) -> str:
        return f"[{self.vec}]"



class EQOptAdd(EQOptAbstract):
    '''
    The expression for additions of quantum operators.

    EQOptAdd ::= (a : QOpt) '+' (b : QOpt)
    
    Nonterminal.
    '''

    def __init__(self, optA : EQOptAbstract, optB : EQOptAbstract):
        optA.type_checking(QOptType)
        optB.type_checking(QOptType)

        if optA.type.qnum != optB.type.qnum:
            raise ValueError("Quantum operator addition with different dimensions.")
        
        super().__init__(optA.type.qnum)

        self.optA = optA
        self.optB = optB

    def eval(self, env: Env) -> EQOpt:
        return EQOpt(self.optA.eval(env).qopt + self.optB.eval(env).qopt)
    
    def __str__(self) -> str:
        return "(" + str(self.optA) + "+" + str(self.optB) + ")"
    
    def __hash__(self) -> int:
        return hash(("qopt-add", self.optA, self.optB))
    
    def __eq__(self, other : object) -> bool:
        return isinstance(other, EQOptAdd) and self.optA == other.optA and self.optB == other.optB
    

class EQOptNeg(EQOptAbstract):
    '''
    The expression for negation of a quantum operator.

    EQOptNeg ::= '(' '-' (a : QOpt) ')'
    
    Nonterminal.
    '''

    def __init__(self, opt : EQOptAbstract):
        opt.type_checking(QOptType)

        super().__init__(opt.type.qnum)

        self.opt = opt

    
    def eval(self, env: Env) -> EQOpt:
        return EQOpt(- self.opt.eval(env).qopt)
    
    def __str__(self) -> str:
        return "(-" + str(self.opt) + ")"
    
    def __hash__(self) -> int:
        return hash(("qopt-neg", self.opt))
    
    def __eq__(self, other : object) -> bool:
        return isinstance(other, EQOptNeg) and self.opt == other.opt



class EQOptSub(EQOptAbstract):
    '''
    The expression for subtractions of quantum operators.

    EQOptSub ::= (a : QOpt) '-' (b : QOpt)
    
    Nonterminal.
    '''

    def __init__(self, optA : EQOptAbstract, optB : EQOptAbstract):
        optA.type_checking(QOptType)
        optB.type_checking(QOptType)

        if optA.type.qnum != optB.type.qnum:
            raise ValueError("Quantum operator subtraction with different dimensions.")
        
        super().__init__(optA.type.qnum)

        self.optA = optA
        self.optB = optB

    def eval(self, env: Env) -> EQOpt:
        return EQOpt(self.optA.eval(env).qopt - self.optB.eval(env).qopt)
    
    def __str__(self) -> str:
        return "(" + str(self.optA) + "-" + str(self.optB) + ")"
    
    def __hash__(self) -> int:
        return hash(("qopt-sub", self.optA, self.optB))
    
    def __eq__(self, other : object) -> bool:
        return isinstance(other, EQOptSub) and self.optA == other.optA and self.optB == other.optB

class EQOptMul(EQOptAbstract):
    '''
    The expression for subtractions of quantum operators.

    EQOptMul ::= (a : QOpt) '*' (b : QOpt)
    
    Nonterminal.
    '''

    def __init__(self, optA : EQOptAbstract, optB : EQOptAbstract):
        optA.type_checking(QOptType)
        optB.type_checking(QOptType)

        if optA.type.qnum != optB.type.qnum:
            raise ValueError("Quantum operator multiplication with different dimensions.")
        
        super().__init__(optA.type.qnum)

        self.optA = optA
        self.optB = optB

    def eval(self, env: Env) -> EQOpt:
        return EQOpt(self.optA.eval(env).qopt @ self.optB.eval(env).qopt)
    
    def __str__(self) -> str:
        return "(" + str(self.optA) + " " + str(self.optB) + ")"
    
    def __hash__(self) -> int:
        return hash(("qopt-mul", self.optA, self.optB))
    
    def __eq__(self, other : object) -> bool:
        return isinstance(other, EQOptMul) and self.optA == other.optA and self.optB == other.optB

class EQOptScale(EQOptAbstract):
    '''
    The expression for scaling of quantum operators.

    EQOptScale ::=  (c : complex) (b : QOpt)
                    | (c : complex) '*' (b : QOpt)
    
    Nonterminal.
    '''

    def __init__(self, c : complex, opt : EQOptAbstract):
        opt.type_checking(QOptType)

        super().__init__(opt.type.qnum)

        assert isinstance(c, (complex, float)), "ASSERTION FAILED"
        self.c = c
        self.opt = opt
    
    def eval(self, env: Env) -> EQOpt:
        return EQOpt(self.c * self.opt.eval(env).qopt)
    
    def __str__(self) -> str:
        return "(" + str(self.c) + " " + str(self.opt) + ")"
    
    def __hash__(self) -> int:
        return hash(("qopt-scale", self.c, self.opt))
    
    def __eq__(self, other : object) -> bool:
        return isinstance(other, EQOptScale) and self.c == other.c and self.opt == other.opt
    

class EQOptDagger(EQOptAbstract):
    '''
    The expression for the conjugate transpose of a quantum operator.

    EQOptDagger ::= (a : QOpt) '^\\dagger'
                    | (a : QOpt) '†'
    
    Nonterminal.
    '''

    def __init__(self, opt : EQOptAbstract):
        opt.type_checking(QOptType)

        super().__init__(opt.type.qnum)

        self.opt = opt

    def eval(self, env: Env) -> EQOpt:
        return EQOpt(self.opt.eval(env).qopt.dagger())
    
    def __str__(self) -> str:
        return "(" + str(self.opt) + "†" + ")"
    
    def __hash__(self) -> int:
        return hash(("qopt-dagger", self.opt))
    
    def __eq__(self, other : object) -> bool:
        return isinstance(other, EQOptDagger) and self.opt == other.opt


class EQOptTensor(EQOptAbstract):
    '''
    The expression for tensor product of quantum operators.

    EQOptTensor ::= (a : QOpt) '⊗' (b : QOpt)
                    | (a : QOpt) '\\otimes' (b : QOpt)
    
    Nonterminal.
    '''

    def __init__(self, optA : EQOptAbstract, optB : EQOptAbstract):
        optA.type_checking(QOptType)
        optB.type_checking(QOptType)

        super().__init__(optA.type.qnum + optB.type.qnum)

        self.optA = optA
        self.optB = optB

    def eval(self, env: Env) -> EQOpt:
        return EQOpt(self.optA.eval(env).qopt.tensor(self.optB.eval(env).qopt))
    
    def __str__(self) -> str:
        return "(" + str(self.optA) + " ⊗ " + str(self.optB) + ")"
    
    def __hash__(self) -> int:
        return hash(("qopt-tensor", self.optA, self.optB))
    
    def __eq__(self, other : object) -> bool:
        return isinstance(other, EQOptTensor) and self.optA == other.optA and self.optB == other.optB



class EQOptDisjunct(EQOptAbstract):
    '''
    The expression for disjunction of projective quantum operators.

    EQOptDisjunct ::= (a : QOpt) '\\vee' (b : QOpt)
                    | (a : QOpt) '∨' (b : QOpt)
    
    Nonterminal.
    '''

    def __init__(self, optA : EQOptAbstract, optB : EQOptAbstract):
        optA.type_checking(QOptType)
        optB.type_checking(QOptType)

        if optA.type.qnum != optB.type.qnum:
            raise ValueError("Quantum operator disjunction with different dimensions.")
        
        super().__init__(optA.type.qnum)

        self.optA = optA
        self.optB = optB
        
    def eval(self, env: Env) -> EQOpt:
        return EQOpt(self.optA.eval(env).qopt | self.optB.eval(env).qopt)
    
    def __str__(self) -> str:
        return "(" + str(self.optA) + " ∨ " + str(self.optB) + ")"
    
    def __hash__(self) -> int:
        return hash(("qopt-disjunct", self.optA, self.optB))
    
    def __eq__(self, other : object) -> bool:
        return isinstance(other, EQOptDisjunct) and self.optA == other.optA and self.optB == other.optB
    


class EQOptConjunct(EQOptAbstract):
    '''
    The expression for conjunction of projective quantum operators.

    EQOptConjunct   ::= (a : QOpt) '\\wedge' (b : QOpt)
                    | (a : QOpt) '∧' (b : QOpt)
    
    Nonterminal.
    '''

    def __init__(self, optA : EQOptAbstract, optB : EQOptAbstract):
        optA.type_checking(QOptType)
        optB.type_checking(QOptType)

        if optA.type.qnum != optB.type.qnum:
            raise ValueError("Quantum operator conjunction with different dimensions.")
        
        super().__init__(optA.type.qnum)

        self.optA = optA
        self.optB = optB
        
    def eval(self, env: Env) -> EQOpt:
        return EQOpt(self.optA.eval(env).qopt & self.optB.eval(env).qopt)
    
    def __str__(self) -> str:
        return "(" + str(self.optA) + " ∧ " + str(self.optB) + ")"
    
    def __hash__(self) -> int:
        return hash(("qopt-conjunct", self.optA, self.optB))
    
    def __eq__(self, other : object) -> bool:
        return isinstance(other, EQOptConjunct) and self.optA == other.optA and self.optB == other.optB
    
class EQOptComplement(EQOptAbstract):
    '''
    The expression for complement of projective quantum operators.

    EQOptComplement ::= (a : QOpt) '^\\bot'
                    | (a : QOpt) '^⊥'
    
    Nonterminal.
    '''

    def __init__(self, opt : EQOptAbstract):
        opt.type_checking(QOptType)

        super().__init__(opt.type.qnum)

        self.opt = opt
    
    def eval(self, env: Env) -> EQOpt:
        return EQOpt(~ self.opt.eval(env).qopt)
    
    def __str__(self) -> str:
        return "(" + str(self.opt) + "^⊥)"
    
    def __hash__(self) -> int:
        return hash(("qopt-complement", self.opt))
    
    def __eq__(self, other : object) -> bool:
        return isinstance(other, EQOptComplement) and self.opt == other.opt
    


class EQOptSasakiImply(EQOptAbstract):
    '''
    The expression for Sasaki implication of projective quantum operators.

    EQOptSasakiImply   ::= (a : QOpt) '\\SasakiImply' (b : QOpt)
                        | (a : QOpt) '⇝' (b : QOpt)
    
    Nonterminal.
    '''

    def __init__(self, optA : EQOptAbstract, optB : EQOptAbstract):
        optA.type_checking(QOptType)
        optB.type_checking(QOptType)

        if optA.type.qnum != optB.type.qnum:
            raise ValueError("Quantum operator Sasaki implication with different dimensions.")
        
        super().__init__(optA.type.qnum)

        self.optA = optA
        self.optB = optB


    def eval(self, env: Env) -> EQOpt:
        return EQOpt(self.optA.eval(env).qopt.Sasaki_imply(self.optB.eval(env).qopt))
    
    def __str__(self) -> str:
        return "(" + str(self.optA) + " ⇝ " + str(self.optB) + ")"
    
    def __hash__(self) -> int:
        return hash(("qopt-sasaki-imply", self.optA, self.optB))
    
    def __eq__(self, other : object) -> bool:
        return isinstance(other, EQOptSasakiImply) and self.optA == other.optA and self.optB == other.optB
    

class EQOptSasakiConjunct(EQOptAbstract):
    '''
    The expression for Sasaki conjunction of projective quantum operators.

    EQOptSasakiConjunct ::= (a : QOpt) '\\SasakiConjunct' (b : QOpt)
                        | (a : QOpt) '⋒' (b : QOpt)
    
    Nonterminal.
    '''

    def __init__(self, optA : EQOptAbstract, optB : EQOptAbstract):
        optA.type_checking(QOptType)
        optB.type_checking(QOptType)

        if optA.type.qnum != optB.type.qnum:
            raise ValueError("Quantum operator Sasaki conjunction with different dimensions.")

        super().__init__(optA.type.qnum)

        self.optA = optA
        self.optB = optB
            
    def eval(self, env) -> EQOpt:
        return EQOpt(self.optA.eval(env).qopt.Sasaki_conjunct(self.optB.eval(env).qopt))
    
    def __str__(self) -> str:
        return "(" + str(self.optA) + " ⋒ " + str(self.optB) + ")"
    
    def __hash__(self) -> int:
        return hash(("qopt-sasaki-conjunct", self.optA, self.optB))
    
    def __eq__(self, other : object) -> bool:
        return isinstance(other, EQOptSasakiConjunct) and self.optA == other.optA and self.optB == other.optB


class EQSOptApply(EQOptAbstract):
    '''
    The expression for application of superoperators on operators.

    EQOptConjunct   ::= (E : QSOpt) '(' (b : QOpt) ')'
    
    Nonterminal.
    '''

    def __init__(self, so : EQSOptAbstract, opt : EQOptAbstract):
        so.type_checking(QSOptType)
        opt.type_checking(QSOptType)

        if so.type.qnum != opt.type.qnum:
            raise ValueError("Quantum operator application with different dimensions.")
        
        super().__init__(so.type.qnum)

        self.so = so
        self.opt = opt

    
    def eval(self, env: Env) -> EQOpt:
        return EQOpt(self.so.eval(env).qso.apply(self.opt.eval(env).qopt))
        
    def __str__(self) -> str:
        return "(" + str(self.so) + "(" + str(self.opt) + "))"
    
    def __hash__(self) -> int:
        return hash(("qsopt-apply", self.so, self.opt))
    
    def __eq__(self, other : object) -> bool:
        return isinstance(other, EQSOptApply) and self.so == other.so and self.opt == other.opt

