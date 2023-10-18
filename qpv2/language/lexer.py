
import ply.lex as lex

from qplcomp import lexer_def

from qplcomp.qexpr.lexer_def import *

reserved = {
    'abort'     : 'ABORT',
    'skip'      : 'SKIP',
    'assert'    : 'ASSERT',
    'if'        : 'IF',
    'then'      : 'THEN',
    'else'      : 'ELSE',
    'end'       : 'END',
    'while'     : 'WHILE',
    'do'        : 'DO',
    'pre'       : 'PRE',
    'post'      : 'POST',

# refinement rule names

    'RSKIP'     : 'RSKIP',
    'RIMPLY'    : 'RIMPLY',
    'RSEQ'      : 'RSEQ',
}

tokens = ['ASSIGN0'] + list(reserved.values()) + lexer_def.tokens
reserved.update(lexer_def.reserved)


literals = ['(', ')', '_', '[', ']', ';', ',', ':', '=', '>', '{', '}'] + lexer_def.literals

t_ASSIGN0 = r":=0"


# we have to redefine t_ID to update the reserved keywords. This is not elegant and we may need a framework for multi-layered parsing based on PLY.
def t_ID(t):
    r'[a-zA-Z\'][a-zA-Z\'0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t

# use // or /* */ to comment
def t_COMMENT(t):
    r'(/\*(.|\n)*?\*/)|(//.*)'
    for c in t.value:
        if c == '\n':
            t.lexer.lineno += 1

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    raise ValueError("Syntax Error. Illegal character '" + t.value[0] + "'.")


# Build the lexer
import re
lexer = lex.lex(reflags = re.UNICODE)