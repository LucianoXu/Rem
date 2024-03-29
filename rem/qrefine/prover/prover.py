
from __future__ import annotations

from ...qplcomp import Env

from .ast import *
from .interpreter import *



class Prover:
    '''
    The object that interprates language, store the frames and host the formal verification.
    '''
    def __init__(self, env: Env):
        self.frame_stack : list[Frame] = [Frame(env, '', None, "Empty Prover.")]

    @property
    def current_frame(self) -> Frame:
        return self.frame_stack[-1]
    
    def __str__(self) -> str:
        return str(self.current_frame)

    
    def execute(self, cmd: RemAst) -> None:
        '''
        Push a command to the current frame.
        '''
        self.frame_stack.append(
            Interpreter.exe(cmd, self.current_frame)
        )

    def pop_frame(self) -> None:
        '''
        Pop the current frame.
        '''
        self.frame_stack.pop()

