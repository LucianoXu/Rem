# the module that randomly generate operators/programs

from __future__ import annotations

from typing import Any, Sequence

from rem.mTLC.env import TermError

from ....mTLC import TypedTerm

from ....qplcomp import *
from ....qplcomp.qexpr.eqopt import *
from ....qplcomp.qexpr.eiqopt import *

from ...language.ast import *
from ...language.refine import wlp_check

import random

import multiprocessing as mp

def worker_gen(pres: AstPres, workers: list[GenWorker], index: int):

    # workers: list of workers pass in through ListProxy
    worker = workers[index]

    while True:
        
        # generate a new program
        worker.prog_gen()

        if worker.current_prog is not None:
            try:

                # check the refinement relationship
                wlp_check(pres, worker.current_prog, worker.gen_env)

                # return if the current program pass the checking
                worker.sol = worker.current_prog
                workers[index] = worker
                return
            
            except:
                if worker.prog_count % 50 == 0:
                    workers[index] = worker
                
class GenMachine:

    mp.set_start_method('fork')

    def __init__(self, gen_env : Env):
        self.mng = mp.Manager()
        self.working : bool = False

        self.goal : AstPres | None = None

        # gen settings
        self._gen_env : Env = gen_env

        self._max_depth : int = 5
        self._worker_num : int = 8

        self.retry_times : int = 10

        # two proxy lists for the communication between the main process and the workers
        self.workers = self.mng.list([])

        self.threads : list[mp.Process] = []

        self.info = "Ready to generate."

    @property
    def attempt_total(self) -> int:
        return sum([w.prog_count for w in self.workers])
    
    @property
    def sol(self) -> TypedTerm | None:
        '''
        return the solution if it is found
        '''
        for w in self.workers:
            if w.sol is not None:
                return w.sol
        return None
    
    def __str__(self) -> str:
        '''
        return a representation of the finding procedure
        '''

        if self.sol is not None:
            res = str(self.goal)
            res += f"({self.attempt_total})\nSOL FOUND:\n\n{self.sol}"
            return res
        elif len(self.workers) > 0:
            return f"({self.attempt_total})\n{self.workers[0].current_prog}"
        else:
            return self.info
        
    @property
    def gen_env(self) -> Env:
        return self._gen_env
    
    @gen_env.setter
    def gen_env(self, env: Env) -> None:
        '''
        Configure the generation on the fly.
        '''
        self._gen_env = env

        if self.working and self.goal is not None:
            self.gen(self.goal)
        
    @property
    def max_depth(self) -> int:
        return self._max_depth
    
    @max_depth.setter
    def max_depth(self, depth: int) -> None:
        '''
        Configure the generation on the fly.
        '''
        self._max_depth = depth

        if self.working and self.goal is not None:
            self.gen(self.goal)

    @property
    def worker_num(self) -> int:
        return self._worker_num
    
    @worker_num.setter
    def worker_num(self, num: int) -> None:
        '''
        Configure the generation on the fly.
        '''
        self._worker_num = num

        if self.working and self.goal is not None:
            self.gen(self.goal)


    def gen(self, 
            goal: AstPres) -> None:
        '''
        start the generation processes
        '''
        self.terminate()

        self.working = True
        self.goal = goal
        self.workers[:] = []
        self.threads: list[mp.Process] = []

        ############################################################################################
        # collect the quantum variales, check whether the env is sufficient

        try:
            collect_qvars = goal.P.eval(self.gen_env).iqopt.qvar + goal.Q.eval(self.gen_env).iqopt.qvar
        except TermError as e:
            self.info = "Cannot generate, insufficient environment:\n" + str(e)
            return

        for item in self.gen_env.defs.values():
            if isinstance(item, EIQOptAbstract):
                collect_qvars += item.all_qvar
            elif isinstance(item, QProgAst):
                collect_qvars += item.all_qvar

        ############################################################################################
                


        for i in range(self.worker_num):
            self.workers.append(
                GenWorker(
                    self.gen_env, 
                    collect_qvars, 
                    self.retry_times,
                    self.max_depth))
            
            self.threads.append(
                mp.Process(target=worker_gen, 
                           args=(goal, self.workers, i))
            )

        for t in self.threads:
            t.start()

    def initialize(self):
        '''
        initialize the generation machine
        (the configurations are not changed)
        '''

        for t in self.threads:
            t.terminate()
        self.threads = []

        self.goal = None
        self.working = False
        self.workers[:] = []

        self.into = "Ready to generate."


    def terminate(self):
        '''
        terminate all processes
        '''
        for t in self.threads:
            t.terminate()
        self.threads = []
        self.working = False

