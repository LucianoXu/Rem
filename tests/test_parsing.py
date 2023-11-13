import quire
import numpy as np

def test_opt():
    code = r'''
    // Computing operators

    Def II := I \otimes I.

    Test CX[p q] * CX[q p] * CX[p q] = SWAP[p q].

    Test P0 \otimes P1 <= II.

    Test P0[p] \vee Pp[q] = I[p].
    '''
    quire.quire_code(code)

def test_01():
    code = r'''
    Def prog := Prog
        abort;
        skip;
        [q p] :=0;
        (H \otimes X)[p q];
        assert Pp[p];
        < Pp[p], P1[p] >;
        ( skip [\oplus 0.52] H[p] );
        if (P1[q] \wedge P0[p]) then
            CX[q p]
        else
            while Pm[p] do
                H[p]
            end
        end;
        < P0[p], P1[p] > <= X[p].
    '''
    quire.quire_code(code)

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
    quire.quire_code(code)

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
    quire.quire_code(code)

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

    quire.quire_code(code)

from qplcomp.qval import predefined

def test_RExample():
    opts = {
        "Rz" : predefined.Rz(np.arccos(3/5))
    }

    code = r'''

        Show Def.

        // Computing operators

        Def II := I \otimes I.

        Test CX[p q] * CX[q p] * CX[p q] = SWAP[p q].

        Test P0 \otimes P1 <= II.

        Test P0[p] \vee Pp[q] = I[p].


        // Subprograms and proofs.

        Def prog := Prog X[x].
        Show prog.

        Refine pfsub : < P0[x], P1[x] >.

            Step proc prog.

        End.
        Show pfsub.

        Def rho1 := [[proc pfsub]](P0[x]).
        Show rho1.




        // The example in the draft.
        Def P00 := P0 \otimes P0.
        Def Pnot00 := (I \otimes I - P00).

        Def pCircuit := Prog
            H[q0]; H[q1];
            CCX[q0 q1 t]; S[t]; CCX[q0 q1 t];
            H[q0]; H[q1];
            if Pnot00[q0 q1] then Z[t] else skip end.

        Refine pf : < Omega[t t'], Rz[t] * Omega[t t'] * Rz[t]^\dagger >.


            Step Seq Pnot00[q0 q1] * Omega[t t'].
            
            Step [q0 q1] :=0; X[q0].

            Def Inv0 := (Pnot00[q0 q1] \otimes Omega[t t']) \vee (P00[q0 q1] \otimes (Rz[t] * Omega[t t'] * Rz[t]^\dagger)).

            Step While Pnot00[q0 q1] Inv IQOPT Inv0.

            Step Seq P00[q0 q1] \otimes Omega[t t'].
            
            Step [q0 q1] :=0.

            Step proc pCircuit.
        End.
        Show pf.
        Def S0:= Extract pf. Show S0.
        Def rho := [[proc S0]](Pp[t]). Show rho.

    '''

    quire.quire_code(code, opts)