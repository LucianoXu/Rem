

#############################################################
# the lexer

import ply.lex as lex

from .lexer_def import *

# Build the lexer
import re
lexer = lex.lex(reflags = re.UNICODE)



#############################################################
# the parser

import ply.yacc as yacc

from .parser_def import *
from .ast import QWhileAst

# Build the parser
parser = yacc.yacc()

def parser_reset():
    lexer.lineno = 1


def parse(code: str) -> QWhileAst:
    return parser.parse(code, lexer = lexer)