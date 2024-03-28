
from ..language import lexer_def as AstLexer
from ..language.lexer_def import *

reserved = {
    'Def'       : 'DEF',
    'Refine'    : 'REFINE',
    'End'       : 'META_END',
    'Choose'    : 'CHOOSE',

    # for refinement control
    'Step'      : 'STEP',
    'Seq'       : 'REFINE_SEQ',
    'If'        : 'REFINE_IF',
    'While'     : 'REFINE_WHILE',
    'Inv'       : 'REFINE_INV',

    # pause the prover to see the state.
    'Pause'     : 'PAUSE',
    'WeakenPre' : 'REFINE_WEAKEN_PRE',
    'StrengthenPost' :  'REFINE_STRENGTHEN_POST',


    'Extract'   : 'EXTRACT',

    'Show'      : 'SHOW',
    'Draw'      : 'DRAW',
    'Test'      : 'TEST',

    'Eval'      : 'EVAL',
    'Prog'      : 'PROG',
}

tokens = ['ASSIGN'] + list(reserved.values()) + AstLexer.tokens
reserved.update(AstLexer.reserved)

literals = ['.'] + AstLexer.literals

t_ASSIGN = r":="

def t_ID(t):
    r'[a-zA-Z\'][a-zA-Z\'0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_error(t):
    raise LexingError(f"({t.lineno}, {find_column(t.lexer.lexdata, t)}) Illegal character '{t.value[0]}'.")