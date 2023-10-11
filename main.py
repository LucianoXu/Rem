
import qpv2

code = '''
    [pre: P0[p], post: P0[p]]
        ==>
    [pre: P0[p], post: Pp[p]]; [pre: Pp[p], post: P0[p]]
'''

prog = qpv2.parser.parse(code)
print(prog)