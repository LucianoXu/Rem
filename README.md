# QPV2
`QPV2` is a Python-based interactive tool for quantum program development.
It checks whether operator terms and quantum programs are well-formed, calculates the classical simulation of program execution, checks whether the specified prescription is satisfied, and assists in the step-wise refinement of programs in the sense of partial correctness. 

Efforts are made to balance and ensure that `QPV2` is user-friendly, expressive and automated.
`QPV2` works in an environment of definitions, and a simple imperative language is designed to manipulate the environment and prover in a convenient way. 
The basic operator algebra is implemented in `QPV2`. Although only ground terms (variable-free expressions) are allowed, it enables us to express many verification scenes without too much compromise.
Thanks to Python's numerical calculation and the structure of projective predicates, all properties of operators and programs are decidable here, which makes the tool highly automated.


## Installation

After cloning the repository, navigate to its root folder and run
```
pip install -r requirements.txt
```
It will install all the dependent packages. Afterwards, test whether the software works well by running
```
pytest
```
If the all test are passed then the tool is well installed.

## Hello World Example
This is a simple example demonstrating the function and usage of QPV2. In the example, We refine the prescription $$[\mathrm{pre}: \ket{00}_{p, q} \bra{00}, \mathrm{post}: \ket{++}_{p, q}\bra{++}]$$ with program $prog$ and simulate the computing result.

```python
from qpv2 import *
prover_restart()
prover(
    r'''
    Def HH := (H \otimes H).
    Def prog := Prog HH[p q].
    Refine pf : < P0[p] \otimes P0[q], Pp[p] \otimes Pp[q] >.
        Step proc prog.
    End.
    Def res := [[proc pf]](c1[]).
    '''
)
```

Here is the step-wise explanation.

First we import the package and reset the prover.
```python
from qpv2 import *
prover_restart()
print(prover_info())
```

The prover has a variable environment, and commonly used quantum operators are predefined in the environment. Use `Show Def.` to print all the definitions.
```python
prover(r"Show Def.")
print(prover_info())
```
Use `Show <ID>.` to print the definition.
```pytnon
prover(r"Show CX.")
print(prover_info())
```
Define an operator.
```python
prover(r"Def HH := (H \otimes H). Show HH.")
print(prover_info())
```


```python
Define the program $prog$ using operator $HH$.
prover(r'''
       Def prog := Prog 
            HH[p q]. 
       Show prog.
       ''')
print(prover_info())
```
Then we conduct a refinement. We need a program which transforms $\ket{00}$ state into $\ket{++}$ state, so the program prescription is:
$$
[\mathrm{pre}: \ket{00}_{p, q} \bra{00}, \mathrm{post}: \ket{++}_{p, q}\bra{++}].
$$

```python
prover(r'''
    Refine pf : < P0[p] \otimes P0[q], Pp[p] \otimes Pp[q] >.
''')
print(prover_info())
```
And as the information suggested, we entered the refinement mode. It quite resembles the proof mode in other interactive theorem provers, but here the goals become the prescriptions to be refined.

Actually, the program $prog$ we have defined satisfies this prescription. We then use it to complete the goal and finish the refinement.
```python
prover(r'''
    Step proc prog.
    End.
''')
```
print(prover_info())
Calculate the classical simulation of $\llbracket prog \rrbracket (1)$. Note that here the density operator $1$ is automatically extended to the system of $[p\ q]$, with the assumption that their initial states are $\ket{0}$.

The result state is $\ket{++}_{p,q}$, exactly as expected.

```python
prover(r"Def res := [[proc prog]](c1[]). Show res.")
print(prover_info())
```

## Documentation
This section explains the Python interface, commands and syntax of `QPV2`.

### Python Interface

- `qpv2_code(input_code, opts)`
  
    Reset the prover with extra operators in `opt`, and process the `QPV2` commands in the string `input_code`.

- `qpv2_file(input_path, opts)`
  
    Reset the prover with extra operators in `opt`, and process the `QPV2` commands in the file at `input_path`.

- `qpv2_server(input, output, opts)`
  
    Reset the prover with extra operators in `opt`, and start an interactive server which processes `QPV2` commands in the file `input` and output information in the file `output`.\\
    Note: Modify and save the `input` file to update the input, and use `Ctrl+C` to close the server.

In the following introduction of syntax, $C$ denotes an identifier for a constant, $stm$ denotes a quantum program, $qvar$ denotes a quantum register, $o$ denotes an unlabelled operator and $oi$ denotes a labelled quantum operator.
### `QPV2` commands

- $\texttt{Def}\ C\ \texttt{:=}\ o \texttt{.}$
    
    Define the constant $C$ as the unlabelled operator $o$.
    
- $\texttt{Def}\ C\ \texttt{:=}\ oi \texttt{.}$
  
    Define the constant $C$ as the labelled operator $oi$.
    
- $\texttt{Def}\ C\ \texttt{:= [[}stm \texttt{]](} oi \texttt{).}$
  
    Define the constant $C$ as the classical simulation result of executing quantum program $stm$ on the quantum state $oi$.
    
- $\texttt{Def}\ C\ \texttt{:=}\ \texttt{Prog}\ stm \texttt{.}$
  
    Define the constant $C$ as the quantum program $stm$.
    
- $\texttt{Def}\ C_1\ \texttt{:=}\ \texttt{Extract}\ C_2 \texttt{.}$
    Define the constant $C_1$ as the extracted program of program/proof $C_2$.
    
- $\texttt{Refine}\ C : pres \texttt{.}$
  
    Define $C$ as the prescription $pres$ and start the step-wise refinement mode on it.
      
- $\texttt{Step}\ stm \texttt{.}$
  
    (refinement mode) Try to refine the current goal with program $stm$. 
    
