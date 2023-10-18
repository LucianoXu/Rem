
from __future__ import annotations


from qplcomp import Env, prepare_env
from ..language import Ast

class Prover:
    '''
    The class that hosts the formal verification.
    '''
    __instance : Prover | None = None

    def __new__(cls):
        if cls.__instance is None:
            prepare_env()
            cls.__instance = object.__new__(cls)

            cls.__instance.refine_proof = None
            cls.__instance.current_goals = []

        return cls.__instance
    
    def __init__(self):
        self.refine_proof : Ast | None
        self.current_goals : list[Ast]
    
    def define(self, var : str, obj):
        Env()[var] = obj

    