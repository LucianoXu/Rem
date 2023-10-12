import qpv2

def test_01():
    code = r'''
    abort;
    skip;
    [q p] :=0;
    (H \otimes X)[p q];
    assert Pp[p];
    [ pre: Pp[p], post: P1[p]];
    ( skip _ 0.52 \otimes H[p] );
    if (P1[q] \wedge P0[p]) then
        CX[q p]
    else
        while Pm[p] do
            H[p]
        end
    end
    '''
    res = qpv2.parser.parse(code)
    print(res)

def test_forward_calc():
    rho0 = qpv2.OPTParser.parse("c1[]").eval()
    print(rho0)
    code = '''
    [p] :=0;
    [q] :=0;
    skip;
    H[p];
    CX[p q];
    assert P0[p]
    '''
    prog = qpv2.parser.parse(code)
    print(prog)
    print(qpv2.calc(prog, rho0))

def test_forward_calc2():
    rho0 = qpv2.OPTParser.parse("c1[]").eval()
    print(rho0)

    code = '''
    [p] :=0;
    H[p];
    while P0[p] do
        H[p]
    end
    '''
    prog = qpv2.parser.parse(code)
    print(prog)
    print()
    print(qpv2.calc(prog, rho0))

def test_RSKIP():
    rho0 = qpv2.OPTParser.parse("c1[]").eval()
    print(rho0)

    code = '''
    [pre: P0[p], post: P0[p]]
         = RSKIP => 
      skip
    '''

    prog = qpv2.parser.parse(code)
    print(prog)

    rho0 = qpv2.OPTParser.parse("c1[]").eval()
    print(qpv2.calc(prog, rho0))

def test_RPres():
    
    code = '''

        [pre : Omega[t t'], post: (I \\otimes I - P00)[q0 q1] \\otimes Omega[t t']]

        ==>

        [q0 q1] :=0; [pre: P00[q0 q1] \\otimes Omega[t t'], post: (I \\otimes I - P00)[q0 q1] \\otimes Omega[t t']]
    '''

    prog = qpv2.parser.parse(code)
    print(prog)