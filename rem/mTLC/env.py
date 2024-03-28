'''
env
=====

This package provides a simple variable system. It includes:

- class `TypedTerm`: the typed expressions of the system. More specific definition of expressions should be defined as its subclasses.
- class `Variable`: It is the expression constructed by a variable.
- class `Env`: environments for the variable system. It is a dictionary from identifiers (`str`) to its definitions (`TypedTerm`).

'''

from __future__ import annotations

from typing import Type, Any

from abc import ABC, abstractmethod

class TermError(Exception):
    pass

class Types(ABC):
    '''
    The class for types.
    '''
    @abstractmethod
    def __str__(self) -> str:
        pass

    def __eq__(self, other : Any) -> bool:
        return isinstance(other, Types) and str(self) == str(other)


class TypedTerm(ABC):
    '''
    The class for (typed) terms.
    Type checking is implemented in the construction of TypedTerm.
    '''

    def __init__(self, type: Types):
        if not isinstance(type, Types):
            raise TermError("The type should be a Types object.")
        self.type: Types = type

    def eval(self, env: Env) -> TypedTerm:
        '''
        Evaluate the term within the environment.
        '''
        return self
    
    @abstractmethod
    def __str__(self) -> str:
        pass


    def type_checking(self : TypedTerm, type : Types) -> None:
        '''
        The method to check the type of this expression. It will raise a TypeError if the type of expr is not target_type.
        '''
        if self.type != type and not isinstance(self.type, UncertainType):
            raise ValueError(f"The parameter expression '{self}' should have type '{type}', but actually has type '{self.type}'.")

class UncertainType(Types):
    '''
    The class for uncertain types.
    '''
    def __str__(self) -> str:
        return "Uncertain"

class Var(TypedTerm):
    '''
    The class for typed variables.
    '''
    def __init__(self, id : str, type : Types = UncertainType()):

        super().__init__(type)

        if not isinstance(id, str):
            raise TermError("The id for the variable should be a string.")
        
        self.id: str = id

    
    def eval(self, env: Env) -> TypedTerm:
        val = env[self.id].eval(env)

        if (not isinstance(self.type, UncertainType)) and self.type != val.type:
            raise TermError(f"The variable '{self.id}' should be of type '{self.type}', but the value defined in the environment is of type '{val.type}'.")
        
        return val
    
    def __str__(self) -> str:
        return self.id


class Env:
    '''
    The environment relates variable (string) to their definitions.
    '''

    DEFAULT_PREFIX = "X"

    def __init__(self) -> None:

        self._lib : dict[str, TypedTerm] = {}

    def copy(self) -> Env:
        '''
        Return a shallow copy of this environment.
        '''
        res = Env()
        res._lib = self._lib.copy()
        return res


    def get_unique_name(self, prefix : str = DEFAULT_PREFIX) -> str:
        '''
        Return a key which is not used in the environment. The key will be in the form of `prefix` + number.

        Parameters: prefix = "VAL" : str.
        Returns: a key which is not used in this environment.
        '''
        n = 0
        res = prefix + str(n)
        n += 1
        while res in self._lib:
            res = prefix + str(n)
            n += 1
        return res


    def append(self, term : TypedTerm) -> str:
        '''
        Check whether the value already exists in this environment.
        If yes, return the corresponding key.
        If not, create a new item with an auto key and return the key used.
        '''
        
        for key in self._lib:
            if self._lib[key] == term:
                return key
            
        name = self.get_unique_name()
        self._lib[name] = term
        return name
    
    def __setitem__(self, key : str, term : TypedTerm) -> None:
        if not isinstance(term, TypedTerm):
            raise ValueError("Invalid value. Only TypedTerm instances are allowed.")
        
        # it's not allowed to change the value.
        if key in self._lib:
            raise TermError(f"The variable '{str(key)}' has been defined.")

        self._lib[key] = term

    def __getitem__(self, key : str) -> TypedTerm:
        if key not in self._lib:
            raise TermError(f"The variable '{key}' is not defined.")
        return self._lib[key]
    
    def __contains__(self, key : str) -> bool:
        return key in self._lib
    

    ##################################################################
    # output

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
    