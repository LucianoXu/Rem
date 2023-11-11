from __future__ import annotations
from typing import Type

from ..error import type_check
from ..env import Expr, Env, expr_type_check

from ..qval import QVec


import numpy as np

class EQVecBitString(Expr):
    '''
    The expression for quantum vectors.

    Terminal.
    '''

    def __init__(self, bitstr : str):
        
        type_check(bitstr, str)
        self._qvec = QVec(bitstr)
        self._bitstr = bitstr

    @property
    def T(self) -> Type:
        return QVec
    
    def eval(self) -> object:
        return self._qvec
    
    def __str__(self) -> str:
        return f"|{self._bitstr}>"
    
class EQVecAdd(Expr):
    '''
    The expression for additions of quantum vectors.

    EQVecAdd ::= (a : QVec) '+' (b : QVec)
    
    Nonterminal.
    '''

    def __init__(self, vec1 : Expr, vec2 : Expr):
        type_check(vec1, Expr)
        expr_type_check(vec1, QVec)
        self._vec1 = vec1

        type_check(vec2, Expr)
        expr_type_check(vec2, QVec)
        self._vec2 = vec2

    @property
    def T(self) -> Type:
        return QVec

    
    def eval(self) -> object:
        return self._vec1.eval() + self._vec2.eval()    # type: ignore
    

    def __str__(self) -> str:
        return str(self._vec1) + " + " + str(self._vec2)
    
     

class EQVecScale(Expr):
    '''
    The expression for scaling of quantum vectors.

    EQOptVec ::= (c : complex) (v : QVec)
                | (c : complex) '*' (v : QVec)
    
    Nonterminal.
    '''

    def __init__(self, c : complex, vec : Expr):

        type_check(c, (complex, float))
        self._c = c

        type_check(vec, Expr)
        expr_type_check(vec, QVec)
        self._vec = vec

    ##################################
    # Expression settings

    @property
    def T(self) -> Type:
        return QVec
    
    def eval(self) -> object:
        return self._c * self._vec.eval() # type: ignore
    
    def __str__(self) -> str:
        return str(self._c) + " " + str(self._vec)
    
    ##################################