
from __future__ import annotations

from ...mTLC.env import Env
from .lexer_def import PLYError

class ParsingError(PLYError):
    pass

def type_match(p, types: tuple[str, ...]) -> bool:
    '''
    The method to check whether the sentence match the corresponding types.
    '''
    if len(p) != len(types) + 1:
        return False
    
    for i in range(len(types)):
        if p.slice[i + 1].type != types[i]:
            return False
    return True


# global variables to store the parsed information
class ParserState:
    input_code = ""
    env: Env

    @staticmethod
    def reset(env: Env):
        ParserState.input_code = ""
        ParserState.env = env


def find_column(token):
    '''
    Compute column.
    token is a token instance
    '''
    line_start = ParserState.input_code.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1


############################################################
# parsing rules
############################################################

precedence = (
    ('right', '.'),
    ('left', '>'),
    ('right', ';'),
    ('left', '+', '-'),
    ('right', 'SASAKI_IMPLY'),
    ('left', 'SASAKI_CONJUNCT'),
    ('left', 'DISJUNCT'),
    ('left', 'CONJUNCT'),
    ('left', '*', 'OTIMES'),
    ('left', 'DAGGER'),
)

def p_term(p):
    '''
    term    : var
            | '(' term ')'
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[2]

from ...mTLC.env import Var
def p_variable(p):
    '''
    var     : ID
    '''
    p[0] = Var(p[1], ParserState.env)


from ...qplcomp.qexpr.eiqopt import *
def p_1(p):
    '''
    term    : term eqvar
    '''
    p[0] = EIQOptPair(p[1], p[2])

def p_2(p):
    '''
    term    : '-' term
    '''
    if isinstance(p[2].type, IQOptType):
        p[0] = EIQOptNeg(p[2])
    elif isinstance(p[2].type, QOptType):
        p[0] = EQOptNeg(p[2])
    else:
        raise ValueError("Invalid term for expression '- term'.")

def p_3(p):
    '''
    term    : term '+' term
    '''
    if isinstance(p[1].type, IQOptType):
        p[0] = EIQOptAdd(p[1], p[3])
    elif isinstance(p[1].type, QOptType):
        p[0] = EQOptAdd(p[1], p[3])
    else:
        raise ValueError("Invalid term for expression 'term + term'.")
    

def p_4(p):
    '''
    term    : term '-' term
    '''
    if isinstance(p[1].type, IQOptType):
        p[0] = EIQOptSub(p[1], p[3])
    elif isinstance(p[1].type, QOptType):
        p[0] = EQOptSub(p[1], p[3])
    else:
        raise ValueError("Invalid term for expression 'term - term'.")
    
def p_5(p):
    '''
    term    : num '*' term
    '''
    if isinstance(p[3].type, IQOptType):
        p[0] = EIQOptScale(p[1], p[3])
    elif isinstance(p[3].type, QOptType):
        p[0] = EQOptScale(p[1], p[3])
    else:
        raise ValueError("Invalid term for expression 'num * term'.")
    
def p_5SIMP(p):
    '''
    term    : num term
    '''
    if isinstance(p[2].type, IQOptType):
        p[0] = EIQOptScale(p[1], p[2])
    elif isinstance(p[2].type, QOptType):
        p[0] = EQOptScale(p[1], p[2])
    else:
        raise ValueError("Invalid term for expression 'num term'.")
    

def p_6(p):
    '''
    term    : term '*' term
    '''
    if isinstance(p[1].type, IQOptType):
        p[0] = EIQOptMul(p[1], p[3])
    elif isinstance(p[1].type, QOptType):
        p[0] = EQOptMul(p[1], p[3])
    else:
        raise ValueError("Invalid term for expression 'term * term'.")

def p_7(p):
    '''
    term    : term DAGGER
    '''
    if isinstance(p[1].type, IQOptType):
        p[0] = EIQOptDagger(p[1])
    elif isinstance(p[1].type, QOptType):
        p[0] = EQOptDagger(p[1])
    else:
        raise ValueError("Invalid term for expression 'term DAGGER'.")

def p_8(p):
    '''
    term    : term OTIMES term
    '''
    if isinstance(p[1].type, IQOptType):
        p[0] = EIQOptTensor(p[1], p[3])
    elif isinstance(p[1].type, QOptType):
        p[0] = EQOptTensor(p[1], p[3])
    else:
        raise ValueError("Invalid term for expression 'term OTIMES term'.")
    
def p_9(p):
    '''
    term    : term DISJUNCT term
    '''
    if isinstance(p[1].type, IQOptType):
        p[0] = EIQOptDisjunct(p[1], p[3])
    elif isinstance(p[1].type, QOptType):
        p[0] = EQOptDisjunct(p[1], p[3])
    else:
        raise ValueError("Invalid term for expression 'term DISJUNCT term'.")
    
def p_10(p):
    '''
    term    : term CONJUNCT term
    '''
    if isinstance(p[1].type, IQOptType):
        p[0] = EIQOptConjunct(p[1], p[3])
    elif isinstance(p[1].type, QOptType):
        p[0] = EQOptConjunct(p[1], p[3])
    else:
        raise ValueError("Invalid term for expression 'term CONJUNCT term'.")
    
def p_11(p):
    '''
    term    : term COMPLEMENT
    '''
    if isinstance(p[1].type, IQOptType):
        p[0] = EIQOptComplement(p[1])
    elif isinstance(p[1].type, QOptType):
        p[0] = EQOptComplement(p[1])
    else:
        raise ValueError("Invalid term for expression 'term COMPLEMENT'.")

def p_12(p):
    '''
    term    : term SASAKI_IMPLY term
    '''
    if isinstance(p[1].type, IQOptType):
        p[0] = EIQOptSasakiImply(p[1], p[3])
    elif isinstance(p[1].type, QOptType):
        p[0] = EQOptSasakiImply(p[1], p[3])
    else:
        raise ValueError("Invalid term for expression 'term SASAKI_IMPLY term'.")
    
def p_13(p):
    '''
    term    : term SASAKI_CONJUNCT term
    '''
    if isinstance(p[1].type, IQOptType):
        p[0] = EIQOptSasakiConjunct(p[1], p[3])
    elif isinstance(p[1].type, QOptType):
        p[0] = EQOptSasakiConjunct(p[1], p[3])
    else:
        raise ValueError("Invalid term for expression 'term SASAKI_CONJUNCT term'.")


from ...qplcomp.qexpr.eqopt import *
def p_14(p):
    '''
    term    : '[' eqvec ']'
    '''
    p[0] = EQOptKetProj(p[2])


from ...qplcomp.qexpr.eqvar import EQVar
def p_eqvar(p):
    '''
    eqvar   : qvar
    '''
    p[0] = EQVar(p[1])

from ...qplcomp.qval import QVar
def p_qvar(p):
    '''
    qvar : qvar_pre ']'
    '''
    p[0] = QVar(p[1])


def p_qvar_pre(p):
    '''
    qvar_pre : '['
                | qvar_pre ID
    '''
    if p[1] == '[':
        p[0] = []
    else:
        p[0] = p[1] + [p[2]]

from ...qplcomp.qexpr.eqvec import *
def p_eqvec(p):
    '''
    eqvec   : KET_BITSTR
            | eqvec '+' eqvec
            | num eqvec %prec '*'
            | num '*' eqvec
    '''
    if type_match(p, ('KET_BITSTR',)):
        p[0] = EQVecBitString(p[1])
    elif type_match(p, ('eqvec', '+', 'eqvec')):
        p[0] = EQVecAdd(p[1], p[3])
    elif type_match(p, ('num', 'eqvec')):
        p[0] = EQVecScale(p[1], p[2])
    elif type_match(p, ('num', '*', 'eqvec')):
        p[0] = EQVecScale(p[1], p[3])
    else:
        raise Exception()
        

def p_num(p):
    '''
    num : FLOATNUM
        | COMPLEXNUM
    '''
    if p.slice[1].type == 'FLOATNUM':
        p[0] = float(p[1])
    elif p.slice[1].type == 'COMPLEXNUM':
        p[0] = complex(p[1])
    else:
        raise Exception()



from ..language.ast import *

def p_stt_0(p):
    '''
    term    : statement
    '''
    p[0] = p[1]

def p_stt_var(p):
    '''
    statement   : var
    '''
    p[0] = p[1]

def p_stt_1(p):
    '''
    statement   : ABORT
    '''
    p[0] = AstAbort()

def p_stt_2(p):
    '''
    statement    : SKIP
    '''
    p[0] = AstSkip()

def p_stt_3(p):
    '''
    statement    : eqvar ASSIGN0
    '''
    p[0] = AstInit(p[1])

def p_stt_4(p):
    '''
    statement    : term ';'
    '''
    p[0] = AstUnitary(p[1])

def p_stt_5(p):
    '''
    statement    : ASSERT term
    '''
    p[0] = AstAssert(p[2])

def p_pres(p):
    '''
    statement    : '<' term ',' term '>'
    '''
    p[0] = AstPres(p[2], p[4])

def p_stt_6(p):
    '''
    statement    : statement statement
    '''
    p[0] = AstSeq(p[1], p[2])

def p_stt_7(p):
    '''
    statement    : '{' statement '[' OPLUS FLOATNUM ']' statement '}'
    '''
    p[0] = AstProb(p[2], p[7], float(p[5]))

def p_stt_8(p):
    '''
    statement    : IF term THEN statement ELSE statement END
    '''
    p[0] = AstIf(p[2], p[4], p[6])

def p_stt_9(p):
    '''
    statement    : WHILE term DO statement END
    '''
    p[0] = AstWhile(p[2], p[4])

def p_stt_10(p):
    '''
    statement    : statement LEQ statement
    '''
    # particularly, the first term should be a prescription
    if not isinstance(p[1], AstPres):
        raise ValueError("The first term should be a prescription.")
    p[1].refine_wlp(p[3])
    p[0] = p[1]


from ..language.semantics.state import EIQOptCalc
def p_calc_iqopt(p):
    '''
    term    : '[' '[' statement ']' ']' '(' term ')'
    '''
    p[0] = EIQOptCalc(p[3], p[7])

from ..language.semantics.extract import QProgExtract
def p_extract_prog(p):
    '''
    term    : EXTRACT statement
    '''
    p[0] = QProgExtract(p[2])

from ..prover.ast import *

########################################################
# commands                                             #
########################################################

def p_cmd_0(p):
    '''
    cmd : VAR ID ':' QOPT '[' FLOATNUM ']' '.'
        | VAR ID ':' IQOPT '.'
        | VAR ID ':' QPROG '.'
    '''
    if p[4] == 'QOpt':
        p[0] = Declaration(p[2], QOptType(int(p[6])))
    elif p[4] == 'IQOpt':
        p[0] = Declaration(p[2], IQOptType())
    elif p[4] == 'QProg':
        p[0] = Declaration(p[2], QProgType())
    else:
        raise ValueError("Invalid declaration.")

def p_cmd_1(p):
    '''
    cmd : DEF ID ASSIGN term '.'
    '''
    p[0] = Definition(p[2], p[4])

def p_cmd_2(p):
    '''
    cmd : REFINE ID ':' term '.'
    '''
    # particularly, the term should be a prescription
    if not isinstance(p[4], AstPres):
        raise ValueError("The term should be a prescription.")
    
    p[0] = StartRefine(p[2], p[4])

def p_cmd_3(p):
    '''
    cmd : STEP term '.'
    '''
    p[0] = StepStatement(p[2])

def p_cmd_4(p):
    '''
    cmd : STEP REFINE_SEQ term '.'
    '''
    p[0] = StepRefineSeq(p[3])

def p_cmd_5(p):
    '''
    cmd : STEP REFINE_IF term '.'
    '''
    p[0] = StepRefineIf(p[3])

def p_cmd_6(p):
    '''
    cmd : STEP REFINE_WHILE term REFINE_INV term '.'
    '''
    p[0] = StepRefineWhile(p[3], p[5])

def p_cmd_7(p):
    '''
    cmd : REFINE_WEAKEN_PRE term '.'
    '''
    p[0] = RefineWeakenPre(p[2])

def p_cmd_8(p):
    '''
    cmd : REFINE_STRENGTHEN_POST term '.'
    '''
    p[0] = RefineStrengthenPost(p[2])

def p_cmd_9(p):
    '''
    cmd : CHOOSE FLOATNUM '.'
    '''
    p[0] = RefineChooseGoal(int(p[2]))

def p_cmd_10(p):
    '''
    cmd : META_END '.'
    '''
    p[0] = MetaEnd()

def p_cmd_11(p):
    '''
    cmd : SHOW ID '.'
    '''
    p[0] = ShowId(p[2])

def p_cmd_12(p):
    '''
    cmd : SHOW DEF '.'
    '''
    p[0] = ShowDef()

def p_cmd_13(p):
    '''
    cmd : EVAL term '.'
    '''
    p[0] = EvalTerm(p[2])

def p_cmd_14(p):
    '''
    cmd : TEST term '=' term '.'
    '''
    if isinstance(p[2].type, IQOptType):
        p[0] = TestEIQOptEQ(p[2], p[4])

    elif isinstance(p[2].type, QOptType):
        p[0] = TestEQOptEQ(p[2], p[4])

    else:
        raise ValueError("Invalid test command.")
    
def p_cmd_15(p):
    '''
    cmd : TEST term LEQ term '.'
    '''
    if isinstance(p[2].type, IQOptType):
        p[0] = TestEIQOptLEQ(p[2], p[4])

    elif isinstance(p[2].type, QOptType):
        p[0] = TestEQOptLEQ(p[2], p[4])

    else:
        raise ValueError("Invalid test command.")


def p_error(p):
    if p is None:
        raise ParsingError("EOF encountered. (end of input).")
    raise ParsingError(f"({p.lineno}, {find_column(p)}) Syntax error in input: '{p.value}'.")