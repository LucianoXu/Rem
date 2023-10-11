
import ply.lex as lex

from ..qplcomp import lexer as OPTlexer

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

reserved.update(OPTlexer.reserved)

tokens = ['ASSIGN0', 'FLOATNUM'] + list(reserved.values()) + OPTlexer.tokens

literals = ['(', ')', '_', '[', ']', ';', ',', ':', '=', '>', '{', '}'] + OPTlexer.literals

t_OTIMES = OPTlexer.t_OTIMES
t_DAGGER = OPTlexer.t_DAGGER
t_DISJUNCT = OPTlexer.t_DISJUNCT
t_CONJUNCT = OPTlexer.t_CONJUNCT
t_SASAKI_IMPLY = OPTlexer.t_SASAKI_IMPLY
t_SASAKI_CONJUNCT = OPTlexer.t_SASAKI_CONJUNCT
t_ASSIGN0 = r":=0"

# use // or /* */ to comment
def t_COMMENT(t):
    r'(/\*(.|\n)*?\*/)|(//.*)'
    for c in t.value:
        if c == '\n':
            t.lexer.lineno += 1


def t_ID(t):
    r'[a-zA-Z\'][a-zA-Z\'0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t

t_ignore = OPTlexer.t_ignore

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_FLOATNUM(t):
    r'[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?'
    return t

def t_error(t):
    raise ValueError("Syntax Error. Illegal character '" + t.value[0] + "'.")


# Build the lexer
import re
lexer = lex.lex(reflags = re.UNICODE)