class GenWorker:
    '''
    The worker for executing an generation.

    Generation rule:
    - abort, prescription, assertion and while are forbidden
    - only provided operators can be utilized
    '''
    def __init__(self, gen_env: Env, qvars: QVar, retry_times, max_depth):
        
        # the expressions available for generation (QOpt, IQOpt, QProg)
        self.gen_env = gen_env

        self.qvars = qvars
        self.retry_times = retry_times
        self.max_depth = max_depth

        self.prog_count = 0
        self.current_prog : TypedTerm | None = None
        self.sol : TypedTerm | None = None

    def prog_gen(self) -> TypedTerm|None:
        '''
        generate a new program
        '''
        res = self.random_prog_gen(self.max_depth)
        self.prog_count += 1
        self.current_prog = res
        return res

    #############################################################
    # qvar generation
    #############################################################

    def random_qvar_gen(self, qubit_num: int) -> EQVar:
        '''
        generate a random qvar of [qubit_num] qubits from qvarls
        '''
        return EQVar(QVar(random.sample(self.qvars._qvls, qubit_num)))
    
    #############################################################
    # operator generation
    #############################################################


    def random_opt_gen(self, qubit_num: int, depth: int) -> TypedTerm|None:
        '''
        Randomly generate an operator.
        '''
        for i in range(self.retry_times):

            # randomly execute one generation rule
            res = random.choice(
                [self.opt_gen_def] * 10 +
                [
                    self.opt_gen_add,
                    self.opt_gen_sub,
                    self.opt_gen_mul,
                    self.opt_gen_dagger,
                    self.opt_gen_tensor,
                    self.opt_gen_disjunct,
                    self.opt_gen_conjunct,
                    self.opt_gen_complement,
                    self.opt_gen_sasaki_imply,
                    self.opt_gen_sasaki_conjunct
                 ]
            )(qubit_num, depth)

            if res is not None:
                return res

    def opt_gen_def(self, qubit_num: int, depth: int) -> TypedTerm|None:
        '''
        Terminal symbol for the random generation of operators.
        '''
        keys = list(self.gen_env.defs.keys())
        for i in range(self.retry_times):
            key = random.choice(keys)
            item = self.gen_env[key]
            if item.type == QOptType(qubit_num):
                return Var(key, self.gen_env)
            
        # give up for this time
        return None
    
    def opt_gen_add(self, qubit_num: int, depth: int) -> EQOptAbstract|None:
        '''
        The generation rule for adding operators.
        '''
        if depth <= 0:
            return None
        
        a = self.random_opt_gen(qubit_num, depth-1)
        b = self.random_opt_gen(qubit_num, depth-1)

        if a is not None and b is not None:
            return EQOptAdd(a, b)   # type: ignore
    
    def opt_gen_sub(self, qubit_num: int, depth: int) -> EQOptAbstract|None:
        '''
        The generation rule for subtracting operators.
        '''
        if depth <= 0:
            return None
        
        a = self.random_opt_gen(qubit_num, depth-1)
        b = self.random_opt_gen(qubit_num, depth-1)
        
        if a is not None and b is not None:
            return EQOptSub(a, b)   # type: ignore
    
    def opt_gen_mul(self, qubit_num: int, depth: int) -> EQOptAbstract|None:
        '''
        The generation rule for multiplying operators.
        '''
        if depth <= 0:
            return None
        
        a = self.random_opt_gen(qubit_num, depth-1)
        b = self.random_opt_gen(qubit_num, depth-1)

        if a is not None and b is not None:
            return EQOptMul(a, b)   # type: ignore
    
    def opt_gen_dagger(self, qubit_num: int, depth: int) -> EQOptAbstract|None:
        '''
        The generation rule for daggering operators.
        '''
        if depth <= 0:
            return None
        
        a = self.random_opt_gen(qubit_num, depth-1)

        if a is not None:
            return EQOptDagger(a)   # type: ignore
    
    def opt_gen_tensor(self, qubit_num: int, depth: int) -> EQOptAbstract|None:
        '''
        The generation rule for tensoring operators.
        '''
        if depth <= 0:
            return None
        
        a_qnum = random.randint(0, qubit_num)

        a = self.random_opt_gen(a_qnum, depth-1)
        b = self.random_opt_gen(qubit_num-a_qnum, depth-1)

        if a is not None and b is not None:
            return EQOptTensor(a, b)   # type: ignore
    
    def opt_gen_disjunct(self, qubit_num: int, depth: int) -> EQOptAbstract|None:
        '''
        The generation rule for disjuncting operators.
        '''
        if depth <= 0:
            return None
        
        a = self.random_opt_gen(qubit_num, depth-1)
        b = self.random_opt_gen(qubit_num, depth-1)

        if a is not None and b is not None:    
            return EQOptDisjunct(a, b)   # type: ignore
    
    def opt_gen_conjunct(self, qubit_num: int, depth: int) -> EQOptAbstract|None:
        '''
        The generation rule for conjuncting operators.
        '''
        if depth <= 0:
            return None
        
        a = self.random_opt_gen(qubit_num, depth-1)
        b = self.random_opt_gen(qubit_num, depth-1)

        if a is not None and b is not None:
            return EQOptConjunct(a, b)   # type: ignore
    
    def opt_gen_complement(self, qubit_num: int, depth: int) -> EQOptAbstract|None:
        '''
        The generation rule for complementing operators.
        '''
        if depth <= 0:
            return None
        
        a = self.random_opt_gen(qubit_num, depth-1)
        
        if a is not None:
            return EQOptComplement(a)   # type: ignore
    
    def opt_gen_sasaki_imply(self, qubit_num: int, depth: int) -> EQOptAbstract|None:
        '''
        The generation rule for Sasaki implication.
        '''
        if depth <= 0:
            return None
        
        a = self.random_opt_gen(qubit_num, depth-1)
        b = self.random_opt_gen(qubit_num, depth-1)

        if a is not None and b is not None:
            return EQOptSasakiImply(a, b)   # type: ignore
    
    def opt_gen_sasaki_conjunct(self, qubit_num: int, depth: int) -> EQOptAbstract|None:
        '''
        The generation rule for Sasaki conjunct.
        '''
        if depth <= 0:
            return None
        
        a = self.random_opt_gen(qubit_num, depth-1)
        b = self.random_opt_gen(qubit_num, depth-1)

        if a is not None and b is not None:
            return EQOptSasakiConjunct(a, b)   # type: ignore
    
    #############################################################
    # indexed operator generation
    #############################################################
    def random_iopt_gen(self, depth: int) -> TypedTerm|None:
        '''
        Randomly generate an indexed operator.
        '''
        for i in range(self.retry_times):

            # randomly execute one generation rule
            res = random.choice(
                [self.iopt_gen_def,
                 self.iopt_gen_pair]
            )(depth)

            if res is not None:
                return res

    def iopt_gen_def(self, depth: int) -> TypedTerm|None:
        '''
        Terminal symbol for the random generation of indexed operators.
        '''
        keys = list(self.gen_env.defs.keys())
        for i in range(self.retry_times):
            key = random.choice(keys)
            item = self.gen_env[key]
            if item.type == IQOptType():
                return Var(key, self.gen_env)
            
        # give up for this time
        return None

    def iopt_gen_pair(self, depth: int) -> EIQOptAbstract|None:
        '''
        The generation rule for pairing indexed operators.
        '''
        if depth <= 0:
            return None
        
        qnum = random.randint(0, self.qvars.qnum)
        O = self.random_opt_gen(qnum, depth - 1)
        qv = self.random_qvar_gen(qnum)

        if O is not None:
            return EIQOptPair(O, qv)   # type: ignore

    #############################################################
    # program generation
    #############################################################

    def random_prog_gen(self, depth: int) -> TypedTerm|None:
        '''
        Randomly generate a program.
        '''
        for i in range(self.retry_times):

            # randomly execute one generation rule
            res = random.choice(
                [
                    self.prog_gen_def,
                    self.prog_gen_skip,
                    self.prog_gen_init,
                    self.prog_gen_unitary,
                    self.prog_gen_if,
                    #self.prog_gen_while
                 ]
            )(depth)

            if res is not None:
                return res

    def prog_gen_def(self, depth: int) -> TypedTerm|None:
        '''
        Terminal symbol for the random generation of programs.
        '''
        keys = list(self.gen_env.defs.keys())
        for i in range(len(keys)):
            key = random.choice(keys)
            item = self.gen_env[key]
            if item.type == QProgType():
                return Var(key, self.gen_env)
            
        # give up for this time
        return None

    def prog_gen_skip(self, depth: int) -> QProgAst|None:
        '''
        The generation rule for skip.
        '''
        return AstSkip()
    
    def prog_gen_init(self, depth: int) -> QProgAst|None:
        '''
        The generation rule for init.
        '''
        qnum = random.randint(0, self.qvars.qnum)
        qv = self.random_qvar_gen(qnum)
        return AstInit(qv)

    def prog_gen_unitary(self, depth: int) -> QProgAst|None:
        '''
        The generation rule for unitary.
        '''
        if depth <= 0:
            return None
        
        U = self.random_iopt_gen(depth - 1)
        if U is not None:
            return AstUnitary(U)   # type: ignore
    
    def prog_gen_if(self, depth: int) -> QProgAst|None:
        '''
        The generation rule for if.
        '''
        if depth <= 0:
            return None
        
        P = self.random_iopt_gen(depth - 1)
        S1 = self.random_prog_gen(depth - 1)
        S0 = self.random_prog_gen(depth - 1)

        if P is not None and S1 is not None and S0 is not None:
            return AstIf(P, S1, S0)   # type: ignore
    
    def prog_gen_while(self, depth: int) -> QProgAst|None:
        '''
        The generation rule for while.
        '''
        if depth <= 0:
            return None
        
        P = self.random_iopt_gen(depth - 1)
        S = self.random_prog_gen(depth - 1)

        if P is not None and S is not None:
            return AstWhile(P, S)   # type: ignore
                