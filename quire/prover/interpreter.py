
from __future__ import annotations
from typing import Any

from qplcomp import Env, prepare_env, EQOpt, QOpt, PLYError, QPLCompError
from ..language import AstPres, TypedTerm, ValueError, EIQOptPair

from .ast import *
from ..language.semantics.forward import calc

from copy import deepcopy

import numpy as np


class Frame:
    '''
    An exclusive proof frame of the prover.
    '''
    def __init__(self, env: Env, 
                 refine_proof_name: str,
                 refine_proof: AstPres|None,
                 info: str | Exception = ""):
        self.env : Env = env.copy()
        self.refine_proof_name = refine_proof_name
        self.refine_proof = deepcopy(refine_proof)
        self.info : str | Exception = info

        if self.refine_proof is None:
            self.current_goals = []
        if self.refine_proof:
            self.current_goals = self.refine_proof.get_prescription()

    @property
    def goals_str(self) -> str:
        if self.refine_proof is None:
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

    def copy(self) -> Frame:
        return Frame(
            self.env, 
            self.refine_proof_name,
            self.refine_proof,
            self.info)
    
    def __str__(self) -> str:
        res = self.goals_str
        res += "\n" + "-"*40 + "\n"
        res += f"= Info =\n\n" + str(self.info)
        return res


