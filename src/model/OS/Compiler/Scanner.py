"""
Name: Scanner.py
Purpose: To take a string input and tokenize it. 
Notes:
        * I am rewriting this code for it to be more readable and also faster.
"""

import os
import traceback
import subprocess

class Token:
    def __init__(self,kind,val):
        self.kind = kind
        self.val = val
    def __repr__(self):
        return f'token({self.kind},{self.val})'

class Scanner:
    def __init__(self,text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos] if len(self.text) > 0 else None

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
    def scan (self,text):
        self.current_char = self.text[self.pos] if len(self.text) > 0 else None
        while self.current_char is not None:
            if self.current_char.isspace():
                self.advance()


    

    
def main():
    t = Token("STRING","HEY")
    print("What the string is: ",t)

main()
