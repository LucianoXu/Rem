'''
env
=====

This package provides a simple variable system. It includes:

- class `Expr`: the typed expressions of the system. More specific definition of expressions should be defined as its subclasses.
- class `Variable`: It is the expression constructed by a variable.
- class `Env`: environments for the variable system. It is a dictionary from identifiers (`str`) to its definitions (`Expr`).

'''

from __future__ import annotations

from typing import Dict, Type

DEFAULT_PREFIX = "VAL"

# TODO : type information needed.

class EnvError(Exception):
    pass

class Expr:
    '''
    The class for expressions.
    The type checking is implemented in the construction of Expr.
    '''

    def __init__(self):
        '''
        parameter env: ever expression lives in some particular environment.

        TODO #2
        '''
    
    @property
    def T(self) -> None | Type:
        raise NotImplementedError()
    
    def eval(self) -> object:
        '''
        Calculate the value of this varible within the environment.

        Note: this is going to be a complete calculation, which is different from partial reductions.
        '''
        raise NotImplementedError()
    
    def __str__(self) -> str:
        raise NotImplementedError()
    
class Variable(Expr):
    '''
    The class for variables. Variables can be of any type, and can be replaced by beta-reduction.
    '''
    def __init__(self, id : str, T : None | Type = None):
        '''
        Construct a Variable expression.

        The type of it can be `None`, meaning that it's type is not determined yet.
        '''

        if not isinstance(id, str):
            raise EnvError("The id for the variable should be a string.")
        if not isinstance(T, Type) and T is not None:
            raise EnvError("The type T should be a Type or the None object.")
        
        self._id = id
        self._T = T

    
    @property
    def T(self) -> None | Type:
        if self._T is not None:
            return self._T
        
        elif self._id in Env():
            return Env()[self._id].T
        
        else:
            return None

    def eval(self):
        val = Env()[self._id].eval()

        if self.T is not None:
            if not isinstance(val, self.T):
                raise EnvError("The variable '" + self._id + "' should be of type '" + str(self.T) + "', but the value defined in the environment is of type '" + str(type(val)) + "'.")
        
        return val
    
    def __str__(self) -> str:
        return self._id


def expr_type_check(expr : Expr, target_type : Type) -> None:
    '''
    The method to check the type of this expression. It will raise a TypeError if the type of expr is not target_type.
    '''
    if expr.T is not None and expr.T != target_type:
        raise EnvError("The parameter expression '" + str(expr) + "' should be of type '" + str(target_type) + "', but is of type '"+ str(expr.T) + "'.")

class Env:
    '''
    The environment relates variable (string) to their definitions.
    singleton model
    '''
    __instance : Env | None = None
    def __new__(cls):
        '''
        Initializing an empty value environment.
        '''
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
            cls.__instance._lib = {}
            # the number for auto naming
            cls.__instance._numbering = 0
        return cls.__instance


    def __init__(self) -> None:

        self._lib : Dict[str, Expr]
        self._numbering : int

    @staticmethod
    def restart():
        Env.__instance = None

    def get_name(self, prefix : str = DEFAULT_PREFIX) -> str:
        '''
        Return a key which is not used in the environment. The key will be in the form of `prefix` + number.

        Parameters: prefix = "VAL" : str.
        Returns: a key which is not used in this environment.
        '''
        res = prefix + str(self._numbering)
        self._numbering += 1
        while res in self._lib:
            res = prefix + str(self._numbering)
            self._numbering += 1
        return res


    def append(self, expr : Expr) -> str:
        '''
        Check whether the value already exists in this environment.
        If yes, return the corresponding key.
        If not, create a new item with an auto key and return the key used.
        '''
        
        for key in self._lib:
            if self._lib[key] == expr:
                return key
            
        name = self.get_name()
        self._lib[name] = expr
        return name
    
    def __setitem__(self, key : str, expr : Expr) -> None:
        if not isinstance(expr, Expr):
            raise ValueError("Invalid value. Only Expr instances are allowed.")
        
        # it's not allowed to change the value.
        if key in self._lib:
            raise EnvError(f"The variable '{str(key)}' has been defined.")

        self._lib[key] = expr

    def __getitem__(self, key : str) -> Expr:
        if key not in self._lib:
            raise EnvError(f"The variable '{key}' is not defined.")
        return self._lib[key]
    
    def __contains__(self, key : str) -> bool:
        return key in self._lib
    
    def get_items_str(self, varls : list[str] = []) -> str:
        if len(varls) == 0:
            varls = list(self._lib.keys())
        res = ""
        for key in varls:
            res += key + " := \n" + str(self._lib[key]) + "\n\n"
        return res
    
    def get_items(self) -> str:
        res = ""
        for key in self._lib:
            res += key + "\n"
        return res
    