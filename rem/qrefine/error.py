'''

This file provides the error for the project.

'''

from typing import Type

class ValueError(Exception):
    pass

def type_check(obj : object, target_type : Type) -> None:
    '''
    The method to check the type of this object. It will raise a TypeError if the type of expr is not target_type.
    '''
    if not isinstance(obj, target_type):
        raise ValueError("The parameter expression '" + str(obj) + "' should be of type '" + str(target_type) + "', but is of type '"+ str(type(obj)) + "'.")
