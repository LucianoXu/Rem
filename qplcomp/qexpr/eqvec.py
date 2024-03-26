from __future__ import annotations
from typing import Type

from ..env import TypedTerm, Env, Types

from ..qval import QVec

from abc import ABC, abstractmethod

import numpy as np

class QVecType(Types):
    def __str__(self) -> str:
        return "QVec"

class EQVecAbstract(TypedTerm, ABC):
    '''
    The expression for quantum vectors.
    '''

    def __init__(self):
        super().__init__(QVecType())

    @abstractmethod
    def eval(self, env: Env) -> EQVec:
        pass
    
    
class EQVec(EQVecAbstract):
    def __init__(self, qvec : QVec):
        super().__init__()

        assert isinstance(qvec, QVec)
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
        super().__init__()

        assert isinstance(vec1, EQVecAbstract)
        vec1.type_checking(QVecType())
        self.vec1 = vec1

        assert isinstance(vec2, EQVecAbstract)
        vec1.type_checking(QVecType())
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
        super().__init__()

        assert isinstance(c, (complex, float))
        self.c = c

        assert isinstance(vec, EQVecAbstract)
        
        vec.type_checking(QVecType())
        self.vec = vec

    def eval(self, env: Env) -> EQVec:
        vec_eval = self.vec.eval(env)
        return EQVec(self.c * vec_eval.qvec)

    def __str__(self) -> str:
        return str(self.c) + " " + str(self.vec)
   