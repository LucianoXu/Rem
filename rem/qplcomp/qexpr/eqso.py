from __future__ import annotations
from typing import Type

from ...mTLC.env import TypedTerm, Env, Types

from ..qval import QSOpt

from abc import ABC, abstractmethod

import numpy as np


class QSOptType(Types):
    symbol = "QSOpt"

    def __init__(self, qnum: int):
        super().__init__()
        self.qnum = qnum

    def __str__(self) -> str:
        return f"QSOpt[{self.qnum}]"
    
class EQSOptAbstract(TypedTerm, ABC):
    '''
    The expression for Quantum Super Operators.
    '''
    def __init__(self, qnum: int):
        self.type: QSOptType = QSOptType(qnum)
    
    @abstractmethod
    def eval(self, env: Env) -> EQSOpt:
        pass


class EQSOpt(EQSOptAbstract):

    def __init__(self, qso : QSOpt):
        super().__init__(qso.qnum)

        assert isinstance(qso, QSOpt), "ASSERTION FAILED"
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
        soA.type_checking(QSOptType)
        soB.type_checking(QSOptType)

        if soA.type.qnum != soB.type.qnum:
            raise ValueError(f"The quantum number of the two superoperators should be the same, but actually {soA.type.qnum} and {soB.type.qnum}.")
        super().__init__(soA.type.qnum)

        self.soA = soA
        self.soB = soB

    def eval(self, env: Env) -> EQSOpt:
        return EQSOpt(self.soA.eval(env).qso + self.soB.eval(env).qso)
    
    def __str__(self) -> str:
        return "(" + str(self.soA) + "+" + str(self.soB) + ")"
