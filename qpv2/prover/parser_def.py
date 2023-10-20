
from __future__ import annotations

from .prover import *

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
        | DEF ID ASSIGN PROG statement '.'
        | DEF ID ASSIGN EXTRACT ID '.'
        | REFINE ID ':' prescription '.'
        | STEP statement '.'
        | CHOOSE FLOATNUM '.'
        | META_END '.'

        | SHOW ID '.'
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

    elif type_match(p, ('DEF', 'ID', 'ASSIGN', 'PROG', 'statement', '.')):
        Prover().define(p[2], EAst(p[5]))

    elif type_match(p, ('DEF', 'ID', 'ASSIGN', 'EXTRACT', 'ID', '.')):
        Prover().define(p[2], EAst(Env()[p[5]].eval().extract))

    elif type_match(p, ("REFINE", "ID", ':', 'prescription', '.')):
        Prover().start_refinement(p[2], p[4])

    elif type_match(p, ("STEP", "statement", '.')):
        Prover().step_refine(p[2])

    elif type_match(p, ("CHOOSE", "FLOATNUM", '.')):
        Prover().refine_choose_goal(int(p[2]))

    elif type_match(p, ("META_END", ".")):
        Prover().end_refinement()

    elif type_match(p, ('SHOW', 'ID', '.')):
        Prover().show_id(p[2])
        
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

