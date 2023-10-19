
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
        | REFINE ID ':' prescription '.'
        | STEP statement '.'
        | CHOOSE FLOATNUM '.'
        | META_END '.'
    '''
    if type_match(p, ()):
        pass
    elif type_match(p, ('PAUSE', '.')):
        Prover().paused = True

    elif type_match(p,('cmd', 'cmd')):
        pass

    elif type_match(p, ('DEF', 'ID', 'ASSIGN', 'eqopt', '.')):
        if not Prover().paused:
            Prover().define(p[2], p[4])

    elif type_match(p, ('DEF', 'ID', 'ASSIGN', 'eiqopt', '.')):
        if not Prover().paused:
            Prover().define(p[2], p[4])

    elif type_match(p, ("REFINE", "ID", ':', 'prescription', '.')):
        if not Prover().paused:
            Prover().start_refinement(p[2], p[4])

    elif type_match(p, ("STEP", "statement", '.')):
        if not Prover().paused:
            Prover().step_refine(p[2])

    elif type_match(p, ("CHOOSE", "FLOATNUM", '.')):
        if not Prover().paused:
            Prover().refine_choose_goal(int(p[2]))

    elif type_match(p, ("META_END", ".")):
        if not Prover().paused:
            Prover().end_refinement()
