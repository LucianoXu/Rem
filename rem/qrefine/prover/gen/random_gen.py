# the module that randomly generate operators/programs

from ....qplcomp import Env, EIQOpt, EQVar, QVar, IQOptType, QOptType

import random

def random_qvar_gen(qvarls: QVar, qubit_num: int) -> EQVar:
    '''
    generate a random qvar of [qubit_num] qubits from qvarls
    '''
    return EQVar(QVar(random.sample(qvarls._qvls, qubit_num)))

def random_opt_gen(env: Env, qubit_num: int, depth: int|None = None) -> EIQOpt:
    pass

def opt_gen_def(env: Env, qubit_num: int, depth: int|None = None) -> EIQOpt|None:
    '''
    Terminal symbol for the random generation of operators.
    '''
    values = list(env.defs.values())
    for i in range(len(values)):
        item = random.choice(values)
        if item.type == QOptType():
            