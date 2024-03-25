
from __future__ import annotations
from typing import Any

from qplcomp import Env, prepare_env, EQOpt, QOpt, PLYError, EnvError, QPLCompError
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
    lexer : Any

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
        Prover.lexer.lineno = 1
        Env.restart()
        for id in opts:
            Env()[id] = EQOpt(QOpt(opts[id]))


    def __call__(self, code : str) -> None:
        '''
        Call the parser and operate the prover state.
        '''
        try:
            self.parser.parse(code, lexer = self.lexer)
        except PauseError:
            pass
        except (EnvError, PLYError, QPLCompError, QPVError) as e:
            self.state_bar = f"{e.__class__.__name__}: {e}"

    def process(self, code : str) -> None:
        '''
        Call the parser and operate the prover state.
        Errors are raised.
        '''
        try:
            self.parser.parse(code, lexer = self.lexer)
        except PauseError:
            print(f"Paused at line {self.lexer.lineno}.")
        except (EnvError, PLYError, QPLCompError, QPVError) as e:
            raise e.__class__(str(e) + f" (line {self.lexer.lineno})")


    @property
    def refine_proof(self) -> AstPres:
        if self.__refine_proof is None:
            raise QPVError("It is not currently inside a refinement.")
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
            raise QPVError("It is currently inside a refinement.")
        
        if not isinstance(ast, AstPres):
            raise QPVError("The program to be refined must be a prescription.")
        
        self.define(id, EAst(ast))

        self.__refine_proof = ast
        self.current_goals = [ast]

        self.state_bar = "Refinement starts."


    def end_refinement(self) -> None:
        '''
        It will check whether a refinement proof is finished and end it when it is.
        '''        
        if self.__refine_proof is None:
            raise QPVError("The prover is not in refinement model.")

        if len(self.current_goals) != 0:
            raise QPVError("Goals not clear.")
        
        
        self.__refine_proof = None

        self.state_bar = f"Refinement completed."


    def step_refine_wlp(self, SRefined : Ast) -> None:
        '''
        Refine the first goal in `self.current_goals` with SRefined.
        '''
        if len(self.current_goals) == 0:
            raise QPVError("There is no prescriptions to refine.")
        
        self.current_goals[0].refine_wlp(SRefined)

        self.current_goals = self.current_goals[0].get_prescription() + self.current_goals[1:]
        
        self.state_bar = "Refinement step succeeded."

    def step_refine_weaken_pre(self, R : Expr) -> None:
        if len(self.current_goals) == 0:
            raise QPVError("There is no prescriptions to refine.")
        
        self.current_goals[0].refine_weaken_pre(R)

        self.current_goals = self.current_goals[0].get_prescription() + self.current_goals[1:]
        
        self.state_bar = "Refinement step succeeded."


    def step_refine_strengthen_post(self, R : Expr) -> None:
        if len(self.current_goals) == 0:
            raise QPVError("There is no prescriptions to refine.")
        
        self.current_goals[0].refine_strengthen_post(R)

        self.current_goals = self.current_goals[0].get_prescription() + self.current_goals[1:]
        
        self.state_bar = "Refinement step succeeded."


    def step_refine_seq(self, middle : Expr) -> None:
        '''
        Refine the first goal in `self.current_goals` with SRefined.
        '''
        if len(self.current_goals) == 0:
            raise QPVError("There is no prescriptions to refine.")
        
        self.current_goals[0].refine_seq_break(middle)

        self.current_goals = self.current_goals[0].get_prescription() + self.current_goals[1:]        
        self.state_bar = "Refinement step succeeded."

    def step_refine_if(self, R : Expr) -> None:
        '''
        Refine the first goal in `self.current_goals` with SRefined.
        '''
        if len(self.current_goals) == 0:
            raise QPVError("There is no prescriptions to refine.")
        
        self.current_goals[0].refine_if(R)

        self.current_goals = self.current_goals[0].get_prescription() + self.current_goals[1:]        
        self.state_bar = "Refinement step succeeded."

    def step_refine_while(self, R : Expr, Inv : Expr) -> None:
        '''
        Refine the first goal in `self.current_goals` with SRefined.
        '''
        if len(self.current_goals) == 0:
            raise QPVError("There is no prescriptions to refine.")
        
        self.current_goals[0].refine_while(R, Inv)

        self.current_goals = self.current_goals[0].get_prescription() + self.current_goals[1:]        
        self.state_bar = "Refinement step succeeded."



    def refine_choose_goal(self, i : int) -> None:
        '''
        Choose the i-th goal
        '''
        if not 1 <= i <= len(self.current_goals):
            raise QPVError(f"Invalid goal number {i}. Choose a number from {1} to {len(self.current_goals)}. ")
        
        self.current_goals = [self.current_goals[i-1]] + self.current_goals[:i-1] + self.current_goals[i:]

        self.state_bar = "Goal switched."

    def test_eq(self, a : Expr, b : Expr) -> None:
        if a.eval() == b.eval():
            self.state_bar = f"Test Result: {a} = {b}"
        else:
            self.state_bar = f"Test Result: {a} ≠ {b}"

    def test_leq(self, a : Expr, b : Expr) -> None:
        try:
            if a.eval() <= b.eval():    # type: ignore
                self.state_bar = f"Test Result: {a} <= {b}"
            else:
                self.state_bar = f"Test Result: {a} </= {b}"
        except NotImplementedError:
            raise QPVError(f"The 'less than' relation is not supported for '{a}' and '{b}'.")

    #################################
    # printing
    def eval_id(self, id : str) -> None:
        res = Env()[id].eval()
        self.state_bar = f"Eval {id}: \n{res}"


    def show_id(self, id : str) -> None:
        self.state_bar = f"Show {id}: \n{Env()[id]}"

    def show_def(self) -> None:
        self.state_bar = f"Definitions: \n{Env().get_items()}"
    
    def get_defs(self) -> str:
        return Env().get_items_str(self.defined_var)
    

    def get_goals_str(self) -> str:
        if self.__refine_proof is None:
            return ""
        
        res = "-"*40 + "\n"
        res += "= Refinement Mode =\n"
        if len(self.current_goals) == 0:
            res += "\nGoal Clear.\n"
        else:
            for i in range(len(self.current_goals)):
                res += "\nGoal ({}/{})\n".format(i+1, len(self.current_goals))
                res += str(self.current_goals[i])
                res += "\n"
        return res
    
    def __str__(self) -> str:
        res = self.get_goals_str()
        res += "\n" + "-"*40 + "\n"
        res += f"= Info (line {self.lexer.lineno}) =\n\n" + self.state_bar + "\n"
        return res

