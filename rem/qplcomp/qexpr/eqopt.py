from __future__ import annotations
from typing import Type

from ...mTLC.env import TypedTerm, Env, Types

from .eqvec import EQVecAbstract, QVecType
from .eqso import QSOptType, EQSOptAbstract

from ..qval import QVec, QOpt, QSOpt, qproj_from_qvec

from abc import ABC, abstractmethod
import numpy as np

class QOptType(Types):
    def __str__(self) -> str:
        return "QOpt"

class EQOptAbstract(TypedTerm, ABC):
    '''
    The expression for Quantum Operators.
    '''
    def __init__(self):
        super().__init__(QOptType())
    
    @abstractmethod
    def eval(self, env: Env) -> EQOpt:
        pass

class EQOpt(EQOptAbstract):
    '''
    The expression for Quantum Operators.

    Terminal.
    '''

    def __init__(self, qopt : QOpt):
        super().__init__()
        assert isinstance(qopt, QOpt)
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
        super().__init__()

        assert isinstance(vec, EQVecAbstract)
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
        super().__init__()

        self.optA = optA
        self.optB = optB

    def eval(self, env: Env) -> EQOpt:
        return EQOpt(self.optA.eval(env).qopt + self.optB.eval(env).qopt)
    
    def __str__(self) -> str:
        return "(" + str(self.optA) + "+" + str(self.optB) + ")"
    

class EQOptNeg(EQOptAbstract):
    '''
    The expression for negation of a quantum operator.

    EQOptNeg ::= '(' '-' (a : QOpt) ')'
    
    Nonterminal.
    '''

    def __init__(self, opt : EQOptAbstract):
        super().__init__()

        self.opt = opt

    
    def eval(self, env: Env) -> EQOpt:
        return EQOpt(- self.opt.eval(env).qopt)
    
    def __str__(self) -> str:
        return "(-" + str(self.opt) + ")"
    



class EQOptSub(EQOptAbstract):
    '''
    The expression for subtractions of quantum operators.

    EQOptSub ::= (a : QOpt) '-' (b : QOpt)
    
    Nonterminal.
    '''

    def __init__(self, optA : EQOptAbstract, optB : EQOptAbstract):
        super().__init__()

        self.optA = optA
        self.optB = optB

    def eval(self, env: Env) -> EQOpt:
        return EQOpt(self.optA.eval(env).qopt - self.optB.eval(env).qopt)
    
    def __str__(self) -> str:
        return "(" + str(self.optA) + "-" + str(self.optB) + ")"
    

class EQOptMul(EQOptAbstract):
    '''
    The expression for subtractions of quantum operators.

    EQOptMul ::= (a : QOpt) '*' (b : QOpt)
    
    Nonterminal.
    '''

    def __init__(self, optA : EQOptAbstract, optB : EQOptAbstract):
        super().__init__()

        self.optA = optA
        self.optB = optB

    def eval(self, env: Env) -> EQOpt:
        return EQOpt(self.optA.eval(env).qopt @ self.optB.eval(env).qopt)
    
    def __str__(self) -> str:
        return "(" + str(self.optA) + " " + str(self.optB) + ")"
    

class EQOptScale(EQOptAbstract):
    '''
    The expression for scaling of quantum operators.

    EQOptScale ::=  (c : complex) (b : QOpt)
                    | (c : complex) '*' (b : QOpt)
    
    Nonterminal.
    '''

    def __init__(self, c : complex, opt : EQOptAbstract):
        super().__init__()

        assert isinstance(c, (complex, float))
        self.c = c

        self.opt = opt
    
    def eval(self, env: Env) -> EQOpt:
        return EQOpt(self.c * self.opt.eval(env).qopt)
    
    def __str__(self) -> str:
        return "(" + str(self.c) + " " + str(self.opt) + ")"
    


class EQOptDagger(EQOptAbstract):
    '''
    The expression for the conjugate transpose of a quantum operator.

    EQOptDagger ::= (a : QOpt) '^\\dagger'
                    | (a : QOpt) '†'
    
    Nonterminal.
    '''

    def __init__(self, opt : EQOptAbstract):
        super().__init__()

        self.opt = opt

    def eval(self, env: Env) -> EQOpt:
        return EQOpt(self.opt.eval(env).qopt.dagger())
    
    def __str__(self) -> str:
        return "(" + str(self.opt) + "†" + ")"
    




