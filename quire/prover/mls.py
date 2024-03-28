
from qplcomp.env import Env
from qplcomp.qexpr.lexer_def import LexingError
from .ast import RemAst, ParsingError

from .prover_parsing_build import parser, parse_sentence, ParserState

from .prover import Prover

import numpy as np

class MLS:
    '''
    A micro language server for Rem langauge.

    it integrates the parser, pass input to prover and pass the output to TUI
    '''

    def __init__(self, env: Env):
        self.prover = Prover(env)

        self.cmd_stack: list[RemAst] = []

        # the index of the last charactor of the command (typically, '.')
        self.code_stack: list[str] = []  

        self.current_frame = -1

        self._info = ""

    @property
    def verified_code(self) -> str:
        return ''.join(self.code_stack)

    @property
    def prover_info(self) -> str:
        return str(self.prover)

    @property
    def info(self) -> str:
        return str(self._info)
    
    def __len__(self) -> int:
        return len(self.cmd_stack)

    def step_forward(self, new_code: str) -> str | None:
        '''
        step forward

        If succeeded, return the unparsed code. Else return None.
        '''

        self._info = ''
        
        # STEP 1, parse the command
        res, remaining = parse_sentence(new_code)

        if isinstance(res, Exception):
            self._info = res
            return None
        
        # res: tuple[RemAst, str]

        # STEP 2, execute the command
        try:
            self.prover.execute(res[0])
        except Exception as e:
            self._info = e
            return None

        self.cmd_stack.append(res[0])
        self.code_stack.append(res[1])

        # focus on the latest frame
        self.current_frame = len(self) - 1

        return remaining

    def step_backward(self) -> str|None:
        '''
        step backward

        if succeeded, return the code popped. Else return None.
        '''
        if len(self) == 0:
            self._info = "No more steps to go back."
            return None
        
        else:
            res = self.code_stack.pop()
            self.cmd_stack.pop()
            self.prover.pop_frame()

        # adjust current_frame
        if self.current_frame >= len(self):
            self.current_frame = len(self) - 1

        return res
