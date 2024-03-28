
from .prover import Prover
#############################################################
# the lexer

import ply.lex as lex

from .lexer_def import *

# Build the lexer
import re
lexer = lex.lex(reflags = re.UNICODE)

def first_sentence(code: str) -> tuple[str|None, str]:
    '''
    Returns the first sentence of the code (ending with '.') and the remaining part.
    '''
    lexer.lineno = 1
    lexer.input(code)

    for token in lexer:
        if token.type == '.':
            return code[:token.lexpos+1], code[token.lexpos+1:]
        
    return None, code

#############################################################
# the parser

import ply.yacc as yacc



from .parser_def import *

start = "cmd"

# Build the parser
parser = yacc.yacc()

def parse_sentence(code: str) -> tuple[tuple[RemAst, str]|Exception, str]:
    '''
    parse one sentence of the code, return the result and the remaining part.
    '''

    sentence, remained_part = first_sentence(code)

    if sentence is None:
        return LexingError("unexpected EOF encountered."), code

    # reset lexer
    lexer.lineno = 1
    ParserState.reset()
    ParserState.input_code = sentence

    try:
        res = parser.parse(sentence, lexer = lexer)
    except (LexingError, ParsingError) as e:
        return e, code
    
    return (res, sentence), remained_part
