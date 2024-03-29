from __future__ import annotations

from typing import Type

from ...mTLC.env import Env

from ..qval import QVar
from ...mTLC.env import TypedTerm, Types

class QVarType(Types):
    def __str__(self) -> str:
        return "QVar"


class EQVar(TypedTerm):
    '''
    The expression for a literal quantum variable.

    Terminal.
    '''
    def __init__(self, qvar : QVar):
        super().__init__(QVarType())

        assert isinstance(qvar, QVar), "ASSERTION FAILED"
        self.qvar = qvar

    def eval(self, env: Env) -> EQVar:
        return self
    
    def __str__(self) -> str:
        return str(self.qvar)