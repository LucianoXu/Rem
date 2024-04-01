# the abstract syntax tree for Rem language

from __future__ import annotations

from ...qplcomp.qexpr.eqopt import EQOptAbstract

from ...mTLC import TypedTerm, Types
from ...qplcomp import *
from ..language import QProgAst, AstPres

from abc import ABC, abstractmethod

import numpy as np
        

#################################################
# Special Term for importing numpy array
#

class ImportQOpt(EQOptAbstract):
    def __init__(self, path: str):

        try:
            data = np.load(path)

        except FileNotFoundError:
            raise ValueError(f"File '{path}' not found.")
        
        self.loaded_term = EQOpt(QOpt(data))

        super().__init__(self.loaded_term.qopt.qnum)
        self.path = path

    def eval(self, env: Env) -> EQOptAbstract:
        return self.loaded_term
        

    def __str__(self) -> str:
        return f'Import "{self.path}"'
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, ImportQOpt):
            return self.path == other.path
        return False
    

class RemAst(ABC):
    
    @abstractmethod
    def __eq__(self, __value: object) -> bool:
        pass


class Declaration(RemAst):
    def __init__(self, id: str, type: Types):
        self.id = id
        self.type = type

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, Declaration):
            return self.id == __value.id and self.type == __value.type
        return False

class Definition(RemAst):
    def __init__(self, id: str, term: TypedTerm):
        self.id = id
        self.term = term

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, Definition):
            return self.id == __value.id and self.term == __value.term
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
    def __init__(self, statement: QProgAst):
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

class EvalTerm(RemAst):
    def __init__(self, term: TypedTerm):
        self.term = term

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, EvalTerm):
            return self.term == __value.term
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





