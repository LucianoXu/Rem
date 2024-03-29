from ..ast import *

class QProgExtract(QProgAst):
    
    def __init__(self, prog: TypedTerm):
        super().__init__()
        
        self.prog = prog

    def eval(self, env: Env) -> QProgAst:
        prog = self.prog.eval(env)
        assert isinstance(prog, QProgAst), "ASSERTION FAILED"

        return extract(prog)

    def __str__(self) -> str:
        return f"Extract {self.prog}"
        
        
def extract(prog: QProgAst) -> QProgAst:
    if isinstance(prog, (AstAbort, AstSkip, AstInit, AstUnitary, AstAssert)):
        return prog
    
    elif isinstance(prog, AstPres):
        if prog.SRefined is not None:
            return extract(prog.SRefined)
        else:
            return prog
        
    elif isinstance(prog, AstSeq):
        return AstSeq(extract(prog.S0), extract(prog.S1))

    elif isinstance(prog, AstProb):
        return AstProb(extract(prog.S0), extract(prog.S1), prog.p)
    
    elif isinstance(prog, AstIf):
        return AstIf(prog.P, extract(prog.S1), extract(prog.S0))
    
    elif isinstance(prog, AstWhile):
        return AstWhile(prog.P, extract(prog.S))
    
    else:
        raise ValueError(f"Invalid program to extract: {prog}")