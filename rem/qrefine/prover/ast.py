# the abstract syntax tree for Rem language

from __future__ import annotations

from ...qplcomp import *
from ..language import QWhileAst, AstPres

from abc import ABC, abstractmethod
        

class RemAst(ABC):
    
    @abstractmethod
    def __eq__(self, __value: object) -> bool:
        pass

class Pause(RemAst):
    def __init__(self):
        pass

    def __eq__(self, __value: object) -> bool:
        return isinstance(__value, Pause)

class DefEQOpt(RemAst):
    def __init__(self, id: str, eqopt: EQOpt):
        self.id = id
        self.eqopt = eqopt

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, DefEQOpt):
            return self.id == __value.id and self.eqopt == __value.eqopt
        return False

class DefEIQOpt(RemAst):
    def __init__(self, id: str, eiqopt: EIQOpt):
        self.id = id
        self.eiqopt = eiqopt

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, DefEIQOpt):
            return self.id == __value.id and self.eiqopt == __value.eiqopt
        return False

class DefCalc(RemAst):
    def __init__(self, id: str, statement: QWhileAst, eiqopt: EIQOpt):
        self.id = id
        self.statement = statement
        self.eiqopt = eiqopt

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, DefCalc):
            return self.id == __value.id and self.statement == __value.statement and self.eiqopt == __value.eiqopt
        return False

class DefProg(RemAst):
    def __init__(self, id: str, statement: QWhileAst):
        self.id = id
        self.statement = statement

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, DefProg):
            return self.id == __value.id and self.statement == __value.statement
        return False

class DefExtract(RemAst):
    def __init__(self, id: str, id2: str):
        self.id = id
        self.id2 = id2

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, DefExtract):
            return self.id == __value.id and self.id2 == __value.id2
        return False

class StartRefine(RemAst):
    def __init__(self, id: str, prescription: AstPres):
        self.id = id
        self.prescription = prescription

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, StartRefine):
            return self.id == __value.id and self.prescription == __value.prescription
        return False

class StepStatement(RemAst):
    def __init__(self, statement: QWhileAst):
        self.statement = statement

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, StepStatement):
            return self.statement == __value.statement
        return False

class StepRefineSeq(RemAst):
    def __init__(self, mid_assertion: EIQOpt):
        self.mid_assertion = mid_assertion

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, StepRefineSeq):
            return self.mid_assertion == __value.mid_assertion
        return False
    
class StepRefineIf(RemAst):
    def __init__(self, P: EIQOpt):
        self.P = P

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, StepRefineIf):
            return self.P == __value.P
        return False

class StepRefineWhile(RemAst):
    def __init__(self, P: EIQOpt, inv: EIQOpt):
        self.P = P
        self.inv = inv

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, StepRefineWhile):
            return self.P == __value.P and self.inv == __value.inv
        return False

class RefineWeakenPre(RemAst):
    def __init__(self, pre: EIQOpt):
        self.pre = pre

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, RefineWeakenPre):
            return self.pre == __value.pre
        return False

class RefineStrengthenPost(RemAst):
    def __init__(self, post: EIQOpt):
        self.post = post

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, RefineStrengthenPost):
            return self.post == __value.post
        return False


class RefineChooseGoal(RemAst):
    def __init__(self, n: int):
        self.n = n

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, RefineChooseGoal):
            return self.n == __value.n
        return False

class MetaEnd(RemAst):
    def __init__(self):
        pass

    def __eq__(self, __value: object) -> bool:
        return isinstance(__value, MetaEnd)

class ShowId(RemAst):
    def __init__(self, id: str):
        self.id = id

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, ShowId):
            return self.id == __value.id
        return False

class ShowDef(RemAst):
    def __init__(self):
        pass

    def __eq__(self, __value: object) -> bool:
        return isinstance(__value, ShowDef)

class EvalId(RemAst):
    def __init__(self, id: str):
        self.id = id

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, EvalId):
            return self.id == __value.id
        return False

class TestEQOptEQ(RemAst):
    def __init__(self, eqopt1: EQOpt, eqopt2: EQOpt):
        self.eqopt1 = eqopt1
        self.eqopt2 = eqopt2

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, TestEQOptEQ):
            return self.eqopt1 == __value.eqopt1 and self.eqopt2 == __value.eqopt2
        return False

class TestEQOptLEQ(RemAst):
    def __init__(self, eqopt1: EQOpt, eqopt2: EQOpt):
        self.eqopt1 = eqopt1
        self.eqopt2 = eqopt2

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, TestEQOptLEQ):
            return self.eqopt1 == __value.eqopt1 and self.eqopt2 == __value.eqopt2
        return False

class TestEIQOptEQ(RemAst):
    def __init__(self, eiqopt1: EIQOpt, eiqopt2: EIQOpt):
        self.eiqopt1 = eiqopt1
        self.eiqopt2 = eiqopt2

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, TestEIQOptEQ):
            return self.eiqopt1 == __value.eiqopt1 and self.eiqopt2 == __value.eiqopt2
        return False

class TestEIQOptLEQ(RemAst):
    def __init__(self, eiqopt1: EIQOpt, eiqopt2: EIQOpt):
        self.eiqopt1 = eiqopt1
        self.eiqopt2 = eiqopt2

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, TestEIQOptLEQ):
            return self.eiqopt1 == __value.eiqopt1 and self.eiqopt2 == __value.eiqopt2
        return False