class EQOptTensor(EQOptAbstract):
    '''
    The expression for tensor product of quantum operators.

    EQOptTensor ::= (a : QOpt) '⊗' (b : QOpt)
                    | (a : QOpt) '\\otimes' (b : QOpt)
    
    Nonterminal.
    '''

    def __init__(self, optA : EQOptAbstract, optB : EQOptAbstract):
        super().__init__()

        self.optA = optA
        self.optB = optB

    def eval(self, env: Env) -> EQOpt:
        return EQOpt(self.optA.eval(env).qopt.tensor(self.optB.eval(env).qopt))
    
    def __str__(self) -> str:
        return "(" + str(self.optA) + " ⊗ " + str(self.optB) + ")"
    



class EQOptDisjunct(EQOptAbstract):
    '''
    The expression for disjunction of projective quantum operators.

    EQOptDisjunct ::= (a : QOpt) '\\vee' (b : QOpt)
                    | (a : QOpt) '∨' (b : QOpt)
    
    Nonterminal.
    '''

    def __init__(self, optA : EQOptAbstract, optB : EQOptAbstract):
        super().__init__()

        self.optA = optA
        self.optB = optB
        
    def eval(self, env: Env) -> EQOpt:
        return EQOpt(self.optA.eval(env).qopt | self.optB.eval(env).qopt)
    
    def __str__(self) -> str:
        return "(" + str(self.optA) + " ∨ " + str(self.optB) + ")"
    


class EQOptConjunct(EQOptAbstract):
    '''
    The expression for conjunction of projective quantum operators.

    EQOptConjunct   ::= (a : QOpt) '\\wedge' (b : QOpt)
                    | (a : QOpt) '∧' (b : QOpt)
    
    Nonterminal.
    '''

    def __init__(self, optA : EQOptAbstract, optB : EQOptAbstract):
        super().__init__()

        self.optA = optA
        self.optB = optB
        
    def eval(self, env: Env) -> EQOpt:
        return EQOpt(self.optA.eval(env).qopt & self.optB.eval(env).qopt)
    
    def __str__(self) -> str:
        return "(" + str(self.optA) + " ∧ " + str(self.optB) + ")"
    
class EQOptComplement(EQOptAbstract):
    '''
    The expression for complement of projective quantum operators.

    EQOptComplement ::= (a : QOpt) '^\\bot'
                    | (a : QOpt) '^⊥'
    
    Nonterminal.
    '''

    def __init__(self, opt : EQOptAbstract):
        super().__init__()

        self.opt = opt
    
    def eval(self, env: Env) -> EQOpt:
        return EQOpt(~ self.opt.eval(env).qopt)
    
    def __str__(self) -> str:
        return "(" + str(self.opt) + "^⊥)"
    


class EQOptSasakiImply(EQOptAbstract):
    '''
    The expression for Sasaki implication of projective quantum operators.

    EQOptSasakiImply   ::= (a : QOpt) '\\SasakiImply' (b : QOpt)
                        | (a : QOpt) '⇝' (b : QOpt)
    
    Nonterminal.
    '''

    def __init__(self, optA : EQOptAbstract, optB : EQOptAbstract):
        super().__init__()

        self.optA = optA
        self.optB = optB


    def eval(self, env: Env) -> EQOpt:
        return EQOpt(self.optA.eval(env).qopt.Sasaki_imply(self.optB.eval(env).qopt))
    
    def __str__(self) -> str:
        return "(" + str(self.optA) + " ⇝ " + str(self.optB) + ")"
    


class EQOptSasakiConjunct(EQOptAbstract):
    '''
    The expression for Sasaki conjunction of projective quantum operators.

    EQOptSasakiConjunct ::= (a : QOpt) '\\SasakiConjunct' (b : QOpt)
                        | (a : QOpt) '⋒' (b : QOpt)
    
    Nonterminal.
    '''

    def __init__(self, optA : EQOptAbstract, optB : EQOptAbstract):
        super().__init__()

        self.optA = optA
        self.optB = optB
            
    def eval(self, env) -> EQOpt:
        return EQOpt(self.optA.eval(env).qopt.Sasaki_conjunct(self.optB.eval(env).qopt))
    
    def __str__(self) -> str:
        return "(" + str(self.optA) + " ⋒ " + str(self.optB) + ")"
    


class EQSOptApply(EQOptAbstract):
    '''
    The expression for application of superoperators on operators.

    EQOptConjunct   ::= (E : QSOpt) '(' (b : QOpt) ')'
    
    Nonterminal.
    '''

    def __init__(self, so : EQSOptAbstract, opt : EQOptAbstract):
        super().__init__()

        self.so = so
        self.opt = opt

    
    def eval(self, env: Env) -> EQOpt:
        return EQOpt(self.so.eval(env).qso.apply(self.opt.eval(env).qopt))
        
    def __str__(self) -> str:
        return "(" + str(self.so) + "(" + str(self.opt) + "))"

