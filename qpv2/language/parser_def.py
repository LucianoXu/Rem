
from __future__ import annotations
from typing import Tuple

from .ast import *

from qplcomp import parser_def as QPLCompParser

precedence = (
    ('left', '>'),
    ('right', ';'), # sequential composition is right-associated
) + QPLCompParser.precedence


def type_match(p, types: Tuple[str, ...]) -> bool:
    '''
    The method to check whether the sentence match the corresponding types.
    '''
    if len(p) != len(types) + 1:
        return False
    
    for i in range(len(types)):
        if p.slice[i + 1].type != types[i]:
            return False
    return True

def p_statement(p):
    '''
    statement   : '{' statement '}'
                | ABORT
                | SKIP
                | eqvar ASSIGN0
                | eiqopt
                | ASSERT eiqopt
                | prescription
                | statement ';' statement
                | '(' statement '_' FLOATNUM OTIMES statement ')'
                | IF eiqopt THEN statement ELSE statement END
                | WHILE eiqopt DO statement END
                | ID
                | prescription '=' '=' '>' statement
    '''
    #parentheses
    if type_match(p, ('{', 'statement', '}')):
        p[0] = p[2]

    # abort
    elif type_match(p, ("ABORT",)):
        p[0] = AstAbort()

    # skip
    elif type_match(p, ("SKIP",)):
        p[0] = AstSkip()

    # initialization
    elif type_match(p, ("eqvar", "ASSIGN0")):
        p[0] = AstInit(p[1])

    # unitary
    elif type_match(p, ("eiqopt",)):
        p[0] = AstUnitary(p[1])
    
    # assertion
    elif type_match(p, ("ASSERT", "eiqopt")):
        p[0] = AstAssert(p[2])

    # prescription
    elif type_match(p, ("prescription",)):
        p[0] = p[1]

    # sequential composition
    elif type_match(p, ("statement", ';', "statement")):
        p[0] = AstSeq(p[1], p[3])

    # probabilistic composition
    elif type_match(p, ('(', 'statement', '_', 'FLOATNUM', 'OTIMES', 'statement', ')')):
        p[0] = AstProb(p[2], p[6], float(p[4]))

    # if
    elif type_match(p, ("IF", "eiqopt", "THEN", "statement", "ELSE", "statement", "END")):
        p[0] = AstIf(p[2], p[4], p[6])

    # while
    elif type_match(p, ("WHILE", "eiqopt", "DO", "statement", "END")):
        p[0] = AstWhile(p[2], p[4])

    # subprog
    elif type_match(p, ("ID",)):
        p[0] = AstSubprog(Variable(p[1]))

    # refinement
    elif type_match(p, ("prescription", '=', '=', '>', "statement")):
        p[1].refine(p[5])
        p[0] = p[1]
    else:
        raise Exception()
    
def p_prescription(p):
    '''
    prescription    : '[' PRE ':' eiqopt ',' POST ':' eiqopt ']'
    '''
    p[0] = AstPres(p[4], p[8])
    
    
from qplcomp.qexpr.parser_def import p_eiqopt, p_eqopt, p_eqvar, p_num, p_qvar, p_qvar_pre, p_variable

def p_error(p):
    if p is None:
        raise RuntimeError("unexpected end of file")
    raise RuntimeError("Syntax error in input: '" + str(p.value) + "'.")