class Interpreter:
    '''
    It only work as the interpreter and does not preserve the frames.
    '''

    @staticmethod
    def exe(cmd: RemAst, frame: Frame) -> Frame:
        '''
        Execute a command in the frame.
        Return the result frame.
        '''
        new_frame = frame.copy()

        # DEF ID ASSIGN eqopt '.'
        if isinstance(cmd, DefEQOpt):
            new_frame.env[cmd.id] = cmd.eqopt
            new_frame.info = f"Defined EQOpt {cmd.id}."
            
        # DEF ID ASSIGN eiqopt '.'
        elif isinstance(cmd, DefEIQOpt):
            new_frame.env[cmd.id] = cmd.eiqopt
            new_frame.info = f"Defined EIQOpt {cmd.id}."

        # DEF ID ASSIGN '[' '[' statement ']' ']' '(' eiqopt ')' '.'
        elif isinstance(cmd, DefCalc):
            rho0 = cmd.eiqopt.eval(frame.env).iqopt
            rho = calc(cmd.statement, rho0, frame.env)

            new_frame.env[cmd.id] = EIQOptPair(EQOpt(rho.qval), EQVar(rho.qvar))
            new_frame.info = f"Defined Calculation {cmd.id}."
        
        # DEF ID ASSIGN PROG statement '.'
        elif isinstance(cmd, DefProg):
            new_frame.env[cmd.id] = cmd.statement
            new_frame.info = f"Defined Program {cmd.id}."

        # DEF ID ASSIGN EXTRACT ID '.'
        elif isinstance(cmd, DefExtract):
            term = frame.env[cmd.id2].eval(frame.env)
            if not isinstance(term, QWhileAst):
                raise ValueError("The term is not a While Program.")
            
            new_frame.env[cmd.id] = term.extract
            new_frame.info = f"Defined Extract {cmd.id}."

        # REFINE ID ':' prescription '.'
        elif isinstance(cmd, StartRefine):
            if frame.refine_proof is not None:
                raise ValueError("The prover is currently inside a refinement.")
            

            if not isinstance(cmd.prescription, AstPres):
                raise ValueError("The program to be refined must be a prescription.")
            
            new_frame.refine_proof_name = cmd.id
            new_frame.refine_proof = cmd.prescription
            new_frame.current_goals = [cmd.prescription]

            new_frame.info = f"Refinement starts."

        # STEP statement '.'
        # note: this is the direct refinement in semantics
        elif isinstance(cmd, StepStatement):
            if len(frame.current_goals) == 0:
                raise ValueError("There is no prescriptions to refine.")
            
            new_frame.current_goals[0].refine_wlp(cmd.statement, frame.env)

            new_frame.current_goals = new_frame.current_goals[0].get_prescription() + new_frame.current_goals[1:]
            
            new_frame.info = f"Refinement step succeeded."

        # STEP REFINE_SEQ eiqopt '.'
        elif isinstance(cmd, StepRefineSeq):
            if len(frame.current_goals) == 0:
                raise ValueError("There is no prescriptions to refine.")
            
            new_frame.current_goals[0].refine_seq_break(cmd.mid_assertion)

            new_frame.current_goals = new_frame.current_goals[0].get_prescription() + new_frame.current_goals[1:]
            
            new_frame.info = f"Refinement step succeeded."

        # STEP REFINE_IF eiqopt '.'
        elif isinstance(cmd, StepRefineIf):
            if len(frame.current_goals) == 0:
                raise ValueError("There is no prescriptions to refine.")
            
            new_frame.current_goals[0].refine_if(cmd.P)

            new_frame.current_goals = new_frame.current_goals[0].get_prescription() + new_frame.current_goals[1:]
            
            new_frame.info = f"Refinement step succeeded."

        # STEP REFINE_WHILE eiqopt REFINE_INV eiqopt '.'
        elif isinstance(cmd, StepRefineWhile):
            if len(frame.current_goals) == 0:
                raise ValueError("There is no prescriptions to refine.")
            
            new_frame.current_goals[0].refine_while(cmd.P, cmd.inv, frame.env)

            new_frame.current_goals = new_frame.current_goals[0].get_prescription() + new_frame.current_goals[1:]
            
            new_frame.info = f"Refinement step succeeded."

        # STEP REFINE_WEAKEN_PRE eiqopt '.'
        elif isinstance(cmd, RefineWeakenPre):
            if len(frame.current_goals) == 0:
                raise ValueError("There is no prescriptions to refine.")
            
            new_frame.current_goals[0].refine_weaken_pre(cmd.pre, frame.env)

            new_frame.current_goals = new_frame.current_goals[0].get_prescription() + new_frame.current_goals[1:]
            
            new_frame.info = f"Refinement step succeeded."

        # STEP REFINE_STRENGTHEN_POST eiqopt '.'
        elif isinstance(cmd, RefineStrengthenPost):
            if len(frame.current_goals) == 0:
                raise ValueError("There is no prescriptions to refine.")
            
            new_frame.current_goals[0].refine_strengthen_post(cmd.post, frame.env)

            new_frame.current_goals = new_frame.current_goals[0].get_prescription() + new_frame.current_goals[1:]
            
            new_frame.info = f"Refinement step succeeded."

        # CHOOSE FLOATNUM '.'
        elif isinstance(cmd, RefineChooseGoal):
            if not 1 <= cmd.n <= len(frame.current_goals):
                raise ValueError(f"Invalid goal number {cmd.n}. Choose a number from {1} to {len(frame.current_goals)}. ")
            
            # switch the goals
            new_frame.current_goals = [new_frame.current_goals[cmd.n-1]] + new_frame.current_goals[:cmd.n-1] + new_frame.current_goals[cmd.n:]

            new_frame.info = f"Goal switched."

        # META_END '.'
        elif isinstance(cmd, MetaEnd):
            if frame.refine_proof is None:
                raise ValueError("The prover is not in a refinement.")
            
            if len(frame.current_goals) != 0:
                raise ValueError("Goals not clear.")

            # register this refinement result
            new_frame.env[frame.refine_proof_name] = frame.refine_proof

            new_frame.refine_proof = None
            new_frame.current_goals = []

            new_frame.info = f"Refinement ends."

        # SHOW ID '.'
        elif isinstance(cmd, ShowId):
            new_frame.info = f"Show {cmd.id}:\n {frame.env[cmd.id]}"

        # SHOW DEF '.'
        elif isinstance(cmd, ShowDef):
            new_frame.info = f"Definitions: \n{frame.env.get_items()}"
        
        # EVAL ID '.'
        elif isinstance(cmd, EvalId):
            res = frame.env[cmd.id].eval(frame.env)
            new_frame.info = f"Evaluated {cmd.id} to:\n {res}"

        # TEST eqopt '=' eqopt '.'
        elif isinstance(cmd, TestEQOptEQ):
            res = cmd.eqopt1.eval(frame.env) == cmd.eqopt2.eval(frame.env)
            if res:
                new_frame.info = f"Test Result: {cmd.eqopt1} = {cmd.eqopt2}"
            else:
                new_frame.info = f"Test Result: {cmd.eqopt1} ≠ {cmd.eqopt2}"


        # TEST eiqopt '=' eiqopt '.'
        elif isinstance(cmd, TestEIQOptEQ):
            res = cmd.eiqopt1.eval(frame.env) == cmd.eiqopt2.eval(frame.env)
            if res:
                new_frame.info = f"Test Result: {cmd.eiqopt1} = {cmd.eiqopt2}"
            else:
                new_frame.info = f"Test Result: {cmd.eiqopt1} ≠ {cmd.eiqopt2}"

        # TEST eqopt LEQ eqopt '.'
        elif isinstance(cmd, TestEQOptLEQ):
            res = cmd.eqopt1.eval(frame.env).qopt <= cmd.eqopt2.eval(frame.env).qopt
            if res:
                new_frame.info = f"Test Result: {cmd.eqopt1} <= {cmd.eqopt1}"
            else:
                new_frame.info = f"Test Result: {cmd.eqopt1} </= {cmd.eqopt1}"

        # TEST eiqopt LEQ eiqopt '.'
        elif isinstance(cmd, TestEIQOptLEQ):
            res = cmd.eiqopt1.eval(frame.env).iqopt <= cmd.eiqopt2.eval(frame.env).iqopt
            if res:
                new_frame.info = f"Test Result: {cmd.eiqopt1} <= {cmd.eiqopt1}"
            else:
                new_frame.info = f"Test Result: {cmd.eiqopt1} </= {cmd.eiqopt1}"

        else:
            raise Exception("Not Implemented Command.")

        return new_frame