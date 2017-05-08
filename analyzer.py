import sys

from lexicale import Lexicale
from  syntax import Syntax


test_code1 = """
    int a;
    int b=a+1;
    float c=1.222;
        while(a < 40)
    if (a>=4)
        b=5;
    else
        a=b; """

test_code2 = """
    int a;
    int b;
    int c;
    a=b+2;
    b=c+3;
    while (a>c)
    if (a>b)
        c=a+b;
    else
        c=a-b;
    """
productions = """
        Q->('D','S')
        D->('L','id',';','D')
        D->('null',)
        L->('int',)
        L->('float',)
        S->('id','=','E')
        S->('S',';', "S")
        S->('null',)
        S->('if', '(','C',')', 'S')
        S->('if', '(','C',')','S','else', 'S')
        S->('while', '(','C',')', 'S')
        C->('E','>','E')
        C->('E','<','E')
        C->('E','==','E')
        E->('E','+','T')
        E->('E','-','T')
        E->('T',)
        T->('F',)
        T->('T','*','F')
        T->('T','/','F')
        F->('(','E',')')
        F->('id',)
        F->('digit',)
    """
scanner = Lexicale()
analyzer = Syntax(scanner)
analyzer.initialize(productions)
analyzer.pretty_print()

while (True):
    print("\nInput the source code, and press Ctrl+D to complete the code entry:")
    code = sys.stdin.read()
    tokens, symbol_table = scanner.scan(code)
    scanner.pretty_print(symbol_table)
    analyzer.parser(tokens)
    analyzer.tree_print()
    analyzer.print(code, "Source Code")
    print("")
