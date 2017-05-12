#!/usr/bin/env python
# coding=utf-8

import sys

import fire
from lexicale import Lexicale
from  syntax import Syntax

class HappyCompiler(object):
    def __init__(self, verbose=False):
        self.verbose = verbose

        self.scanner = Lexicale()
        self.analyzer = Syntax(self.scanner)

        # For test
        self.test_code = """
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

        # Default productions
        self.like_c_productions =  """
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
        self.analyzer.initialize(self.like_c_productions)


                                                            
    def test(self):
        tokens, symbol_table = self.scanner.scan(self.test_code)
        self.analyzer.parser(tokens)
        if self.verbose:
            self.analyzer.pretty_print()
            self.scanner.pretty_print(symbol_table)
            self.analyzer.tree_print()
        self.analyzer.print(self.test_code, "Source Code")
        
    def show(self):
        self.analyzer.print(self.like_c_productions, "Default Productions")
        self.analyzer.pretty_print()


    def compiler(self):
        while True:
            print("\nInput the source code, and press Ctrl+D to complete the code entry:\n>>> ", end="")
            code = sys.stdin.read()
            tokens, symbol_table = self.scanner.scan(code)
            self.analyzer.parser(tokens)
            self.scanner.pretty_print(symbol_table)
            print('')
            self.analyzer.tree_print()
            self.analyzer.print(code, "Source Code")
            print('')

if __name__ == '__main__':
    fire.Fire(HappyCompiler)

