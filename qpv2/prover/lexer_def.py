
from ..language import lexer_def as AstLexer
from ..language.lexer_def import *

reserved = {
    'Def'       : 'DEF',
    'Refine'    : 'REFINE',
    'End'       : 'META_END',
    'Choose'    : 'CHOOSE',
    'Step'      : 'STEP',

    # pause the prover to see the state.
    'Pause'     : 'PAUSE',

    'Show'      : 'SHOW',

    'Extract'   : 'EXTRACT',

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