- $\texttt{Step}\ \texttt{Seq}\ oi \texttt{.}$
  
    (refinement mode) Apply the refinement rule $[P, Q] \sqsubseteq [P, R]; [R, Q]$ to the current goal, where $R$ is specified by $oi$.
    
- $\texttt{Step}\ \texttt{If}\ oi \texttt{.}$
  
    (refinement mode) Apply the refinement rule 
    $$
    [P,Q]_{\bar{q}}\equiv if \ R[\bar{q}]\ then \ [R\doublecap P, Q]_{\bar{q}}\ else \ [R^\bot\doublecap P, Q]_{\bar{q}} end
    $$ 
    to the current goal, where $R$ is specified by $oi$.
    
- $\texttt{Step}\ \texttt{While}\ oi_1\ \texttt{Inv}\ oi_2 \texttt{.}$
    
    (refinement mode) Apply the refinement rule 
    $$
    [Inv, P^\bot \doublecap Inv]_{\bar{q}}\le while\ P[\bar{q}]\ do\ [P\doublecap Inv, Inv]_{\bar{q}}\ end
    $$
    to the current goal, where $P$, $Inv$ are specified by $oi_1$, $oi_2$ respectively.
    
- $\texttt{Choose}\ N \texttt{.}$
  
    (refinement mode) Chose the $N$-th goal as the current goal.
    
- $\texttt{End} \texttt{.}$
  
    (refinement mode) Complete the refinement when all goals are clear.
    
- $\texttt{Pause} \texttt{.}$
  
    (interactive server) Pause the parsing of input file so that the current information of the prover can be shown in the output file.
    
- $\texttt{Show}\ \texttt{Def} \texttt{.}$
    
    Print all the names for definitions in the environment.
    
- $\texttt{Show}\ C \texttt{.}$
  
    Print the definition of $C$.
    
- $\texttt{Eval}\ C \texttt{.}$
  
    Evaluate the definition $C$ (e.g. operator expressions) and print the value.
    
- $\texttt{Test}\ o_1\ \texttt{=}\ o_2 \texttt{.}$
  
    Test whether $o_1 = o_2$ for unlabelled operators $o_1$ and $o_2$.
    
- $\texttt{Test}\ o_1\ \texttt{<=}\ o_2 \texttt{.}$
  
    Test whether $o_1 \sqsubseteq o_2$ for unlabelled operators $o_1$ and $o_2$.
    
- $\texttt{Test}\ oi_1\ \texttt{=}\ oi_2 \texttt{.}$
  
    Test whether $oi_1 = oi_2$ for labelled operators $o_1$ and $o_2$.
    
- $\texttt{Test}\ oi_1\ \texttt{<=}\ oi_2 \texttt{.}$
  
    Test whether $oi_1 \sqsubseteq oi_2$ for labelled operators $o_1$ and $o_2$.
### Constructing Program
Quantum program statements, denoted as $stm$, are generated by the following grammar.
- $\texttt{abort}$
- $\texttt{skip}$
- $qvar \texttt{:=0}$
- $oi$
- $\texttt{assert}\ oi$
- $\texttt{< } oi_1\texttt{, } oi_2 \texttt{ >}$
- $ stm_1 \texttt{; }stm_2 $
- $ \texttt{(} stm_1\ \texttt{[} p\ \oplus\texttt{]}\ stm_2 \texttt{)}$
- $ \texttt{if}\ oi\ \texttt{then}\ stm_1\ \texttt{else}\ stm_0\ \texttt{end}$
- $ \texttt{while}\ oi\ \texttt{do}\ stm\ \texttt{end}$
- $ \texttt{proc}\ C$
- $ pres\ \texttt{<=}\ stm$
### Quantum Variables
In QPV2, the whole quantum system consists of qubits, and every qubit is denoted by an identifier (a string following the regular expression `[a-zA-Z\'][a-zA-Z\'0-9]*`). A quantum variable is an ordered list of unique qubit identifiers. For example, valid quantum variables include:
- `[]`, `[p]`, `[p q r']`, ...
  
And invalid quantum variables include:
- `[p p]`, `[1p 2q]`, ...
### Constructing Operators
The grammar for unlabelled quantum variable is:

$$
\begin{aligned}
    o ::=\ &C\ |\ - o\ |\ o + o\ |\ o - o\\
        & |\ c * o\ |\ c\ o\ \\
        & |\ o * o\ |\ o\ o\ |\ o\dagger \\
        & |\ o \otimes o\ \\
        & |\ o \vee o\ |\ o \wedge o\ |\ o\ \^{} \bot \\
        & |\ o \rightsquigarrow o\ |\ o \Cap o.
\end{aligned}
$$
The grammar for labelled quantum variable is:
$$
\begin{aligned}
    oi ::= \ & \text{\texttt{IQOPT}}\ C\ |\ o\ qvar \\
        & |\ -oi\ |\ oi + oi\ |\ oi - oi\\
        & |\ c*oi\ |\ c\ oi\\
        & |\ oi * oi\ |\ oi\ oi\ |\ oi\dagger\\
        & |\ oi \otimes oi\\
        & |\ oi \vee oi\ |\ oi \wedge oi\ |\ oi\ \^{}\bot\\
        & |\ oi \rightsquigarrow oi\ |\ oi \Cap oi.
\end{aligned}
$$
The Unicode characters can be replaced by ASCII strings:
$\dagger$ by \\dagger, $\otimes$ by \\otimes, $\vee$ by \\vee, $\wedge$ by \\wedge, $\bot$ by \\bot, $\rightsquigarrow$ by \\SasakiImply and $\Cap$ by \\SasakiConjunct.