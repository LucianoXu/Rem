
from __future__ import annotations

from .prover import *

from ..language import parser_def as AstParser
from ..language.parser_def import type_match

from .ast import *

precedence = (
    ('right', '.'),
) + AstParser.precedence

def p_cmd_stack(p):
    '''
    cmd-stack : 
              | cmd
              | cmd-stack cmd
    '''
    if type_match(p, ()):
        p[0] = CMDStack(())
    elif type_match(p, ('cmd',)):
        p[0] = CMDStack((p[1],))
    elif type_match(p, ('cmd-stack', 'cmd')):
        p[0] = p[1] + p[2]
    else:
        raise Exception()


def p_cmd(p):
    '''
    cmd : PAUSE '.'
        | DEF ID ASSIGN eqopt '.'
        | DEF ID ASSIGN eiqopt '.'
        | DEF ID ASSIGN '[' '[' statement ']' ']' '(' eiqopt ')' '.'
        | DEF ID ASSIGN PROG statement '.'
        | DEF ID ASSIGN EXTRACT ID '.'
        | REFINE ID ':' prescription '.'

        | STEP statement '.'
        | STEP REFINE_SEQ eiqopt '.'
        | STEP REFINE_IF eiqopt '.'
        | STEP REFINE_WHILE eiqopt REFINE_INV eiqopt '.'
        | REFINE_WEAKEN_PRE eiqopt '.'
        | REFINE_STRENGTHEN_POST eiqopt '.'

        | CHOOSE FLOATNUM '.'
        | META_END '.'

        | SHOW ID '.'
        | SHOW DEF '.'
        | EVAL ID '.'
        | TEST eqopt '=' eqopt '.'
        | TEST eqopt LEQ eqopt '.'
        | TEST eiqopt '=' eiqopt '.'
        | TEST eiqopt LEQ eiqopt '.'

    '''
    if type_match(p, ('PAUSE', '.')):
        p[0] = Pause()

    elif type_match(p, ('DEF', 'ID', 'ASSIGN', 'eqopt', '.')):
        p[0] = DefEQOpt(p[2], p[4])

    elif type_match(p, ('DEF', 'ID', 'ASSIGN', 'eiqopt', '.')):
        p[0] = DefEIQOpt(p[2], p[4])

    elif type_match(p, ('DEF', 'ID', 'ASSIGN', '[', '[', 'statement', ']', ']', '(', 'eiqopt', ')', '.')):
        p[0] = DefCalc(p[2], p[6], p[10])
        # rho0 = p[10].eval()
        # rho = calc(p[6], rho0)
        # Prover().define(p[2], EIQOpt(EQOpt(rho.qval), EQVar(rho.qvar)))

    elif type_match(p, ('DEF', 'ID', 'ASSIGN', 'PROG', 'statement', '.')):
        p[0] = DefProg(p[2], p[5])

    elif type_match(p, ('DEF', 'ID', 'ASSIGN', 'EXTRACT', 'ID', '.')):
        p[0] = DefExtract(p[2], p[5])
        # Prover().define(p[2], EAst(Env()[p[5]].eval().extract)) # type: ignore

    elif type_match(p, ("REFINE", "ID", ':', 'prescription', '.')):
        p[0] = StartRefine(p[2], p[4])

    elif type_match(p, ("STEP", "statement", '.')):
        p[0] = StepStatement(p[2])

    elif type_match(p, ("STEP", 'REFINE_SEQ', 'eiqopt', '.')):
        p[0] = StepRefineSeq(p[3])

    elif type_match(p, ("STEP", 'REFINE_IF', 'eiqopt', '.')):
        p[0] = StepRefineIf(p[3])

    elif type_match(p, ("STEP", 'REFINE_WHILE', 'eiqopt', 'REFINE_INV', 'eiqopt', '.')):
        p[0] = StepRefineWhile(p[3], p[5])

    elif type_match(p, ("REFINE_WEAKEN_PRE", 'eiqopt', '.')):
        p[0] = RefineWeakenPre(p[2])

    elif type_match(p, ("REFINE_STRENGTHEN_POST", 'eiqopt', '.')):
        p[0] = RefineStrengthenPost(p[2])

    elif type_match(p, ("CHOOSE", "FLOATNUM", '.')):
        p[0] = RefineChooseGoal(int(p[2]))

    elif type_match(p, ("META_END", ".")):
        p[0] = MetaEnd()

    elif type_match(p, ('SHOW', 'ID', '.')):
        p[0] = ShowId(p[2])

    elif type_match(p, ('SHOW', 'DEF', '.')):
        p[0] = ShowDef()
        
    elif type_match(p, ("EVAL", "ID", ".")):
        p[0] = EvalId(p[2])

    elif type_match(p, ('TEST', 'eqopt', '=', 'eqopt', '.')):
        p[0] = TestEQOptEQ(p[2], p[4])
    
    elif type_match(p, ('TEST', 'eiqopt', '=', 'eiqopt', '.')):
        p[0] = TestEIQOptEQ(p[2], p[4])

    elif type_match(p, ('TEST', 'eqopt', 'LEQ', 'eqopt', '.')):
        p[0] = TestEQOptLEQ(p[2], p[4])

    elif type_match(p, ('TEST', 'eiqopt', 'LEQ', 'eiqopt', '.')):
        p[0] = TestEIQOptLEQ(p[2], p[4])

    else:
        raise Exception()

