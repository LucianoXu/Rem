
from .prover import Prover
#############################################################
# the lexer

import ply.lex as lex

from .lexer_def import *

# Build the lexer
import re
Prover.lexer = lex.lex(reflags = re.UNICODE)



#############################################################
# the parser

import ply.yacc as yacc

from .parser_def import *

start = "cmd"

# Build the parser
Prover.parser = yacc.yacc()
