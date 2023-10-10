
import qpv2

code = '''
    { [pre: P0[p], post: P0[p]]
         = RSKIP => 
      abort }
'''

prog = qpv2.parser.parse(code)
print(prog)