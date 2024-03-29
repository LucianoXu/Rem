from __future__ import annotations
from typing import Type

from ..qval import QOpt, QVar, IQOpt

from ...mTLC.env import TypedTerm, Env, Types

from abc import ABC, abstractmethod

import numpy as np

from .eqopt import QOptType, EQOptAbstract
from .eqvar import QVarType, EQVar


class IQOptType(Types):
    symbol = "IQOpt"
    def __str__(self) -> str:
        return "IQOpt"
    
class EIQOptAbstract(TypedTerm):
    '''
    The Expression for Indexed Quantum Operators.
    '''
    def __init__(self):
        super().__init__(IQOptType())
    
    @abstractmethod
    def eval(self, env: Env) -> EIQOpt:
        pass

class EIQOpt(EIQOptAbstract):
    '''
    The Expression of Indexed Quantum Operators.
    
    EIQOpt ::= EQOpt EQVar
    '''

    def __init__(self, iqopt: IQOpt):
        super().__init__()

        assert isinstance(iqopt, IQOpt), "ASSERTION FAILED"
        self.iqopt = iqopt

    
    def eval(self, env: Env) -> EIQOpt:
        return self
    
    def __str__(self) -> str:
        return str(self.iqopt)
    
class EIQOptPair(EIQOptAbstract):
    '''
    The Expression of Indexed Quantum Operators.
    
    EIQOpt ::= EQOpt EQVar
    '''

    def __init__(self, qopt : EQOptAbstract, qvar : EQVar):
        qopt.type_checking(QOptType)
        qvar.type_checking(QVarType)

        if qopt.type.qnum != qvar.type.qnum:
            raise TypeError(f"Type Mismatch for operator {qopt} and qvar {qvar}.")

        super().__init__()

        self.qopt = qopt
        self.qvar = qvar
    
    def eval(self, env: Env) -> EIQOpt:
        return EIQOpt(IQOpt(self.qopt.eval(env).qopt, self.qvar.eval(env).qvar))
    
    def __str__(self) -> str:
        return str(self.qopt) + str(self.qvar)


    
class EIQOptAdd(EIQOptAbstract):
    '''
    The Expression for additions of Indexed Quantum Operators.
    
    EIQOptAdd ::= (a : IQOpt) '+' (b : IQOpt)

    Nonterminal.
    '''

    def __init__(self, ioptA : EIQOptAbstract, ioptB : EIQOptAbstract):
        ioptA.type_checking(IQOptType())
        ioptB.type_checking(IQOptType())

        super().__init__()

        self.ioptA = ioptA
        self.ioptB = ioptB

    def eval(self, env: Env) -> EIQOpt:
        return EIQOpt(self.ioptA.eval(env).iqopt + self.ioptB.eval(env).iqopt)
    
    def __str__(self) -> str:
        return "(" + str(self.ioptA) + "+" + str(self.ioptB) + ")"



class EIQOptNeg(EIQOptAbstract):
    '''
    The expression for negation of an indexed quantum operator.

    EIQOptNeg ::= '(' '-' (a : IQOpt) ')'
    
    Nonterminal.
    '''

    def __init__(self, iopt : EIQOptAbstract):
        iopt.type_checking(IQOptType())

        super().__init__()

        self.iopt = iopt
        

    def eval(self, env: Env) -> EIQOpt:
        return EIQOpt(- self.iopt.eval(env).iqopt)
    
    def __str__(self) -> str:
        return "(-" + str(self.iopt) + ")"
    


class EIQOptSub(EIQOptAbstract):
    '''
    The Expression for subtraction of Indexed Quantum Operators.
    
    EIQOptSub ::= (a : IQOpt) '-' (b : IQOpt)

    Nonterminal.
    '''

    def __init__(self, ioptA : EIQOptAbstract, ioptB : EIQOptAbstract):
        ioptA.type_checking(IQOptType())
        ioptB.type_checking(IQOptType())

        super().__init__()

        self.ioptA = ioptA
        self.ioptB = ioptB

    
    def eval(self, env: Env) -> EIQOpt:
        return EIQOpt(self.ioptA.eval(env).iqopt - self.ioptB.eval(env).iqopt)
    
    def __str__(self) -> str:
        return "(" + str(self.ioptA) + "-" + str(self.ioptB) + ")"


