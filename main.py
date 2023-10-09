
import qpv2

code = '''
    abort;
    skip;
    [q] :=0 ;
    H[p];
    assert Pp[p];
    [ pre: Pp[p], post: P1[p]];
    ( skip _ 0.52 \\otimes H[p] );
    if P1[q] then
        CX[q p]
    else
        while Pm[p] do
            H[p]
        end
    end
'''

res = qpv2.parser.parse(code)
print(res)