######################################################################
# Interfaces

def prover_restart(opts : dict[str, np.ndarray] = {}) -> None:
    '''
    Restart the Quire prover.

    - `opts`: `dict[str, np.ndarray]`, the extra quantum operators.
    '''
    Prover.restart(opts)

def prover(input_code : str) -> None:
    '''
    Let the prover execute the code.

    - `input_code` : `str`.
    '''
    Prover().process(input_code)

def prover_info() -> str:
    '''
    Return the current state of the prover.
    '''
    return str(Prover())

def quire_code(input_code, opts: dict[str, np.ndarray] = {}) -> None:
    '''
    Start the qpv prover to process the code.

    - `input_code` : `str`, the code to be checked.
    - `opts`: `dic[str, np.ndarray]`, the extra quantum operators.
    - Returns: `None` if the check succeeds. Otherwise there will be an error.
    '''
    # restart and calculate
    Prover.restart(opts)
    Prover().process(input_code)

def quire_file(input_path : str, opts: dict[str, np.ndarray] = {}) -> None:
    '''
    Start the qpv prover to process the input file.

    - `input_path` : `str`, the path of the file to be checked.
    - `opts`: `dic[str, np.ndarray]`, the extra quantum operators.
    - Returns: `None` if the check succeeds. Otherwise there will be an error.
    '''

    with open(input_path, "r", encoding="utf-8") as p_in:
        code = p_in.read()

    # restart and calculate
    Prover.restart(opts)
    Prover().process(code)

