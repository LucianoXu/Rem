
from typing import List

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
    
    def extract(self) -> Ast:
        '''
        Extract the refinement result as a program syntax (without refinement proofs).
        '''
        raise NotImplementedError()

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
        res = prefix + "{\n"
        res += self._Spre.prefix_str(prefix)
        res += prefix + INDENT + "= " + self.rule_sig + " =>\n"
        res += self._Spost.prefix_str(prefix) + " }"
        return res

class RSKIP(Refinement):
    '''
    parameter: none
    '''

    def validity_check(self) -> None:
        type_check(self._Spre, AstPres)
        self._Spre : AstPres

        if not self._Spre.P == self._Spre.Q:
            raise ValueError("RULE SKIP: The pre and post conditions are not equal.")
        
        type_check(self._Spost, AstSkip)

    @property
    def rule_name(self) -> str:
        return "RSKIP"

