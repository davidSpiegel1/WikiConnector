"""
Name: Scanner.py
Purpose: To take a string input and tokenize it. 
Notes:
        * I am rewriting this code for it to be more readable and also faster.
        * I am also making the 'ls' and 'cd' other functions that can run inside the kernel instead of here.

"""

import os
import traceback
import subprocess
import re

# Defining some needed token types
KEYWORDS = ['IF','THEN','ELSE','FOR','WHILE','DO','FUNC','IN','SELECT','PAREN','EOF']
MSC = {'COMMENTS':'#','LPAREN':'(','RPAREN':')','+':'ADD','-':'SUB','*':'MUL','/':'DIV'}
#keyReg = r'\b(?:' + '|'.join(KEYWORDS+MSC) + r')\b'
# Defining some token types
NUMBER,EOF,IDENTIFIER = ('NUMBER','EOF','IDENTIFIER')


#finalReg = '|'.join(KEYWORDS)
#regex = re.compile(finalReg)

#print("final Reg: ",finalReg)
class Token:
    def __init__(self,kind,val):
        self.kind = kind
        self.val = val
        #self.MSC = MSC
    def __repr__(self):
        return f'token({self.kind},{self.val})'

class Scanner:
    def __init__(self,text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos] if len(self.text) > 0 else None
        self.KEYWORDS = {}
        self.OPERATORS = {}
        self.populateKeywords()
        self.MSC = MSC

    def populateKeywords(self):
        for key in KEYWORDS:
            self.KEYWORDS[key.lower()] = key.upper()

    def advance(self,optional=None):
        if optional is None:
            self.pos += 1
        else:
            self.pos += len(optional)
        if self.pos > len(self.text)-1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    # Removed checking for ',' because there is a better way.
    """def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()"""
    
    # Going to try to do this all with one module
    def next_token (self):
        if self.pos < len(self.text):
            self.current_char = self.text[self.pos] if len(self.text) > 0 else None
        else:
            self.current_char = None
        while self.current_char is not None:
            
            if self.current_char.isspace():
                while self.current_char.isspace():
                    self.advance()
            # Getting a number
            if self.current_char.isdigit():
                num = ''
                while self.current_char is not None and self.current_char.isdigit():
                    num += self.current_char
                    self.advance()
                return Token(NUMBER,int(num))    
            # Getting a character (Identifier)
            if self.current_char.isalpha():
                ids = ''
                while self.current_char is not None and (self.current_char.isalpha() or self.current_char.isdigit() or self.current_char == '_'):
                    ids += self.current_char
                    self.advance()
                if ids in self.KEYWORDS:
                    return Token(self.KEYWORDS[ids],ids)
                elif ids in self.MSC.values():
                    return Token(ids,self.MSC[ids])
                else:
                    return Token(IDENTIFIER,ids)
            elif self.current_char in self.MSC.values():
                
                return Token(self.current_char,self.MSC[self.current_char])
            # Possibly delete this!
            else:
                self.advance()
        #for m in regex.finditer(self.text):
        #    print(m.group())
    def scan (self):
        scanList = []
        sc = self.next_token()
        while sc is not None:
            scanList.append(sc)
            #print("NEXT TOKEN: ")
            sc = self.next_token()
        return scanList

def main():
    #t = Token("STRING","HEY")
    script = '''x=10; if x = 10 then x=x+x'''
    print("Script: ",script)
    sc = Scanner(script)
    #print(sc.next_token())
    print(sc.scan())
    #print("What the string is: ",t)



main()
