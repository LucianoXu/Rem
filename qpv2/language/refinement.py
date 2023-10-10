
from typing import List

from qpv2.language.ast import Ast

from ..qplcomp import Expr
from ..sugar import type_check
from . import *

class Refinement(Ast):
    '''
    The proof of refinement relation `S0 \\sqsubseteq S1`
    The subclass of `Refinement` defines different rules allowed (thus the shallow embedding).
    A refinement instance should also contains the information of the application of particular refinement rule.

    IMPORTANT
    +++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    We define `Refinement` as the subclass of `Ast`, because a refinement proof can be considered as a special kind of program - the one with a chained refinement history.
    +++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    And we can even parse this refinement proof!
    '''
    def __init__(self, Spre : Ast, Spost : Ast, parals : List[Expr]):
        type_check(Spre, Ast)
        type_check(Spost, Ast)
        type_check(parals, list)

        self._Spre = Spre
        self._Spost = Spost
        self._parals = parals

        self.validity_check()

    def validity_check(self) -> None:
        '''
        Check whether the rule applied here is valid.
        Raise an error when it is not.
        '''
        raise NotImplementedError()
    
    @property
    def rule_name(self) -> str:
        '''
        The name of the rule.
        '''
        raise NotImplementedError()

    @property
    def rule_sig(self) -> str:
        '''
        The signature of the rule applied for this refinement relation.
        It will looks like : 'RULE0(para0, para1, ...)'
        '''
        res = self.rule_name
        if len(self._parals) == 0:
            res += "[]"
        else:
            res += "[" + str(self._parals[0])
            for i in range(1, len(self._parals)):
                res += ", " + str(self._parals[i])
            res += "]"
        return res


    @property
    def Spre(self) -> Ast:
        return self._Spre

    @property
    def Spost(self) -> Ast:
        return self._Spost

    @property
    def definite(self) -> bool:
        
        # whether a refinement is definite is determined by the post refinement statement `Spost`.
        return self._Spost.definite
    
    def prefix_str(self, prefix = "") -> str:
        res = self._Spre.prefix_str(prefix) + "\n"
        res += prefix + INDENT + "= " + self.rule_sig + " => {\n"
        res += self._Spost.prefix_str(prefix) + " }"
        return res
    
    @property
    def extract(self) -> Ast:
        return self._Spost.extract
    
    @property
    def proof_root(self) -> Ast:
        return self.Spre.extract


class RSKIP(Refinement):
    '''
    Lemma 4.5 (1)
    [P, P]_{q} \\sqsubseteq skip

    parameter: none
    '''

    def validity_check(self) -> None:
        Spre = self._Spre.extract
        Spost = self._Spost.proof_root
        type_check(Spre, AstPres)
        type_check(Spost, AstSkip)

        if not Spre.P == Spre.Q:    # type: ignore
            raise ValueError("RULE SKIP: The pre and post conditions are not equal.")
        

    @property
    def rule_name(self) -> str:
        return "RSKIP"
    

class RIMPLY(Refinement):
    '''
    Lemma 4.5 (2)
    [P, Q]_{q} \\sqsubseteq [R, T]_{q} if P \\sqsubseteq R and T \\sqsubseteq Q

    parameters: none, inferred from Spost
    '''

    def validity_check(self) -> None:
        Spre = self._Spre.extract
        Spost = self._Spost.proof_root

        type_check(Spre, AstPres)
        type_check(Spost, AstPres)

        # check P \\sqsubseteq R
        if not Spre.P <= Spost.P:    # type: ignore
            raise ValueError("RULE IMPLY: P \\sqsubseteq R not satisfied.")

        # check T \\sqsubseteq Q
        if not Spost.Q <= Spre.Q:    # type: ignore
            raise ValueError("RULE IMPLY: T \\sqsubseteq Q not satisfied.")

    @property
    def rule_name(self) -> str:
        return "RIMPLY"
    
class RSEQ(Refinement):
    '''
    Lemma 4.5 (3)
    [P, Q]_{q} \\sqsubseteq [P, R]_{q}; [R, Q]_{q}

    parameters: none
    '''

    def validity_check(self) -> None:
        Spre = self._Spre.extract
        Spost = self._Spost.proof_root

        type_check(Spre, AstPres)
        type_check(Spost, AstSeq)
        S0 = Spost.S0 # type: ignore
        S1 = Spost.S1 # type: ignore
        type_check(S0, AstPres)
        type_check(S1, AstPres)


        # check P
        if not Spre.P == S0.P:    # type: ignore
            raise ValueError("RULE SEQ: invalid P.")

        # check Q
        if not Spre.Q == S1.Q:    # type: ignore
            raise ValueError("RULE SEQ: invalid Q.")
        
        # check R
        if not S0.Q == S1.P:
            raise ValueError("RULE SEQ: invalid R.")

    @property
    def rule_name(self) -> str:
        return "RSEQ"
    
