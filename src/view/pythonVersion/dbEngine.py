# To be the database engine for the query of data
import csv
import sys
# Define token types
NUMBER, select, where, AND, OR, column, RPAREN, EOF, equal, lessThan, greaterThan = (
    'NUMBER', 'select', 'where', 'AND', 'OR', 'column', 'RPAREN', 'EOF','=','LESS','GREAT'
)

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
		while self.current_char is not None and self.current_char.isspace():
			self.advance()

	def number(self):
		result = ''
		while self.current_char is not None and self.current_char.isdigit() and not self.current_char.isspace():
			result += self.current_char
			self.advance()
		return Token(NUMBER,int(result))

	def column(self):
		result = ''
		while self.current_char is not None and self.current_char.isalnum() or self.current_char == "_":
			result += self.current_char
			self.advance()
		return Token(column,result)
	def get_next_token(self):
		while self.current_char is not None:
			if self.current_char.isspace():
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
			if self.current_char == 'OR':
				self.advance()
				return Token(OR,'OR')
			if self.current_char.isalpha() or self.current_char == '_':
				print("The selec:",self.current_char.isalpha())	
				if self.pos+len('select') < len(self.text) and self.text[self.pos:self.pos+len('select')]=='select':
					self.advance('select')
					return Token(select,'select')

				#if self.current_char == 'where':
				elif self.pos+len('where') < len(self.text) and self.text[self.pos:self.pos+len('where')] == 'where':
					self.advance('where')
					return Token(where,'where')
				
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
	def expression (self):
		node = self.term()
		while self.current_token.t in (equal,lessThan,greaterThan,AND,OR):
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
		else:
			self.error()
		return a
	def parse(self):
		return self.select()
		
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
		if ast is not None and ast['where'] is not None:
			self.visit_Expr(ast['where'])
		if ast['type'] == column:
			self.variables['column'] = ast['val']
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
		self.com = commands
		self.columnList = self.getColumn(commands['column'].strip())
		print("Column list:",self.columnList)
		if len(self.com) > 1:
			
			finalList = self.filterColumn(commands,self.columnList)
			print("the final list:",finalList)
		else:
			print("the final list w/o condition:",self.columnList)
	def getColumn(self, columnName):
		columnList = []
		with open('test.csv',newline='') as c:
			r = csv.reader(c,delimiter=',')
			for row in r:
				if columnName.upper() == 'TITLE':
					columnList.append(row[0])
				if columnName.upper() == 'PAGEID':
					columnList.append(row[1])
				if columnName.upper() == 'SNIPPET':
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
		with open('test.csv',newline='') as c:
			r = csv.reader(c,delimiter=',')
			for row in r:
				for a in s1:
					for b in s2:
						#print(a,b,row)
						if a.upper() in (row[0].join((row[2],row[1]))).upper() and b.upper() in (row[0].join((row[2],row[1])).upper()):
							finalList.append(b)
		return finalList

		

		

	

		
class dbEngine:
	def __init__(self,obj):
		self.obj=obj
		self.tokens = []
		self.scanner = None
		self.parser = None
	def scan(self,string):
		self.scanner = Scanner(string)
	def parse(self):
		self.parser = Parser(self.scanner)
		#ast = self.parser.parse()
		interpreter = Interpreter(self.parser)
		#print("the interpreter: ",interpreter)
		result = interpreter.interpret()
		print("The interpreter: ",result)
		q = Query(result)
		
		#while True:
		#self.token = scanner.get_next_token()
		#self.tokens.append(self.token)
		#if self.token.t == EOF:
		#break
			
		#print(self.tokens)


d = dbEngine("HI")

d.scan("select PAGEID where TITLE=MIKE MYERS")

#d.scan(sys.argv)
d.parse()


