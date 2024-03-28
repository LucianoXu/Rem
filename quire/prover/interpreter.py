
from __future__ import annotations
from typing import Any

from qplcomp import Env, prepare_env, EQOpt, QOpt, PLYError, QPLCompError
from ..language import AstPres, TypedTerm, ValueError

from .ast import *

import numpy as np


class Frame:
    '''
    A exclusive proof frame of the prover.
    '''
    def __init__(self, env: Env, 
                 refine_proof: AstPres|None, 
                 current_goals: list[AstPres],
                 info: str | Exception = ""):
        self.env : Env = env.copy()
        self.refine_proof = refine_proof
        self.current_goals = current_goals.copy()
        self.info : str | Exception = info

    def copy(self) -> Frame:
        return Frame(
            self.env, 
            self.refine_proof, 
            self.current_goals,
            self.info)
    
    def __str__(self) -> str:
        return f"Frame: {self.info}\n{self.env}"


class Interpreter:
    @staticmethod
    def exe(cmd: RemAst, frame: Frame) -> Frame:
        '''
        Execute a command in the frame.
        Return the result frame.
        '''
        new_frame = frame.copy()

        if isinstance(cmd, DefEQOpt):
            new_frame.env[cmd.id] = cmd.eqopt
            new_frame.info = f"Defined EQOpt {cmd.id}."
            
        else:
            raise Exception()

        return new_frame