
from __future__ import annotations
from typing import Sequence

from ..error import QPLCompError

from .. import linalgPP

import numpy as np

from .val import QVal

class QVec(QVal):
    '''
    The class to represent quantum vectors.
    '''

    def __init__(self, data : np.ndarray | str):
        '''
        Construct a QVec instance with the given data.

        Parameters
            - data: 
                - `np.ndarray`, two options:
                    - a tensor representation of the QVec
                    - a vector representation of the QVec
                - `str`, a bitstring.
        '''
        
        # the tensor representation of this quantum vector
        self._tensor_repr : np.ndarray 

        # the vector representation of this quantum vector
        self._vector_repr : np.ndarray

        # the qubit number
        self._qnum : int

        if isinstance(data, str):
            self._qnum = len(data)
            idx = int(data, base=2)

            self._vector_repr = np.zeros((2**self._qnum,))
            self._vector_repr[idx] = 1.

            self._tensor_repr = np.reshape(self._vector_repr, (2,)*self._qnum)

        elif isinstance(data, np.ndarray):
            if len(data.shape) == 2:

                # check whether dim = 2**n for some n
                self._qnum = round(np.log2(len(data)))
                if (2**self._qnum != len(data)):
                    raise QPLCompError(f"Incorrect vector dimension: {len(data)} should be some power of 2.")
                
                self._vector_repr = data
                self._tensor_repr = np.reshape(self._vector_repr, (2,)*self._qnum)
            else:
                for d in data.shape:
                    if d != 2:
                        raise QPLCompError(f"Incorrect tensor shape: {data.shape} has indices of dimension other than 2.")
                self._qnum = len(data.shape)
                self._vector_repr = data.reshape((2**self._qnum,))
                self._tensor_repr = data

        else:
            raise Exception()



    @property
    def t_repr(self) -> np.ndarray:
        '''
        Return the tensor representation of this quantum vector.
        '''
        return self._tensor_repr

    @property
    def v_repr(self) -> np.ndarray:
        '''
        Return the vector representation of this quantum vector.
        '''
        return self._vector_repr
    
    def __str__(self) -> str:
        return str(self.v_repr)
    

    def __eq__(self, other) -> bool:
        if not isinstance(other, QVec):
            return False
        
        if self.qnum != other.qnum:
            return False
        
        return linalgPP.close_equal(self.v_repr, other.v_repr, QVal.prec)
    
    @property
    def qnum(self) -> int:
        return self._qnum


    def __add__(self, other : QVec) -> QVec:
        '''
        Calculate and return the addition result of self and other.
        Operators must be of the same qubit number.
        - Parameters: `self`, `other` : `QVec`.
        - Returns: `QVec`.
        '''

        assert isinstance(other, QVec)
        if self.qnum != other.qnum:
            raise QPLCompError(f"Inconsistent qubit number: {self.qnum} and {other.qnum}. The two QVec should have the same number of qubit numbers.")
        
        return QVec(self.t_repr + other.t_repr)
    


    def neg(self) -> QVec:
        '''
        Calculate and return the negation of this QVec instance.
        
        Parameters: none.
        Returns: QVec, the result.
        '''
        return QVec(-self.t_repr)
    

    def __neg__(self) -> QVec:
        return self.neg()
    

    def __sub__(self, other : QVec) -> QVec:
        '''
        Calculate and return the subtraction result of self and other.
        Operators must be of the same qubit number.
        - Parameters: `self`, `other` : `QVec`.
        - Returns: `QVec`.
        '''
        return self + (- other)
    
    def conj(self) -> QVec:
        '''
        Return the conjugate quantum vector.
        '''
        return QVec(self.t_repr.conj())
    

    def scale(self, c : complex | float) -> QVec:
        '''
        Calculate and return the scaling of `c * self'.

        Parameters: 
            - `self` : `QVec`.
            - `c` : `float`, the scalar.
        Returns: `QVec`, the result.
        '''

        return QVec(self.t_repr * c)
    
    def __mul__(self, other : complex | float) -> QVec:
        return self.scale(other)
    def __rmul__(self, other : complex | float) -> QVec:
        return self.scale(other)