class EIQOptScale(EIQOptAbstract):
    '''
    The expression for scaling of quantum operators.

    EIQOptScale ::= (c : complex) (b : IQOpt)
                    | (c : complex) '*' (b : IQOpt)
    
    Nonterminal.
    '''

    def __init__(self, c : complex, iopt : EIQOptAbstract):
        iopt.type_checking(IQOptType())

        super().__init__()

        assert isinstance(c, (complex, float)), "ASSERTION FAILED"
        self.c = c
        self.iopt = iopt
    
    def eval(self, env: Env) -> EIQOpt:
        return EIQOpt(self.c * self.iopt.eval(env).iqopt)
    
    def __str__(self) -> str:
        return "(" + str(self.c) + " " + str(self.iopt) + ")"
    


class EIQOptMul(EIQOptAbstract):
    '''
    The Expression for multiplications of Indexed Quantum Operators.
    
    EIQOptMul ::= (a : IQOpt) '*' (b : IQOpt)

    Nonterminal.
    '''

    def __init__(self, ioptA : EIQOptAbstract, ioptB : EIQOptAbstract):
        ioptA.type_checking(IQOptType())
        ioptB.type_checking(IQOptType())

        super().__init__()

        self.ioptA = ioptA
        self.ioptB = ioptB

    def eval(self, env: Env) -> EIQOpt:
        return EIQOpt(self.ioptA.eval(env).iqopt @ self.ioptB.eval(env).iqopt)
    
    def __str__(self) -> str:
        return "(" + str(self.ioptA) + " " + str(self.ioptB) + ")"


class EIQOptDagger(EIQOptAbstract):
    '''
    The expression for the conjugate transpose of an indexed quantum operator.

    EIQOptDagger ::= (a : IQOpt) '^\\dagger'
                    | (a : IQOpt) '†'
    
    Nonterminal.
    '''

    def __init__(self, iopt : EIQOptAbstract):
        iopt.type_checking(IQOptType())

        super().__init__()

        self.iopt = iopt
    
    def eval(self, env: Env) -> EIQOpt:
        return EIQOpt(self.iopt.eval(env).iqopt.dagger())
        
    def __str__(self) -> str:
        return "(" + str(self.iopt) + "†" + ")"
    


class EIQOptTensor(EIQOptAbstract):
    '''
    The expression for tensor product of indexed quantum operators.

    EIQOptTensor ::= (a : IQOpt) '⊗' (b : IQOpt)
                    | (a : IQOpt) '\\otimes' (b : IQOpt)
    
    Nonterminal.
    '''

    def __init__(self, ioptA : EIQOptAbstract, ioptB : EIQOptAbstract):
        ioptA.type_checking(IQOptType())
        ioptB.type_checking(IQOptType())

        super().__init__()

        self.ioptA = ioptA
        self.ioptB = ioptB


    def eval(self, env: Env) -> EIQOpt:
        return EIQOpt(self.ioptA.eval(env).iqopt.tensor(self.ioptB.eval(env).iqopt))
    
    def __str__(self) -> str:
        return "(" + str(self.ioptA) + " ⊗ " + str(self.ioptB) + ")"
    



