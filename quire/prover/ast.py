# the abstract syntax tree for Rem language

from __future__ import annotations

from typing import Tuple
from qplcomp import *
from ..language import QWhileAst, AstPres

class CMDStack:
    '''
    A list of commands
    '''
    def __init__(self, stack: Tuple[RemAst, ...]):
        self.stack : Tuple[RemAst, ...] = stack

    def __add__(self, cmd: RemAst|CMDStack) -> CMDStack:
        if isinstance(cmd, RemAst):
            return CMDStack(self.stack + (cmd,))
        else:
            return CMDStack(self.stack + cmd.stack)
        

class RemAst:
    def __add__(self, cmd: RemAst|CMDStack) -> CMDStack:
        if isinstance(cmd, RemAst):
            return CMDStack((self, cmd))
        else:
            return CMDStack((self,) + cmd.stack)

class Pause(RemAst):
    def __init__(self):
        pass

class DefEQOpt(RemAst):
    def __init__(self, id: str, eqopt: EQOpt):
        self.id = id
        self.eqopt = eqopt

class DefEIQOpt(RemAst):
    def __init__(self, id: str, eiqopt: EIQOpt):
        self.id = id
        self.eiqopt = eiqopt

class DefCalc(RemAst):
    def __init__(self, id: str, statement: QWhileAst, eiqopt: EIQOpt):
        self.id = id
        self.statement = statement
        self.eiqopt = eiqopt

class DefProg(RemAst):
    def __init__(self, id: str, statement: QWhileAst):
        self.id = id
        self.statement = statement

class DefExtract(RemAst):
    def __init__(self, id: str, id2: str):
        self.id = id
        self.id2 = id2

class StartRefine(RemAst):
    def __init__(self, id: str, prescription: AstPres):
        self.id = id
        self.prescription = prescription

class StepStatement(RemAst):
    def __init__(self, statement: QWhileAst):
        self.statement = statement

class StepRefineSeq(RemAst):
    def __init__(self, mid_assertion: EIQOpt):
        self.mid_assertion = mid_assertion

class StepRefineIf(RemAst):
    def __init__(self, P: EIQOpt):
        self.P = P

class StepRefineWhile(RemAst):
    def __init__(self, P: EIQOpt, inv: EIQOpt):
        self.P = P
        self.inv = inv

class RefineWeakenPre(RemAst):
    def __init__(self, pre: EIQOpt):
        self.pre = pre

class RefineStrengthenPost(RemAst):
    def __init__(self, post: EIQOpt):
        self.post = post


class RefineChooseGoal(RemAst):
    def __init__(self, n: int):
        self.n = n

class MetaEnd(RemAst):
    def __init__(self):
        pass

class ShowId(RemAst):
    def __init__(self, id: str):
        self.id = id

class ShowDef(RemAst):
    def __init__(self):
        pass

class EvalId(RemAst):
    def __init__(self, id: str):
        self.id = id

class TestEQOptEQ(RemAst):
    def __init__(self, eqopt1: EQOpt, eqopt2: EQOpt):
        self.eqopt1 = eqopt1
        self.eqopt2 = eqopt2

class TestEQOptLEQ(RemAst):
    def __init__(self, eqopt1: EQOpt, eqopt2: EQOpt):
        self.eqopt1 = eqopt1
        self.eqopt2 = eqopt2

class TestEIQOptEQ(RemAst):
    def __init__(self, eiqopt1: EIQOpt, eiqopt2: EIQOpt):
        self.eiqopt1 = eiqopt1
        self.eiqopt2 = eiqopt2

class TestEIQOptLEQ(RemAst):
    def __init__(self, eiqopt1: EIQOpt, eiqopt2: EIQOpt):
        self.eiqopt1 = eiqopt1
        self.eiqopt2 = eiqopt2





