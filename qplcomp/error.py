'''

This file provides the error for the project.

'''
from __future__ import annotations
from typing import Type, Tuple

class QPLCompError(Exception):
    pass

def type_check(obj : object, target_type : Type | Tuple[Type, ...]) -> None:
    '''
    The method to check the type of this object. It will raise a TypeError if the type of expr is not target_type.
    '''
    if isinstance(target_type, tuple):
        for t in target_type:
            if isinstance(obj, t):
                return
        
        raise QPLCompError("The parameter expression '" + str(obj) + "' should be within type '" + str(target_type) + "', but has type '"+ str(type(obj)) + "'.")

    elif not isinstance(obj, target_type):
        raise QPLCompError("The parameter expression '" + str(obj) + "' should be of type '" + str(target_type) + "', but has type '"+ str(type(obj)) + "'.")