class EIQOptDisjunct(EIQOptAbstract):
    '''
    The expression for disjunction of projective indexed quantum operators.

    EIQOptDisjunct ::= (a : IQOpt) '\\vee' (b : IQOpt)
                    | (a : IQOpt) '∨' (b : IQOpt)
    
    Nonterminal.
    '''

    def __init__(self, ioptA : EIQOptAbstract, ioptB : EIQOptAbstract):
        ioptA.type_checking(IQOptType())
        ioptB.type_checking(IQOptType())

        super().__init__()

        self.ioptA = ioptA
        self.ioptB = ioptB
        
    def eval(self, env: Env) -> EIQOpt:
        return EIQOpt(self.ioptA.eval(env).iqopt | self.ioptB.eval(env).iqopt)
    
    def __str__(self) -> str:
        return "(" + str(self.ioptA) + " ∨ " + str(self.ioptB) + ")"
    

class EIQOptConjunct(EIQOptAbstract):
    '''
    The expression for conjunction of projective indexed quantum operators.

    EIQOptConjunct   ::= (a : IQOpt) '\\wedge' (b : IQOpt)
                    | (a : IQOpt) '∧' (b : IQOpt)
    
    Nonterminal.
    '''

    def __init__(self, ioptA : EIQOptAbstract, ioptB : EIQOptAbstract):
        ioptA.type_checking(IQOptType())
        ioptB.type_checking(IQOptType())

        super().__init__()

        self.ioptA = ioptA
        self.ioptB = ioptB

    
    def eval(self, env: Env) -> EIQOpt:
        return EIQOpt(self.ioptA.eval(env).iqopt & self.ioptB.eval(env).iqopt)
    
    def __str__(self) -> str:
        return "(" + str(self.ioptA) + " ∧ " + str(self.ioptB) + ")"
    


class EIQOptComplement(EIQOptAbstract):
    '''
    The expression for complement of projective quantum operators.

    EIQOptComplement ::= (a : IQOpt) '^\\bot'
                    | (a : IQOpt) '^⊥'
    
    Nonterminal.
    '''

    def __init__(self, iopt : EIQOptAbstract):
        iopt.type_checking(IQOptType())

        super().__init__()

        self.iopt = iopt
    
    def eval(self, env: Env) -> EIQOpt:
        return EIQOpt(~ self.iopt.eval(env).iqopt)
    
    def __str__(self) -> str:
        return "(" + str(self.iopt) + "^⊥)"
    


class EIQOptSasakiImply(EIQOptAbstract):
    '''
    The expression for Sasaki implication of projective quantum operators.

    EIQOptSasakiImply   ::= (a : IQOpt) '\\SasakiImply' (b : IQOpt)
                        | (a : IQOpt) '⇝' (b : IQOpt)
    
    Nonterminal.
    '''

    def __init__(self, ioptA : EIQOptAbstract, ioptB : EIQOptAbstract):
        ioptA.type_checking(IQOptType())
        ioptB.type_checking(IQOptType())

        super().__init__()

        self.ioptA = ioptA
        self.ioptB = ioptB

    
    def eval(self, env: Env) -> EIQOpt:
        return EIQOpt(self.ioptA.eval(env).iqopt.Sasaki_imply(self.ioptB.eval(env).iqopt))
    
    def __str__(self) -> str:
        return "(" + str(self.ioptA) + " ⇝ " + str(self.ioptB) + ")"
    

class EIQOptSasakiConjunct(EIQOptAbstract):
    '''
    The expression for Sasaki conjunction of projective quantum operators.

    EIQOptSasakiConjunct ::= (a : IQOpt) '\\SasakiConjunct' (b : IQOpt)
                        | (a : IQOpt) '⋒' (b : IQOpt)
    
    Nonterminal.
    '''

    def __init__(self, ioptA : EIQOptAbstract, ioptB : EIQOptAbstract):
        ioptA.type_checking(IQOptType())
        ioptB.type_checking(IQOptType())

        super().__init__()

        self.ioptA = ioptA
        self.ioptB = ioptB


    def eval(self, env: Env) -> EIQOpt:
        return EIQOpt(self.ioptA.eval(env).iqopt.Sasaki_conjunct(self.ioptB.eval(env).iqopt))
    
    def __str__(self) -> str:
        return "(" + str(self.ioptA) + " ⋒ " + str(self.ioptB) + ")"
    