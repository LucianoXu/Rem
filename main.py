
import qpv2



rho0 = qpv2.OPTParser.parse("Pm[q]").eval()
print(rho0)

code = '''
    [p] :=0
'''
prog = qpv2.parser.parse(code)
print(prog)

rho_out = qpv2.calc(prog, rho0, 10)
print(rho_out)