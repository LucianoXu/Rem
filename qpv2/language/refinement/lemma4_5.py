
from .refinement import Refinement, type_check
from ..ast import *


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
    
