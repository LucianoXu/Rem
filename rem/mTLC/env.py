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
    symbol = "T"

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


    def type_checking(self, type : Types|Type[Types]) -> None:
        '''
        The method to check the type of this expression. It will raise a TypeError if the type of expr is not target_type.
        '''
        if isinstance(type, Types):
            if self.type != type:
                raise ValueError(f"The parameter expression '{self}' should have type '{type}', but actually has type '{self.type}'.")
        else:
            if not isinstance(self.type, type):
                raise ValueError(f"The parameter expression '{self}' should have type '{type.symbol}', but actually has type '{self.type}'.")
            
    def __hash__(self) -> int:
        return hash(str(self))
    
    def __eq__(self, other : Any) -> bool:
        return isinstance(other, TypedTerm) and str(self) == str(other)

class Var(TypedTerm):
    '''
    The class for typed variables.
    '''
    def __init__(self, id : str, env : Env):
        if not id in env.decs:
            raise TermError(f"The variable '{id}' is not declared.")
        
        super().__init__(env.decs[id])

        if not isinstance(id, str):
            raise TermError("The id for the variable should be a string.")
        
        self.id: str = id

    
    def eval(self, env: Env) -> TypedTerm:
        val = env[self.id].eval(env)

        if self.type != val.type:
            raise TermError(f"The variable '{self.id}' should be of type '{self.type}', but the value defined in the environment is of type '{val.type}'.")
        
        return val
    
    def __str__(self) -> str:
        return self.id
    
    def __hash__(self) -> int:
        return hash(self.id)

    def __eq__(self, other : Any) -> bool:
        return isinstance(other, Var) and self.id == other.id


class Env:
    '''
    The environment relates variable (string) to their definitions.
    '''

    DEFAULT_PREFIX = "X"

    def __init__(self) -> None:

        self.decs : dict[str, Types] = {}

        self.defs : dict[str, TypedTerm] = {}

    def __eq__(self, other : Env) -> bool:
        if self is other:
            return True
        return self.decs == other.decs and self.defs == other.defs

    def copy(self) -> Env:
        '''
        Return a shallow copy of this environment.
        '''
        res = Env()
        res.decs = self.decs.copy()
        res.defs = self.defs.copy()
        return res
    
    def sub_env(self, defs: set[str]) -> Env:
        '''
        Return a sub-environment with the definitions in `defs`.
        '''
        res = Env()

        for key in defs:
            if key in self.defs:
                res[key] = self.defs[key]

        return res        


    def _get_unique_name(self, prefix : str = DEFAULT_PREFIX) -> str:
        '''
        Return a key which is not used in the environment. The key will be in the form of `prefix` + number.

        Parameters: prefix = "VAL" : str.
        Returns: a key which is not used in this environment.
        '''
        n = 0
        res = prefix + str(n)
        n += 1
        while res in self.defs:
            res = prefix + str(n)
            n += 1
        return res


    def append(self, term : TypedTerm) -> str:
        '''
        Check whether the value already exists in this environment.
        If yes, return the corresponding key.
        If not, create a new item with an auto key and return the key used.
        '''
        
        for key in self.defs:
            if self.defs[key] == term:
                return key
            
        name = self._get_unique_name()

        self.decs[name] = term.type
        self.defs[name] = term

        return name
    
    def declare(self, name: str, t : Types) -> None:
        '''
        Declare a variable with a type.
        '''
        if name in self.decs:
            raise ValueError(f"The variable '{name}' has been declared.")
        
        if name in self.defs:
            raise ValueError(f"The variable '{name}' has been defined.")
        
        self.decs[name] = t
    
    def __setitem__(self, key : str, term : TypedTerm) -> None:

        if not isinstance(term, TypedTerm):
            raise ValueError("Invalid value. Only TypedTerm instances are allowed.")
        
        # check the type
        if key in self.decs:
            if self.decs[key] != term.type:
                raise ValueError(f"The variable '{key}' should have type '{self.decs[key]}', but the value has type '{term.type}'.")

        # it's not allowed to change the value.
        if key in self.defs:
            raise TermError(f"The variable '{str(key)}' has been defined.")

        self.decs[key] = term.type
        self.defs[key] = term

    def __getitem__(self, key : str) -> TypedTerm:
        if key not in self.defs:
            raise TermError(f"The variable '{key}' is not defined.")
        return self.defs[key]
    
    def __contains__(self, key : str) -> bool:
        return key in self.defs
    

    ##################################################################
    # output

    def get_items_str(self, varls : list[str] = []) -> str:
        if len(varls) == 0:
            varls = list(self.defs.keys())
        res = ""
        for key in varls:
            res += key + " := \n" + str(self.defs[key]) + "\n\n"
        return res
    
    def get_items(self) -> str:
        res = ""
        for key in self.defs:
            res += key + "\n"
        return res
    