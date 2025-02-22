# To be the database engine for the query of data
import csv
import sys
# Define token types
NUMBER, select, where, AND, OR, column, RPAREN, EOF, equal, lessThan, greaterThan,LS,CD,RM,CAT,MKDIR,RUN,USERADD,PASSWD,SU,USERMOD,PWD = (
    'NUMBER', 'select', 'where', 'AND', 'OR', 'column', 'RPAREN', 'EOF','=','LESS','GREAT','ls','cd','rm','cat','mkdir','run','useradd','passwd','su','usermod','pwd'
)

import subprocess
import os
import pickle
import traceback
#from Kernel import *

class Token:
    def __init__(self,t,val):
        self.t = t
        self.val = val
    def __repr__(self):
        return f'token({self.t},{self.val})'
class Scanner:
    def __init__(self,text):
        self.text = text
        self.pos = 0 
        self.current_char = self.text[self.pos] if len(self.text) >0 else None

    def advance(self,optional=None):
        if optional is None:
            self.pos += 1
        else:

            self.pos += len(optional)
        if self.pos > len(self.text)-1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]
    def skip_whitespace(self):
        while self.current_char is not None and (self.current_char.isspace() or self.current_char == ','):
            self.advance()

    def number(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit() and not self.current_char.isspace():
            result += self.current_char
            self.advance()
        return Token(NUMBER,int(result))

    def column(self):
        result = ''
        while self.current_char is not None and self.current_char.isalnum() or self.current_char == "_" or self.current_char in (".",".."):
            result += self.current_char
            self.advance()
        return Token(column,result)

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace() or self.current_char == ',':
                self.skip_whitespace()
                continue
            if self.current_char.isdigit():
                return self.number()
            if self.current_char == '=':
                self.advance()
                return Token(equal,'=')
            if self.current_char == '<':
                self.advance()
                return Token(lessThan,'<')
            if self.current_char == '>':
                self.advance()
                return Token(greaterThan,'>')
            if self.current_char == 'AND':
                self.advance()
                return Token(AND,'AND')
            if self.current_char.lower() == 'or':
                self.advance()
                return Token(OR,'OR')
            """if self.current_char.lower() == 'ls':
                self.advance()
                return Token(LS,'ls')
            if self.current_char.lower() == 'cd':
                self.advance()
                return Token(CD,'cd')
            if self.current_char.lower() == 'rm':
                self.advance()
                return Token(RM,'rm')"""
            if self.current_char.isalpha() or self.current_char == '_' or self.current_char == '.':
                print("The select:",self.current_char) 
                if self.pos+len('select') < len(self.text) and self.text[self.pos:self.pos+len('select')]=='select':
                    self.advance('select')
                    return Token(select,'select')

                #if self.current_char == 'where':
                elif self.pos+len('where') < len(self.text) and self.text[self.pos:self.pos+len('where')] == 'where':
                    self.advance('where')
                    return Token(where,'where')
                elif self.pos+len('ls') < len(self.text)+1 and self.text[self.pos:self.pos+len('ls')]=='ls':
                    #print("DO WE GET GERE??")

                    self.advance('ls')
                    return Token(LS,'ls')
                
                elif self.pos+len('mkdir') < len(self.text)+1 and self.text[self.pos:len('mkdir')]=='mkdir':
                    self.advance('mkdir')
                    return Token(MKDIR,'mkdir')
                elif self.pos+len('cd') < len(self.text)+1 and self.text[self.pos:self.pos+len('cd')] == 'cd':
                    self.advance('cd')
                    return Token(CD,'cd')
                elif self.pos+len('rm') < len(self.text)+1 and self.text[self.pos:self.pos+len('rm')] == 'rm':
                    self.advance('rm')
                    return Token(RM,'rm')
                elif self.pos+len('cat') < len(self.text)+1 and self.text[self.pos:self.pos+len('cat')] == 'cat':
                    self.advance('cat')
                    return Token(CAT,'cat')
                elif self.pos+len('run') < len(self.text)+1 and self.text[self.pos:self.pos+len('run')]=='run':
                    self.advance('run')
                    return Token(RUN,'run')
                elif self.pos+len('useradd') < len(self.text)+1 and self.text[self.pos:self.pos+len('useradd')]=='useradd':
                    self.advance('useradd')
                    return Token(USERADD,'useradd')
                elif self.pos+len('passwd') < len(self.text)+1 and self.text[self.pos:self.pos+len('passwd')]=='passwd':
                    self.advance('passwd')
                    return Token(PASSWD,'passwd')
                elif self.pos+len('su') < len(self.text)+1 and self.text[self.pos:self.pos+len('su')]=='su':
                    self.advance('su')
                    return Token(SU,'su')
                elif self.pos+len(USERMOD) < len(self.text)+1 and self.text[self.pos:self.pos+len(USERMOD)]==USERMOD:
                    self.advance(USERMOD)
                    return Token(USERMOD,USERMOD)
                elif self.pos+len(PWD) < len(self.text)+1 and self.text[self.pos:self.pos+len(PWD)]==PWD:
                    self.advance(PWD)
                    return Token(PWD,PWD)
                else:
                    return self.column()

            raise Exception(f'Invalid character')
        return Token(EOF,None)

class Parser:
    def __init__(self,scanner):
        self.scanner = scanner
        self.current_token = self.scanner.get_next_token()
        #print(self.current_token)
    def error (self):
        raise Exception('Invalid syntax')
    
    def eat(self,token_type):
        if self.current_token.t == token_type:
            self.current_token = self.scanner.get_next_token()
            print("the new token: ",self.current_token)
        else:
            self.error()
    def bash (self):
        token = self.current_token
        if token.t in {CD,LS,RM,CAT,MKDIR,RUN,USERADD,PASSWD,SU,USERMOD,PWD}:
            n = {'type': token.t,'right': None}
            self.eat(token.t)
            n1 = self.term()
            n['right'] = n1
            return n
        else:
            return self.term()


    def select (self):
        token = self.current_token
        if token.t == select:
            n = {'type':token.t,'right':None,'where':None}
            self.eat(select)
            n1 = self.expression()
            n['right'] = n1
            if self.current_token.t == where:
                self.eat(where)
                n2 = self.expression()
                n['where'] = n2
                return n
            else:
                return n
        #elif token.t in {CD,LS,RM,ECHO}:
        #    return self.bash()
    def expression (self):
        node = self.term()
        while self.current_token.t in (equal,lessThan,greaterThan,AND,OR,USERMOD):
            token = self.current_token
            if token.t == equal:
                self.eat(equal)
            elif token.t == lessThan:
                self.eat(lessThan)
            node = {'type': token.t,'left':node,'right':self.term()}
        return node 
        
    def term(self):
        a = None
        if self.current_token.t == column:
            result = '' 
            while self.current_token.t == column:
                result += ' '+self.current_token.val
                self.eat(column)

            a = {'type':column,'val':result}
            #self.eat(column)
            
        elif self.current_token.t == NUMBER:
            a = {'type':self.current_token.t,'val':self.current_token.val}
            self.eat(NUMBER) 
        elif self.current_token.t == EOF:
            return
        else:
            self.error()
        return a
    def parse(self):
        print("What the first token is: ",self.current_token.t)

        if self.current_token.t == select:
            return self.select()
        elif self.current_token.t in (LS,MKDIR,CD,CAT,RM,RUN,USERADD,PASSWD,SU,USERMOD,PWD):
            return self.bash()
        
class Interpreter:
    def __init__(self,parser):
        self.parser = parser
        self.variables = {}

    def interpret(self):
        ast = self.parser.parse()
        print("The final ast: ",ast)
        return self.visit(ast)
    def visit(self,ast):
        if ast is not None and ast['right'] is not None:
            self.visit_Expr(ast['right'])
        if ast is not None and 'where' in ast and ast['where'] is not None:
            self.visit_Expr(ast['where'])
        if ast is not None and ast['type'] == column:
            self.variables['column'] = ast['val']
        if ast is not None and ast['type'] in (LS,MKDIR,CD,CAT,RM,RUN,USERADD,PASSWD,SU,USERMOD,PWD):
            self.variables['bash'] = ast['type']
            #self.variables['args'] = ast['right']
        return self.variables
    def visit_Expr(self,ast):
        if ast['type'] == equal:
            self.visit_assign(ast['left'],ast['right'])
        if ast['type'] == lessThan:
            self.visit_less(ast['left'],ast['right'])
        if ast['type'] == greaterThan:
            self.visit_great(ast['left'],ast['right'])
        if ast['type'] == column:
            self.variables['column'] = ast['val']
    def visit_assign(self,left,right):
        if left['type'] == column:
            if right['type'] == NUMBER or right['type'] == column:
                self.variables[left['val']] = right['val']
            else:
                Exception('Error. Left Right not good')
        elif left['type'] == NUMBER:
            if right['type'] == column or right['type'] == NUMBER:
                self.variables[right['val']] = left['val']
            else:
                Exception('Error. Left Right not good')
    def visit_less(self,left,right):
        if left['type'] == column:
            if right['type'] == NUMBER:
                self.variables[left['val']+'<'] = right['val']
            else:
                Exception('Error. condition not good')
        elif left['type'] == NUMBER:
            if right['type'] == column:
                self.variables[right['val']+'>'] = left['val']

class Query:
    def __init__(self,commands):
        #self.com = commands
        #self.fList = []
        
        self.current_dir = ''
        
    def query(self,commands,kernel):
        self.com = commands
        self.fList = []
        if 'bash' not in commands and 'column' in commands:
            print("SELECT STATEMENT!!")
            print("What commands is: ",commands)
            print("What column is: ",commands['column'].strip())

            self.columnList = self.getColumn(commands['column'].strip())
        
            print("Column list:",self.columnList)
            if len(self.com) > 1:
            
                finalList = self.filterColumn(commands,self.columnList)
                print("the final list:",finalList)
                self.fList = finalList
            else:
                print("the final list w/o condition:",self.columnList)
                self.fList = self.columnList
        elif 'bash' in commands:
            print("What the commands are: ",commands)
            print("What the ls is:",commands['bash'])
            #print(subprocess.run(commands['bash']))
            # Get the absolute path of the current directory
            #current_dir = subprocess.check_output("pwd", shell=True, text=True).strip()
            #current_dir = ''
            if commands['bash']=='ls':
                self.fList = kernel.get_file_system().list_contents()
            if commands['bash']=='cd' and 'column' in commands:
                print("Preforming cd")
                kernel.get_file_system().change_directory(commands['column'].strip())
            if commands['bash']=='cd' and 'column' not in commands:
                print("Preforming cd")
                kernel.get_file_system().switch_to_user_home(kernel.get_current_user())
            if commands['bash']=='rm' and 'column' in commands:
                print("Preforming rm")
                kernel.get_file_system().delete_file(commands['column'].strip())
            if commands['bash']=='mkdir' and 'column' in commands:
                print("Preforming mkdir")
                kernel.get_file_system().create_directory(commands['column'].strip())
            if commands['bash']=='cat' and 'column' in commands:
                print("Preforming cat")
                self.fList.append(kernel.get_file_system().open_file(commands['column'].strip()))
            if commands['bash']=='useradd' and 'column' in commands:
                print("Preforming useradd")
                kernel.add_user(commands['column'].strip(),'123')
            if commands['bash']==USERMOD and 'column' in commands:
                print(f"Preforming {USERMOD}")
                kernel.trigger_username_change(commands['column'].strip())
            if commands['bash']=='su' and 'column' in commands:
                print("Preforming su")
                kernel.trigger_login(commands['column'].strip())

            if commands['bash']=='passwd' and 'column' in commands:
                print("Preforming passwd")
                kernel.trigger_password_reset(commands['column'].strip())
            if commands['bash']=='pwd':
                print("Preforming pwd")
                self.fList.append(kernel.get_file_system().get_current_directory().name)

            if commands['bash']=='run' and 'column' in commands:
                print("Preforming run")
                try:
                    if commands['column'].strip() == 'notVim':
                        kernel.run_application(commands['column'].strip(),file_system=kernel.get_file_system())
                    if commands['column'].strip() in ('view','View'):
                        kernel.run_application(commands['column'].strip(),kern=kernel)
                    elif commands['column'].strip() in kernel.get_apps_name():
                        self.fList.append(kernel.run_application(commands['column'].strip(),commands['column'].strip(),kernel))
                    else:
                        kernel.run_application(commands['column'].strip())
                    
                except Exception as e:
                    print(f"Error with application: {e}")
                    traceback.print_exc()


    def getFlist(self):
        return self.fList


    def getColumn(self, columnName):
        columnList = []
        with open('view/test.csv',newline='') as c:
            r = csv.reader(c,delimiter=',')
            for row in r:
                if len(row) >= 3:
                    if 'TITLE' in columnName.upper():
                        columnList.append(row[0])
                    if 'PAGEID' in columnName.upper():
                        columnList.append(row[1])
                    if 'SNIPPET' in columnName.upper():
                        columnList.append(row[2])
        return columnList
    
    
    def filterColumn(self, filters,columnList):
        filterColumns = []
        for colName in filters:
            if colName != 'column' and str(filters[colName])[-1] in ('<','>'):
                print("Doing compare")
            elif colName != 'column':
                columns = self.getColumn(colName.strip())
                for row in columns:
                    print("The filter", filters[colName])
                    if str(filters[colName]).strip().upper() in str(row).upper():
                        filterColumns.append(row)
        return self.intersection(filterColumns,columnList)
    def intersection(self,s1,s2):
        finalList = []
        print("s1: ",s1)
        print("s2: ",s2)
        with open('view/test.csv',newline='') as c:
            r = csv.reader(c,delimiter=',')
            for row in r:
                for a in s1:
                    for b in s2:
                        #print(a,b,row)
                        if len(row) >= 3:
                            if a.upper() in (row[0].join((row[2],row[1]))).upper() and b.upper() in (row[0].join((row[2],row[1])).upper()):
                                finalList.append(b)
        return finalList

        

        

    

     
class dbEngine:
    def __init__(self,kernel):
        self.kernel=kernel
        self.tokens = []
        self.scanner = None
        self.parser = None
        self.q = Query(None)
        #self.scanner = None

    def scan(self,string):
        self.scanner = Scanner(string)
    def parse(self):
        self.parser = Parser(self.scanner)
        #ast = self.parser.parse()
        interpreter = Interpreter(self.parser)
        #print("the interpreter: ",interpreter)
        result = interpreter.interpret()
        print("The interpreter: ",result)
        
        #self.q = Query(result)
        self.q.query(result,self.kernel)

    def getFlist(self):
        return self.q.getFlist() if self.q is not None else [""]
        #while True:
        #self.token = scanner.get_next_token()
        #self.tokens.append(self.token)
        #if self.token.t == EOF:
        #break
            
        #print(self.tokens)


#d = dbEngine("HI")

#d.scan("select PAGEID where TITLE=MIKE MYERS")

#d.scan(sys.argv)
#d.parse()


