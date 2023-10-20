
from __future__ import annotations
from typing import Any

from qplcomp import Env, prepare_env, EQOpt, QOpt
from ..language import *

from ply.yacc import ParserReflect

import numpy as np


class PauseError(Exception):
    pass

class Prover:
    '''
    The class that hosts the formal verification.
    '''
    __instance : Prover | None = None
    parser : Any

    def __new__(cls):
        if cls.__instance is None:
            prepare_env()
            cls.__instance = object.__new__(cls)
            
            cls.__instance.defined_var = []
            cls.__instance.__refine_proof = None
            cls.__instance.current_goals = []
            cls.__instance.state_bar = "Emtpy Prover."

        return cls.__instance
    
    def __init__(self):
        # all the variables defined in this Prover
        self.defined_var : list[str]
        self.__refine_proof : AstPres | None
        self.current_goals : list[AstPres]

        self.state_bar : str

    @staticmethod
    def restart(opts: dict[str, np.ndarray]):
        '''
        It restarts `Env` with these additional opts.
        '''
        Prover.__instance = None
        Env.restart()
        for id in opts:
            Env()[id] = EQOpt(QOpt(opts[id]))


    def __call__(self, code : str) -> None:
        '''
        Call the parser and operate the prover state.
        '''
        try:
            self.parser.parse(code)
        except PauseError:
            pass
        except Exception as e:
            self.state_bar = f"{e.__class__.__name__}: {e}"


    @property
    def refine_proof(self) -> AstPres:
        if self.__refine_proof is None:
            raise Exception("It is not currently inside a refinement.")
        return self.__refine_proof

    
    def define(self, var : str, obj : Expr):
        Env()[var] = obj
        self.defined_var.append(var)
        self.state_bar = f"Variable defined: {var}."


    def start_refinement(self, id : str, ast : AstPres) -> None:
        '''
        It will start a refinement proof.
        '''
        if self.__refine_proof is not None:
            raise Exception("It is currently inside a refinement.")
        
        if not isinstance(ast, AstPres):
            raise Exception("The program to be refined must be a prescription.")
        
        self.define(id, EAst(ast))

        self.__refine_proof = ast
        self.current_goals = [ast]

        self.state_bar = "Refinement starts."


    def end_refinement(self) -> None:
        '''
        It will check whether a refinement proof is finished and end it when it is.
        '''        
        if len(self.current_goals) != 0:
            raise Exception("Unfinished goals.")
        
        self.__refine_proof = None

        self.state_bar = f"Refinement completed."

    def step_refine(self, SRefined : Ast) -> None:
        '''
        Refine the first goal in `self.current_goals` with SRefined.
        '''
        if len(self.current_goals) == 0:
            raise Exception("There is no prescriptions to refine.")
        
        self.current_goals[0].refine(SRefined)

        self.current_goals = SRefined.get_prescription() + self.current_goals[1:]
        
        self.state_bar = "Refine step succeeded."
    
    def refine_choose_goal(self, i : int) -> None:
        '''
        Choose the i-th goal
        '''
        if not 1 <= i <= len(self.current_goals):
            raise Exception(f"Invalid goal number {i}. Choose a number from {1} to {len(self.current_goals)}. ")
        
        self.current_goals = [self.current_goals[i-1]] + self.current_goals[:i-1] + self.current_goals[i:]

        self.state_bar = "Goal switched."

    #################################
    # printing

    def show_id(self, id : str) -> None:
        self.state_bar = f"Show {id}:" + "\n" + str(Env()[id])
    
    def get_defs(self) -> str:
        return Env().get_items_str(self.defined_var)
    

    def get_goals_str(self) -> str:
        if self.__refine_proof is None:
            return "\nNot in Refinement Model.\n"
        
        if len(self.current_goals) == 0:
            return "\nGoal Clear.\n"
        res = ""
        for i in range(len(self.current_goals)):
            res += "\nGoal ({}/{})\n".format(i+1, len(self.current_goals))
            res += str(self.current_goals[i])
            res += "\n"
        return res
    
    def __str__(self) -> str:
        res = "-"*40 + "\n"
        res += self.get_goals_str()
        res += "\n" + "-"*40 + "\n"
        res += "= Info =\n" + self.state_bar + "\n"
        return res


def prover(code : str) -> None:
    Prover()(code)


