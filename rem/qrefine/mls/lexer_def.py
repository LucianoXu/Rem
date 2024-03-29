
class PLYError(Exception):
    pass

class LexingError(PLYError):
    pass



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

    'proc'      : 'PROC',


    # for refinement control
    'Refine'    : 'REFINE',
    'End'       : 'META_END',
    'Choose'    : 'CHOOSE',

    'Step'      : 'STEP',
    'Seq'       : 'REFINE_SEQ',
    'If'        : 'REFINE_IF',
    'While'     : 'REFINE_WHILE',
    'Inv'       : 'REFINE_INV',

    'WeakenPre' : 'REFINE_WEAKEN_PRE',
    'StrengthenPost' :  'REFINE_STRENGTHEN_POST',

    'Extract'   : 'EXTRACT',

    # for the meta-language and types
    'Var'       : 'VAR',
    'Def'       : 'DEF',

    'Show'      : 'SHOW',
    'Draw'      : 'DRAW',
    'Test'      : 'TEST',

    'Eval'      : 'EVAL',
    'Prog'      : 'PROG',

    # types
    'IQOpt'     : 'IQOPT',
    'QOpt'      : 'QOPT',
    'QProg'     : 'QPROG',
}

tokens = [
    'ID',
    'ASSIGN',

    'OTIMES',
    'DAGGER',
    'DISJUNCT',
    'CONJUNCT',
    'COMPLEMENT',
    'SASAKI_IMPLY',
    'SASAKI_CONJUNCT',

    'ASSIGN0', 
    'OPLUS', 
    'LEQ',
    'FLOATNUM',
    'COMPLEXNUM',
    'KET_BITSTR',
    ] + list(reserved.values())

literals = ['.', '(', ')', '+', '-', '*', '_', '[', ']', ';', ',', ':', '=', '>', '{', '}', '<', '|', '>']

t_ASSIGN = r":="

t_OTIMES = r"⊗|\\otimes"
t_DAGGER = r"†|\^\\dagger"
t_DISJUNCT = r"∨|\\vee"
t_CONJUNCT = r"∧|\\wedge"
t_COMPLEMENT = r"\^⊥|\^\\bot"
t_SASAKI_IMPLY = r"⇝|\\SasakiImply"
t_SASAKI_CONJUNCT = r"⋒|\\SasakiConjunct"

t_OPLUS = r"⊕|\\oplus"
t_ASSIGN0 = r":=0"
t_LEQ = r"<="


def t_ID(t):
    r'[a-zA-Z\'][a-zA-Z\'0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t

# note this token will not include real numbers
def t_COMPLEXNUM(t):
    r'(\(([-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?)([-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?)?j\))|(([-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?)?j)'
    return t

def t_FLOATNUM(t):
    r'[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?'
    return t

def t_KET_BITSTR(t):
    r'\|[01]+>'
    t.value = t.value[1:-1]
    return t


# A string containing ignored characters (spaces and tabs)
t_ignore = ' \t'


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
    raise LexingError(f"({t.lineno}, {find_column(t.lexer.lexdata, t)}) Illegal character '{t.value[0]}'.")


def find_column(input, token):
    '''
    Compute column.
    input is the input text string
    token is a token instance
    '''
    line_start = input.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1

