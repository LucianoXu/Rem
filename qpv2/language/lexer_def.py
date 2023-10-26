

from qplcomp import lexer_def as QPLCompLexer

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

    'proc'      : 'PROC',

# refinement rule names

}

tokens = ['ASSIGN0', 'OPLUS'] + list(reserved.values()) + QPLCompLexer.tokens
reserved.update(QPLCompLexer.reserved)


literals = ['(', ')', '_', '[', ']', ';', ',', ':', '=', '>', '{', '}'] + QPLCompLexer.literals

t_OPLUS = r"⊕|\\oplus"
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
    raise LexingError("Illegal character '" + t.value[0] + f"'. (line {t.lineno})")