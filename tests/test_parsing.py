import qpv2
import numpy as np

def test_opt():
    code = r'''
    // Computing operators

    Def II := I \otimes I.

    Test CX[p q] CX[q p] CX[p q] = SWAP[p q].

    Test P0 \otimes P1 <= II.

    Test P0[p] \vee Pp[q] = I[p].
    '''
    qpv2.qpv2_code(code)

def test_01():
    code = r'''
    Def prog := Prog
        abort;
        skip;
        [q p] :=0;
        (H \otimes X)[p q];
        assert Pp[p];
        < Pp[p], P1[p] >;
        ( skip [0.52 \oplus] H[p] );
        if (P1[q] \wedge P0[p]) then
            CX[q p]
        else
            while Pm[p] do
                H[p]
            end
        end;
        < P0[p], P1[p] > <= X[p].
    '''
    qpv2.qpv2_code(code)

def test_forward_calc():
    code = r'''
    Def prog := Prog
        [p] :=0;
        [q] :=0;
        skip;
        H[p];
        CX[p q];
        assert P0[p].

    Def rho := [[ proc prog ]](c1[]).
    '''
    qpv2.qpv2_code(code)

def test_forward_calc2():
    code = r'''
    Def prog := Prog
        [p] :=0;
        H[p];
        while P0[p] do
            H[p]
        end.

    Def rho := [[ proc prog ]](c1[]).
    '''
    qpv2.qpv2_code(code)

def test_Refine():
    code = r'''
    // Subprograms and proofs.

    Def prog := Prog X[x].
    Show prog.

    Refine pfsub : < P0[x], P1[x] >.

        Step proc prog.

    End.
    Show pfsub.

    Def rho1 := [[proc pfsub]](P0[x]).
    Show rho1.    
    '''

    qpv2.qpv2_code(code)

from qplcomp.qval import predefined

def test_RExample():
    opts = {
        "Rztheta" : predefined.Rz(np.arccos(3/5))
    }

    code = r'''

    // The example in the draft.

    Def P00 := P0 \otimes P0.

    Def Inv0 := ((I \otimes I - P00)[q0 q1] \otimes Omega[t t']) \vee (P00[q0 q1] \otimes (Rztheta[t] Omega[t t'] Rztheta[t]^\dagger)).

    // simplified style.

    Refine pf : < Omega[t t'], Rztheta[t] Omega[t t'] Rztheta[t]^\dagger>.


        Step Seq (I \otimes I - P00)[q0 q1] Omega[t t'].

        Step 
            [q0 q1] :=0; X[q0].


        Step 
            While (I \otimes I - P00)[q0 q1] 
            Inv IQOPT Inv0.

        Step 
            [q0 q1] :=0; < P00[q0 q1] \otimes Omega[t t'], IQOPT Inv0>.

        Step 
            H[q0]; H[q1];
            < Pp[q0] \otimes Pp[q1] \otimes Omega[t t'], IQOPT Inv0>.

        Step
            CCX[q0 q1 t]; S[t]; CCX[q0 q1 t];
            // problem?
            H[q0]; H[q1];
            if (I \otimes I - P00)[q0 q1] then
                Z[t]
            else
                skip
            end.
    End.

    Def pfextract := Extract pf.
    Show pfextract.
    //Pause.

    Def rho2 := [[proc pf]](Pp[t]).
    Show rho2.
    '''

    qpv2.qpv2_code(code, opts)