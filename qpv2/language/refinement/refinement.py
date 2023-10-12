
from typing import List

from qpv2.language.ast import Ast
from qpv2.qplcomp import IQOpt

from ...qplcomp import Expr
from ...sugar import type_check
from ..ast import *

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
            pass
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
        res += prefix + INDENT + "=" + self.rule_sig + "=> {\n"
        res += self._Spost.prefix_str(prefix) + " }"
        return res
    
    @property
    def extract(self) -> Ast:
        return self._Spost.extract
    
    @property
    def proof_root(self) -> Ast:
        return self.Spre.extract
    
    def wlp(self, post: IQOpt) -> IQOpt:
        return self.extract.wlp(post)




class RPres(Refinement):
    '''
    Refinement from prescriptions. Validity check conducted by wlp calculation.
    '''
    def __init__(self, Spre : AstPres, Spost : Ast, parals : List[Expr]):
        type_check(Spre, AstPres)
        
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
        # check whether wlp relation is satisfied
        if not self._Spre.P <= self._Spost.wlp(self._Spre.Q):
            raise ValueError("The relation P <= wlp.S.Q is not satisfied.")
    
    @property
    def rule_name(self) -> str:
        '''
        The name of the rule.
        '''
        return ""

    @property
    def rule_sig(self) -> str:
        '''
        The signature of the rule applied for this refinement relation.
        It will looks like : 'RULE0(para0, para1, ...)'
        '''
        res = self.rule_name
        if len(self._parals) == 0:
            pass
        else:
            res += "[" + str(self._parals[0])
            for i in range(1, len(self._parals)):
                res += ", " + str(self._parals[i])
            res += "]"
        return res