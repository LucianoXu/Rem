from __future__ import annotations

from typing import Type

from ...mTLC.env import Env

from ..qval import QVar
from ...mTLC.env import TypedTerm, Types

class QVarType(Types):
    symbol = "QVar"
    
    def __init__(self, qnum: int):
        super().__init__()
        self.qnum = qnum

    def __str__(self) -> str:
        return f"QVar[{self.qnum}]"


class EQVar(TypedTerm):
    '''
    The expression for a literal quantum variable.

    Terminal.
    '''
    def __init__(self, qvar : QVar):
        self.type : QVarType = QVarType(qvar.qnum)

        assert isinstance(qvar, QVar), "ASSERTION FAILED"
        self.qvar = qvar

    def eval(self, env: Env) -> EQVar:
        return self
    
    def __str__(self) -> str:
        return str(self.qvar)
    
    def __hash__(self) -> int:
        return hash(tuple(self.qvar._qvls))
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, EQVar):
            return self.qvar == other.qvar
        return False