
from __future__ import annotations
import ply.yacc as yacc

from .lexer import tokens

from .ast import *

from ..qplcomp import parser_def

precedence = (
    ('left', '>'),
    ('right', ';'), # sequential composition is right-associated
) + parser_def.precedence


def p_prog(p):
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
                | refinement
    '''
    #parentheses
    if len(p) == 4 and p[1] == '{':
        p[0] = p[2]

    # abort
    elif p[1] == 'abort':
        p[0] = AstAbort()

    # skip
    elif p[1] == 'skip':
        p[0] = AstSkip()

    # initialization
    elif len(p) == 3 and p.slice[2].type == 'ASSIGN0':
        p[0] = AstInit(p[1])

    # unitary
    elif len(p) == 2 and p.slice[1].type == 'eiqopt':
        p[0] = AstUnitary(p[1])
    
    # assertion
    elif p.slice[1].type == 'ASSERT':
        p[0] = AstAssert(p[2])

    # prescription
    elif p.slice[1].type == 'prescription':
        p[0] = p[1]

    # sequential composition
    elif len(p) == 4 and p.slice[2].type == ';':
        p[0] = AstSeq(p[1], p[3])

    # probabilistic composition
    elif len(p) == 8 and p[3] == '_' and p.slice[4].type == 'FLOATNUM':
        p[0] = AstProb(p[2], p[6], float(p[4]))

    # if
    elif p.slice[1].type == 'IF':
        p[0] = AstIf(p[2], p[4], p[6])

    # while
    elif p.slice[1].type == 'WHILE':
        p[0] = AstWhile(p[2], p[4])

    # refinement
    elif p.slice[1].type == 'refinement':
        p[0] = p[1]

    else:
        raise Exception()
    
def p_prescription(p):
    '''
    prescription    : '[' PRE ':' eiqopt ',' POST ':' eiqopt ']'
    '''
    p[0] = AstPres(p[4], p[8])
    
from .refinement import *
def p_refinement(p):
    '''
    refinement  : statement '=' '=' '>' statement
                | statement '=' RSKIP '=' '>' statement
                | statement '=' RIMPLY '=' '>' statement
                | statement '=' RSEQ '=' '>' statement
    '''
    if len(p) == 6 and p[2] == '=' and p[3] == '=' and p[4] == '>':
        p[0] = RPres(p[1], p[5], [])
    elif p[3] == 'RSKIP':
        p[0] = RSKIP(p[1], p[6], [])
    elif p[3] == 'RIMPLY':
        p[0] = RIMPLY(p[1], p[6], [])
    elif p[3] == 'RSEQ':
        p[0] = RSEQ(p[1], p[6], [])
    else:
        raise Exception()
        
    
    
from ..qplcomp.qexpr.parser_def import p_eiqopt, p_eqopt, p_eqvar, p_num, p_qvar, p_qvar_pre, p_output, p_variable

def p_error(p):
    if p is None:
        raise RuntimeError("unexpected end of file")
    raise RuntimeError("Syntax error in input: '" + str(p.value) + "'.")



# Build the parser
parser = yacc.yacc()