#!/usr/bin/python

import time

keyword = ["if", "else", "while", "then", "do"]
variable_type = ["int", "float", "char"]
unary_operator = ["+","-","*","/","(",")","{","}",";","'","=", ">", "<", "!"]
binary_oprator = ["==",">=","<=","!="]
symbol_table = []



def is_keyword(target):
    if target in keyword:
        return True
    return False

def is_variable_type(target):
    if target in variable_type:
        return True
    return False

def is_operator(target, unary=True):
    if unary:
        if target in unary_operator:
            return True
        return False
    else:
        if target == "=":
            return True
        else:
            return False 

def scan_number(code, current):
    token = dict()
    target = code[current]
    for index in xrange(current+1, len(code)):
        if code[index].isdigit() or (code[index] == "." and code[index+1].isdigit()):
            target  = "%s%s" % (target, code[index])
        else:
            token[target] = "DIGIT"
            _next = len(target)
            print("Fetch %s --> %s" %(target, "DIGIT"))
            return target, token, _next


def scan_keyword_id(code, current):
    token = dict()
    is_declare = False
    variable_type = ""
    target = ""
    for index in xrange(current, len(code)):
        if code[index].isalpha():
            target  = "%s%s" % (target, code[index])
            # is type of variables ?
            if is_variable_type(target):
                is_declare = True
                variable_type = target
                target = ""
            # is keyword ?
            if is_keyword(target):
                token[target] = "KEYWORD"
                _next = len(target)
                print("Fetch %s --> %s" %(target, "KEYWORD"))
                return target, token, _next
        if code[index].isdigit():
            target  = "%s%s" % (target, code[index])
        if is_operator(code[index]) or code[index] == "$":
            if is_declare:
                symbol = dict()
                symbol["name"] = target
                symbol["type"] = variable_type
                symbol_table.append(symbol)
            token[target] = "ID"
            _next = len("%s%s" % (target, variable_type))
            print("Fetch %s --> %s" %(target, "ID"))
            return target, token, _next


def scan_operator(code, current):
    token = dict()
    target = ""
    if is_operator(code[current+1], unary=False):
        target = "%s%s" % (code[current], code[current+1])
    else:
        target = code[current]
    token[target] = "OPERATOR"
    _next = len(target)
    print("Fetch %s --> %s" %(target, "OPERATOR"))
    return target, token, _next
 

def scan(code):
    tokens=[]
    has_analyzed = []
    # code: while(a<4)if(a>=4)b=5;thena=c;elsea=b$
    time.sleep(1)
    print("1. Original Code:")
    time.sleep(1)
    print(code)
    time.sleep(1)
    code ="%s$" % code.replace(" ", "").replace("\n", "")
    print("2. Remove blanks and enters: \n    %s" %code)   
    time.sleep(1)
    print("3. Analyzing...")   
    time.sleep(1)
    current=0
    while(code[current] != "$"):
        time.sleep(1)
        #print(len(code))
        #print(current)
        token = {}
        # is id or keyword ?
        if code[current].isalpha():
            target, token, _next = scan_keyword_id(code, current)                    
        # is unary or binary operator ?
        if is_operator(code[current]):
            target, token, _next = scan_operator(code, current)                    
        if code[current].isdigit():
            target, token, _next = scan_number(code, current)
        current += _next
        if target not in has_analyzed:
            has_analyzed.append(target)
            tokens.append(token)
    return tokens 

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

    tokens = scan(code)
    print("\nTOKENS:")
    for token in tokens:
        print(token)
    print("\nSYMBOL_TABLE:")
    for symbol in symbol_table:
        print(symbol)




