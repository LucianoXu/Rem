from __future__ import annotations
from typing import Type, Any

from ...mTLC.env import TypedTerm, Env, Types

from ..qval import QVec

from abc import ABC, abstractmethod

import numpy as np

class QVecType(Types):
    symbol = "QVec"
    
    def __init__(self, qnum: int):
        super().__init__()
        self.qnum = qnum

    def __str__(self) -> str:
        return f"QVec[{self.qnum}]"
    
    def __eq__(self, other: Any) -> bool:
        return isinstance(other, QVecType) and self.qnum == other.qnum

class EQVecAbstract(TypedTerm, ABC):
    '''
    The expression for quantum vectors.
    '''

    def __init__(self, qnum: int):
        self.type: QVecType = QVecType(qnum)

    @abstractmethod
    def eval(self, env: Env) -> EQVec:
        pass
    
    
class EQVec(EQVecAbstract):
    def __init__(self, qvec : QVec):
        super().__init__(qvec.qnum)

        assert isinstance(qvec, QVec), "ASSERTION FAILED"
        self.qvec = qvec
    
    def eval(self, env: Env) -> EQVec:
        return self

    def __str__(self) -> str:
        return str(self.qvec)
    
class EQVecBitString(EQVec):
    '''
    The expression for quantum vectors.

    Terminal.
    '''

    def __init__(self, bitstr : str):
        super().__init__(QVec(bitstr))

        self.bitstr = bitstr
    
    def __str__(self) -> str:
        return f"|{self.bitstr}>"
        
    
class EQVecAdd(EQVecAbstract):
    '''
    The expression for additions of quantum vectors.

    EQVecAdd ::= (a : QVec) '+' (b : QVec)
    
    Nonterminal.
    '''

    def __init__(self, vec1 : EQVecAbstract, vec2 : EQVecAbstract):

        vec1.type_checking(QVecType)
        vec2.type_checking(QVecType)

        if not vec1.type.qnum == vec2.type.qnum:
            raise ValueError("The quantum numbers of the two vectors should be the same.")

        super().__init__(vec1.type.qnum)

        self.vec1 = vec1
        self.vec2 = vec2

    def eval(self, env: Env) -> EQVec:
        vec1_eval = self.vec1.eval(env)
        vec2_eval = self.vec2.eval(env)
        return EQVec(vec1_eval.qvec + vec2_eval.qvec)

    def __str__(self) -> str:
        return str(self.vec1) + " + " + str(self.vec2)
    
     

class EQVecScale(EQVecAbstract):
    '''
    The expression for scaling of quantum vectors.

    EQOptVec ::= (c : complex) (v : QVec)
                | (c : complex) '*' (v : QVec)
    
    Nonterminal.
    '''

    def __init__(self, c : complex, vec : EQVecAbstract):
        vec.type_checking(QVecType)

        super().__init__(vec.type.qnum)

        assert isinstance(c, (complex, float)), "ASSERTION FAILED"
        self.c = c
        self.vec = vec

    def eval(self, env: Env) -> EQVec:
        vec_eval = self.vec.eval(env)
        return EQVec(self.c * vec_eval.qvec)

    def __str__(self) -> str:
        return str(self.c) + " " + str(self.vec)
   