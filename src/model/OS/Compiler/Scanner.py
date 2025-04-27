"""
Name

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

    #def advance(self,optional=None):

def main():
    t = Token("STRING","HEY")
    print("What the string is: ",t)

main()
