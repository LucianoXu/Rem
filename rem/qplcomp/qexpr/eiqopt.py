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

    @property
    def all_qvar(self) -> QVar:
        raise NotImplementedError()

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

    @property
    def all_qvar(self) -> QVar:
        return self.iqopt.qvar
    
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

    @property
    def all_qvar(self) -> QVar:
        return self.qvar.qvar
    
    def __hash__(self) -> int:
        return hash(("iqopt-pair", self.qopt, self.qvar))
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, EIQOptPair):
            return self.qopt == other.qopt and self.qvar == other.qvar
        return False
    
    
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
    
    @property
    def all_qvar(self) -> QVar:
        return self.ioptA.all_qvar + self.ioptB.all_qvar

    def __hash__(self) -> int:
        return hash(("iqopt-add", self.ioptA, self.ioptB))
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, EIQOptAdd):
            return self.ioptA == other.ioptA and self.ioptB == other.ioptB
        return False


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
    
    @property
    def all_qvar(self) -> QVar:
        return self.iopt.all_qvar
    
    def __hash__(self) -> int:
        return hash(("iqopt-neg", self.iopt))
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, EIQOptNeg):
            return self.iopt == other.iopt
        return False



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

    @property
    def all_qvar(self) -> QVar:
        return self.ioptA.all_qvar + self.ioptB.all_qvar

    def __hash__(self) -> int:
        return hash(("iqopt-sub", self.ioptA, self.ioptB))
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, EIQOptSub):
            return self.ioptA == other.ioptA and self.ioptB == other.ioptB
        return False

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
    
    @property
    def all_qvar(self) -> QVar:
        return self.iopt.all_qvar
    
    def __hash__(self) -> int:
        return hash(("iqopt-scale", self.c, self.iopt))
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, EIQOptScale):
            return self.c == other.c and self.iopt == other.iopt
        return False

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

    @property
    def all_qvar(self) -> QVar:
        return self.ioptA.all_qvar + self.ioptB.all_qvar
    
    def __hash__(self) -> int:
        return hash(("iqopt-mul", self.ioptA, self.ioptB))
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, EIQOptMul):
            return self.ioptA == other.ioptA and self.ioptB == other.ioptB
        return False

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
    

    @property
    def all_qvar(self) -> QVar:
        return self.iopt.all_qvar
    
    def __hash__(self) -> int:
        return hash(("iqopt-dagger", self.iopt))
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, EIQOptDagger):
            return self.iopt == other.iopt
        return False

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
    
    @property
    def all_qvar(self) -> QVar:
        return self.ioptA.all_qvar + self.ioptB.all_qvar
    
    def __hash__(self) -> int:
        return hash(("iqopt-tensor", self.ioptA, self.ioptB))
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, EIQOptTensor):
            return self.ioptA == other.ioptA and self.ioptB == other.ioptB
        return False

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
    
    @property
    def all_qvar(self) -> QVar:
        return self.ioptA.all_qvar + self.ioptB.all_qvar
    
    def __hash__(self) -> int:
        return hash(("iqopt-disjunct", self.ioptA, self.ioptB))
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, EIQOptDisjunct):
            return self.ioptA == other.ioptA and self.ioptB == other.ioptB
        return False
    
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
    
    @property
    def all_qvar(self) -> QVar:
        return self.ioptA.all_qvar + self.ioptB.all_qvar
    
    def __hash__(self) -> int:
        return hash(("iqopt-conjunct", self.ioptA, self.ioptB))
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, EIQOptConjunct):
            return self.ioptA == other.ioptA and self.ioptB == other.ioptB
        return False

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
    
    @property
    def all_qvar(self) -> QVar:
        return self.iopt.all_qvar
    
    def __hash__(self) -> int:
        return hash(("iqopt-complement", self.iopt))
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, EIQOptComplement):
            return self.iopt == other.iopt
        return False

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
    
    @property
    def all_qvar(self) -> QVar:
        return self.ioptA.all_qvar + self.ioptB.all_qvar
    
    def __hash__(self) -> int:
        return hash(("iqopt-sasaki-imply", self.ioptA, self.ioptB))
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, EIQOptSasakiImply):
            return self.ioptA == other.ioptA and self.ioptB == other.ioptB
        return False

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
    
    @property
    def all_qvar(self) -> QVar:
        return self.ioptA.all_qvar + self.ioptB.all_qvar
    
    def __hash__(self) -> int:
        return hash(("iqopt-sasaki-conjunct", self.ioptA, self.ioptB))
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, EIQOptSasakiConjunct):
            return self.ioptA == other.ioptA and self.ioptB == other.ioptB
        return False