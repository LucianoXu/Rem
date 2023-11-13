
from __future__ import annotations

from .prover import *

from qplcomp import EQVar
from ..calc import calc
from ..language import parser_def as AstParser
from ..language.parser_def import *

precedence = (
    ('right', '.'),
) + AstParser.precedence

def p_cmd(p):
    '''
    cmd : cmd cmd
        | PAUSE '.'
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
        | DRAW ID '.'
        | SHOW DEF '.'
        | EVAL ID '.'
        | TEST eqopt '=' eqopt '.'
        | TEST eqopt LEQ eqopt '.'
        | TEST eiqopt '=' eiqopt '.'
        | TEST eiqopt LEQ eiqopt '.'

    '''
    if type_match(p, ()):
        pass
    elif type_match(p, ('PAUSE', '.')):
        raise PauseError()

    elif type_match(p,('cmd', 'cmd')):
        pass

    elif type_match(p, ('DEF', 'ID', 'ASSIGN', 'eqopt', '.')):
        Prover().define(p[2], p[4])

    elif type_match(p, ('DEF', 'ID', 'ASSIGN', 'eiqopt', '.')):
        Prover().define(p[2], p[4])

    elif type_match(p, ('DEF', 'ID', 'ASSIGN', '[', '[', 'statement', ']', ']', '(', 'eiqopt', ')', '.')):
        rho0 = p[10].eval()
        rho = calc(p[6], rho0)
        Prover().define(p[2], EIQOpt(EQOpt(rho.qval), EQVar(rho.qvar)))

    elif type_match(p, ('DEF', 'ID', 'ASSIGN', 'PROG', 'statement', '.')):
        Prover().define(p[2], EAst(p[5]))

    elif type_match(p, ('DEF', 'ID', 'ASSIGN', 'EXTRACT', 'ID', '.')):
        Prover().define(p[2], EAst(Env()[p[5]].eval().extract)) # type: ignore

    elif type_match(p, ("REFINE", "ID", ':', 'prescription', '.')):
        Prover().start_refinement(p[2], p[4])

    elif type_match(p, ("STEP", "statement", '.')):
        Prover().step_refine_wlp(p[2])

    elif type_match(p, ("STEP", 'REFINE_SEQ', 'eiqopt', '.')):
        Prover().step_refine_seq(p[3])

    elif type_match(p, ("STEP", 'REFINE_IF', 'eiqopt', '.')):
        Prover().step_refine_if(p[3])

    elif type_match(p, ("STEP", 'REFINE_WHILE', 'eiqopt', 'REFINE_INV', 'eiqopt', '.')):
        Prover().step_refine_while(p[3], p[5])

    elif type_match(p, ("REFINE_WEAKEN_PRE", 'eiqopt', '.')):
        Prover().step_refine_weaken_pre(p[2])

    elif type_match(p, ("REFINE_STRENGTHEN_POST", 'eiqopt', '.')):
        Prover().step_refine_strengthen_post(p[2])

    elif type_match(p, ("CHOOSE", "FLOATNUM", '.')):
        Prover().refine_choose_goal(int(p[2]))

    elif type_match(p, ("META_END", ".")):
        Prover().end_refinement()

    elif type_match(p, ('SHOW', 'ID', '.')):
        Prover().show_id(p[2])

    elif type_match(p, ('DRAW', 'ID', '.')):
        Prover().draw_id(p[2])

    elif type_match(p, ('SHOW', 'DEF', '.')):
        Prover().show_def()
        
    elif type_match(p, ("EVAL", "ID", ".")):
        Prover().eval_id(p[2])

    elif type_match(p, ('TEST', 'eqopt', '=', 'eqopt', '.')):
        Prover().test_eq(p[2], p[4])
    
    elif type_match(p, ('TEST', 'eiqopt', '=', 'eiqopt', '.')):
        Prover().test_eq(p[2], p[4])

    elif type_match(p, ('TEST', 'eqopt', 'LEQ', 'eqopt', '.')):
        Prover().test_leq(p[2], p[4])

    elif type_match(p, ('TEST', 'eiqopt', 'LEQ', 'eiqopt', '.')):
        Prover().test_leq(p[2], p[4])

    else:
        raise Exception()

