from __future__ import annotations
from typing import Type

from ..env import TypedTerm, Env, Types

from ..qval import QSOpt

from abc import ABC, abstractmethod

import numpy as np


class QSOptType(Types):
    def __str__(self) -> str:
        return "QSOpt"
    
class EQSOptAbstract(TypedTerm, ABC):
    '''
    The expression for Quantum Super Operators.
    '''
    def __init__(self):
        super().__init__(QSOptType())
    
    @abstractmethod
    def eval(self, env: Env) -> EQSOpt:
        pass


class EQSOpt(EQSOptAbstract):

    def __init__(self, qso : QSOpt):
        super().__init__()

        assert isinstance(qso, QSOpt)
        self.qso = qso


    def eval(self, env: Env) -> EQSOpt:
        return self
    
    def __str__(self) -> str:
        return str(self.qso)



class EQSOptAdd(EQSOptAbstract):
    '''
    The expression for additions of quantum superoperators.

    EQSOptAdd ::= (a : QSOpt) '+' (b : QSOpt)
    '''

    def __init__(self, soA : EQSOptAbstract, soB : EQSOptAbstract):
        super().__init__()

        assert isinstance(soA, EQSOptAbstract)
        soA.type_checking(QSOptType())
        self.soA = soA

        assert isinstance(soB, EQSOptAbstract)
        soB.type_checking(QSOptType())
        self.soB = soB

    def eval(self, env: Env) -> EQSOpt:
        return EQSOpt(self.soA.eval(env).qso + self.soB.eval(env).qso)
    
    def __str__(self) -> str:
        return "(" + str(self.soA) + "+" + str(self.soB) + ")"
