import copy
from pprint import pprint
from prettytable import PrettyTable 

class Lexicale(object):
    def __init__(self):
        self.symbol_table = []
        self.has_scanned = []
        self.tokens = []
        self.error = []
         
        self.keywords = {"if":"IF",
                        "else":"ELSE",
                        "do":"DO",
                        "then":"THEN",
                        "while":"WHILE",
                        "int":"INT",
                        "float":"FLOAT",
                        "char":"CHAR"}
        self.operator = {"+":"ADD",
                         "-":"SUB",
                         "*":"MUL",
                         "/":"DIV",
                         ";":"SEMI",
                         "{":"GLP",
                         "}":"GRP",
                         "(":"LP",
                         ")":"RP"}
        self.relop = ['>','<','=']




    def scan(self, code):
        # setp 1
        code = self.pre_handle(code)
        print("step 1: %s" % code)
  
        # setp 2
        self.has_scanned = []
        self.tokens = []
        self.symbol_table = []
        # state 0 
        current=0
        while(code[current] != '$'):
            # turn to state 1: analyze keywords 
            target = ''
            _next = 0
            if code[current].isalpha():
                target, _next = self.dfa_keyword_identifier(code, current)
            # turn to state 3: analyze digits
            elif code[current].isdigit():
                target, _next= self.dfa_digit(code, current)
            # turn to state 4: analyze operator
            elif code[current] in self.operator.keys():
                target, _next= self.dfa_operator(code, current)
            # turn to state 5: analyze relop
            elif code[current] in self.relop:
                target, _next= self.dfa_relop(code, current)
            # turn to state 6: deal with the error
            else:
               self.error.append(current)
               _next = 1
            if target not in self.has_scanned:
                self.has_scanned.append(target)
            # turn to state 0: continue to analyze
            current += _next    
        
        if len(self.error):
            print("\n\n%s" % code)
            for i in range(0, len(code)+1):
                if i in self.error:
                    print("^", end="")
                else:
                    print(" ", end="")
            print("\nError: invaid character" % self.error)
        tokens = copy.deepcopy(self.tokens)
        self.tokens.reverse()
        return tokens, self.symbol_table                     

    # Remove the blanks and enters in the code string.
    def pre_handle(self, code):
        return "%s$" % code.replace(" ", "").replace("\n", "") 


    def push_tokens(self, target, token):
        self.tokens.append(token)


    def push_symbol_table(self, target, start, length, string, type='', value=''):
        if target not in self.has_scanned:
            symbol = {"start":start, "length":length, "string":string, "type":type, "value":value}
            self.symbol_table.append(symbol)
            return len(self.symbol_table) - 1

    def generate_token(self, token_name, attribute=''):
        #return {"moroheme":morpheme, "token_name":type, "attribute":attribute}
        return (token_name, attribute)

    def dfa_operator(self, code, current):
        token = self.generate_token(self.operator[code[current]])
        _next = 1
        print("Fetch %s --> %s" %(code[current], self.operator[code[current]]))
        self.push_tokens(code[current], token)
        return code[current], _next


    def dfa_keyword_identifier(self, code, current):
        target = ""
        for index in range(current, len(code)):
            if code[index].isalpha():
                target  = "%s%s" % (target, code[index])
                if target in self.keywords.keys():
                    token = self.generate_token(self.keywords[target])
                    _next = len(target)
                    print("Fetch %s --> %s" %(target, self.keywords[target]))
                    self.push_tokens(target, token)
                    return target, _next
            elif code[index].isdigit():
                target  = "%s%s" % (target, code[index])
            # turn to state 2: analyze identifier
            else:
                _next = len(target)
                index = self.push_symbol_table(target, current, _next, target)
                token = self.generate_token("ID", index)
                self.push_tokens(target, token)
                print("Fetch %s --> %s" %(target, "ID"))
                return target, _next

    def dfa_relop(self, code, current):
        target = ""
        s5 = {"token":("EQ", "EQ"), "_next":1, "target":"="}
        s2 = {"token":("LE", "LE"), "_next":2, "target":"<="}
        s3 = {"token":("NT", "NE"), "_next":2, "target":"<>"}
        s4 = {"token":("LE", "LT"), "_next":1, "target":"<"}
        s7 = {"token":("GE", "GE"), "_next":2, "target":">="}
        s8 = {"token":("GT", "GT"), "_next":2, "target":">"}
        end_states = [s5,s2,s3,s4,s7,s8] 
        s1 = {"=":s2, ">":s3, "other":s4}
        s6 = {"=":s7,"other":s8}
        s0 = {"<":s1, "=":s5, ">":s6}
        
        state = s0.get(code[current])
        while(True):
            if state in end_states:
                break
            current = current + 1
            new_state = state.get(code[current], state)
             
            if new_state == state:
                new_state = state.get("other")
            state = new_state 
        _next = len(state['target'])
        self.push_tokens(state['target'], state['token'])
        print("Fetch %s --> %s" %(state['target'], state['token'][1]))
        return state['target'], _next


    def dfa_digit(self, code, current):
        token = dict()
        target = code[current]
        for index in range(current+1, len(code)):
            if code[index].isdigit() or (code[index] == "." and code[index+1].isdigit()):
                target  = "%s%s" % (target, code[index])
            else:
                _next = len(target)
                print("Fetch %s --> %s" %(target, "DIGIT"))
                try:
                    index = self.push_symbol_table(target, current, _next, target, "INT", int(target))
                except ValueError:
                    index = self.push_symbol_table(target, current, _next, target, "FLOAT", float(target))
                token = self.generate_token("DIGIT", index)
                self.push_tokens(target, token)
                return target, _next

    def get_token(self):
        print("Get a token: %s" % str(self.tokens[len(self.tokens)-1]))
        return self.tokens.pop()



    def pretty_print(self, symbol_table):
        print('#\n\n---------Symbol Table---------#')
        cols = ['string', 'start', 'length', 'type','value']
        table = PrettyTable(symbol_table[0].keys())
        table.padding_width = 1
        for i in range(len(symbol_table)):
            temp=[]
            for p in range(len(cols)):
                temp.append(symbol_table[i][cols[p]])
            table.add_row(copy.deepcopy(temp))
        print(table)
        print('#---------Symbol Table---------#')

if __name__ == "__main__":
    code = """
    int a;
    int b=5;
    float c=1.222;
while(a < 40)
{ 
    if (a>=4)
        b=5;
    then
        a=c;
    else
        a=b;
} """
    #code = input("Please input your code:\n")
    scanner = Lexicale()
    tokens, symbol_table = scanner.scan(code)
    for symbol in symbol_table:
        print(symbol)
    scanner.pretty_print(symbol_table)
    #scanner.get_token()












