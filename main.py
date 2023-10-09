
import qpv2
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







rho0 = qpv2.OPTParser.parse("Pm[q]").eval()
print(rho0)

code = '''
    [p] :=0
'''
prog = qpv2.parser.parse(code)
print(prog)

rho_out = qpv2.calc(prog, rho0)
print(rho_out)