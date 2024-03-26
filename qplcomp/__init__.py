'''
QPLComp
=====

This package aims at providing the necessary components for the implementation of numerical/symbolic calculation of quantum computing and quantum information. It contains:

- `QPLComp.qval`: the subpackage for quantum values `QVal` and indexed quantum values `IQVal`. Quantum values are those special vectors, operators and super operators used in quantum computing. `QVal` provides a abstract description and supports flexible representations. `IQVal` is quantum values indexed with quantum variables. Most operations involved in quantum computing can be conducted in a direct way.

- `QPLComp.qexpr`: the subpackage for expressions of quantum computing. We implemented a variable system to represent the values of quantum computing with expressions.
'''

from . import qval
from . import qexpr

from .error import QPLCompError

from .env import TypedTerm, Env, Var

from .qexpr import Parser
from .qexpr import prepare_env


from .qval import QVar
from .qval import QOpt, IQOpt
from .qval import QSOpt, IQSOpt
from .qval import predefined

# qexpr outputs the parsing details for downstream applications
# the lexer and parser is constructed by ply

from .qexpr.eqopt import EQOpt
from .qexpr.eiqopt import EIQOpt
from .qexpr.eqvar import EQVar
from .qexpr import lexer_def
from .qexpr import parser_def
from .qexpr import PLYError, LexingError, ParsingError