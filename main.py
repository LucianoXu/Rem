
import numpy as np

import qpv2

from qplcomp.qval import predefined
from qplcomp import Parser, QOpt

from qplcomp.qexpr.eqopt import EQOpt

Parser.Global["Rztheta"] = EQOpt(QOpt(predefined.Rz(np.arccos(3/5))), Parser.Global)

Inv = Parser.parse('''((I \\otimes I - P00)[q0 q1] \\otimes Omega[t t']) \\vee (P00[q0 q1] \\otimes (Rztheta[t] Omega[t t'] Rztheta[t]^\\dagger))''')

Parser.Global["Inv"] = Inv

code = '''
    [pre : Omega[t t'], post: Rztheta[t] Omega[t t'] Rztheta[t]^\\dagger]

    ==>

    {
        [pre : Omega[t t'], post: (I \\otimes I - P00)[q0 q1] \\otimes Omega[t t']]

        ==>

        [q0 q1] :=0; X[q0]
    }; 
    {
        [pre : (I \\otimes I - P00)[q0 q1] \\otimes Omega[t t'], post: Rztheta[t] Omega[t t'] Rztheta[t]^\\dagger]
        
        ==>

        {
            [pre: IQOPT Inv, post: P00[q0 q1] \\SasakiConjunct IQOPT Inv]

            ==>
            while (I \\otimes I - P00)[q0 q1] do
                {
                    [pre: (I \\otimes I - P00)[q0 q1] \\SasakiConjunct IQOPT Inv, post : IQOPT Inv]
                    
                    ==>

                    {
                        [pre: (I \\otimes I - P00)[q0 q1] \\otimes Omega[t t'], post: IQOPT Inv]

                        ==>

                        {
                            [q0 q1] :=0;

                            {
                                [pre: P00[q0 q1] \\otimes Omega[t t'], post: IQOPT Inv]

                                ==>

                                H[q0]; H[q1];

                                {
                                    [pre: Pp[q0] \\otimes Pp[q1] \\otimes Omega[t t'], post: IQOPT Inv]

                                    ==>

                                    CCX[q0 q1 t]; S[t]; CCX[q0 q1 t];

                                    
                                    // problem?
                                    H[q0]; H[q1];
                                    if (I \\otimes I - P00)[q0 q1] then
                                        Z[t]
                                    else
                                        skip
                                    end
                                    
                                }                 
                            }
                        }
                    }
                }
            end
        }
    }
'''

prog = qpv2.parser.parse(code)
with open("s.txt",  "w", encoding= 'utf-8') as p:
    p.write(str(prog))
    p.write("\n===================================================\n")
    p.write(str(prog.extract))
print(prog)
print()
print(prog.extract)