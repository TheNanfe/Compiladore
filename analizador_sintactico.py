from lexer.lexer import Lexer
import re

class SyntaxError(Exception):
	pass

class SyntaxCheck():
	def __init__(self, fuente):
		self.fuente = fuente
		self.input_file = None
		self.tokens = None
		self.absolute_position = 0

	def crear_sin_espacios(self):
		self.input_file = open('input.txt', 'w')
		for x in self.fuente.readlines():
			self.input_file.write(re.sub(r"[\t\n]*", "", x))

	def next_position(self, increment):
		print(self.tokens[self.absolute_position])
		self.absolute_position = self.absolute_position + increment
		

	def tokens_array(self):
		self.input_file = open('input.txt', 'r')
		#print(self.input_file.read())
		self.tokens = self.input_file.read().split()

	def llaves(self):
		if not self.tokens[self.absolute_position] == 'l_llave': return False
		self.next_position(1)
		print(self.cuerpo(), self.absolute_position)
		print(self.absolute_position)
		if not self.tokens[self.absolute_position] == 'r_llave': raise SyntaxError
		self.next_position(1)
		return True

	def corchetes(self):
		if not self.tokens[self.absolute_position] == 'l_corchete': return False
		self.next_position(1)
		self.llaves()
		self.corchetes()
		self.cuerpo()
		if not self.tokens[self.absolute_position] == 'r_corchete': return False
		self.next_position(1)
		return True
	
	def value(self):
		if self.corchetes(): return True
		if self.llaves(): return True
		if self.tokens[self.absolute_position] == 'number': 
			self.next_position(1)
			return True
		if self.tokens[self.absolute_position] == 'string': 
			self.next_position(1)
			return True
		if self.tokens[self.absolute_position] == 'pr_false': 
			self.next_position(1)
			return True
		if self.tokens[self.absolute_position] == 'pr_true': 
			self.next_position(1)
			return True
		return False

	def cuerpo (self):
		if not self.tokens[self.absolute_position] == 'string': return False
		if not self.tokens[self.absolute_position + 1] == 'dos_puntos': raise SyntaxError
		self.next_position(2)
		if not self.value(): raise SyntaxError
		print('acaaaaaa', self.tokens[self.absolute_position])
		if self.tokens[self.absolute_position] == 'coma':
			self.next_position(1)
			self.cuerpo()
		return True
		

	def get_sintax_cheked(self):
		self.crear_sin_espacios()
		self.tokens_array()
		self.llaves()




if __name__ == '__main__':
	lexer = Lexer()
	output = open('lexer/output.txt', 'r')
	syntax = SyntaxCheck(output)
	syntax.get_sintax_cheked()