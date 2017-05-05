from lexicale import Lexicale
from pprint import pprint


class Grammar(object):
    def __init__(self, scanner):
  
        # lecxicale handler
        self.scanner = scanner

        # result
        self.result = list()
        
        # non-terminal symbols
        self.non_ts = []

        # terminal symbols 
        self.ts = []

        # productions
        self.pros = []




    def initialize(self, productions):
        symbol_map = {"+":"ADD",
                      "-":"SUB",
                      "*":"MUL",
                      "/":"DIV",
		      ";":"SEMI",
                      "==":"EE",
                      "=":"EQ",
                      ">":"GT",
                      "<":"LT",
                      ">=":"GE",
                      "<=":"LE",
                      "<>":"NE",
                      "(":"LP",
                      ")":"RP"}
        keywords = ["WHILE", "IF", "DO", "ELSE", "THEN"]
 

        raw_productions = productions.replace(' ','').split('\n')
        self.pros = []
        for p in raw_productions:
            if not p:
                continue
            temp = list(eval(p[3:]))
            for i in range(len(temp)): 
                if temp[i].isalpha():
                    if temp[i].isupper():
                        if temp[i] not in self.ts:
                            self.ts.append(temp[i])
                    else:
                        temp[i] = temp[i].upper()
                        if (temp[i] not in self.non_ts) and (temp[i] not in keywords) :
                            self.non_ts.append(temp[i])
                temp[i] = temp[i].replace(temp[i], symbol_map.get(temp[i], temp[i]))
            self.pros.append((raw_productions.index(p), p[0]) + tuple(temp))
        pprint(self.pros)
        pprint(self.ts)
        pprint(self.non_ts)
            

            
        













if __name__ == "__main__":
    code = """
    int a;
    int b=5;
    float c=1.222;
while(a < 40)
    if (a>=4)
        b=5;
    then
        a=c;
    else
        a=b; """
    #code = input("Please input your code:\n")

    # lexicale section
    scanner = Lexicale()
    #tokens, symbol_table = scanner.scan(code)
    print("\nTOKENS:")
    #for token in tokens:
    #   print(token)
    print("\nSYMBOL_TABLE:")
    #for symbol in symbol_table:
    #    print(symbol)

    # grammar section
    productions = """
            P->('D', 'S')
            D->('L','id',';','D')
            D->('e',)
            L->('int',)
            L->('float',)
            S->('id','=','E',';')
            S->('if','(','C',')','S',';')
            S->('while','(','C',')','S','do','S',';')
            S->('S',';','S')
            C->('E','>','E')
            C->('E','<','E')
            C->('E','==','E')
            E->('E','+','E')
            E->('E','-','E')
            E->('T',)
            T->('F',)
            T->('T','*','F')
            T->('T','/','F')
            F->('(','E',')')
            F->('id',)
"""
    analyzer = Grammar(scanner)
    analyzer.initialize(productions)
