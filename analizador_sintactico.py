from lexer.lexer import Lexer
import re
import os
#############################################################################################################################
#                                        Pasos a Seguir. !IMPORTANTE!
# 1- El lexer debe recibir un fuente.txt
# 2- El lexer genera un archivo output.txt
# 3-  Este analizador sintactico recibe ese output.txt generado por el lexer y lo convierte en INPUT
#############################################################################################################################

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

	def next_token(self, increment):
		self.absolute_position = self.absolute_position + increment
		
	def tokens_array(self):
		self.input_file = open('input.txt', 'r')
		self.tokens = self.input_file.read().split()
		self.input_file.close()

	def llaves(self):
		if not self.tokens[self.absolute_position] == 'l_llave': return False
		self.next_token(1)
		self.cuerpo()
		while self.tokens[self.absolute_position] == 'coma': 
			self.next_token(1)
			self.value()
			if self.tokens[self.absolute_position] == 'r_corchete': break
		if not self.tokens[self.absolute_position] == 'r_llave': raise SyntaxError
		self.next_token(1)
		return True

	def corchetes(self):
		if not self.tokens[self.absolute_position] == 'l_corchete': return False
		self.next_token(1)
		self.llaves()
		self.corchetes()
		self.cuerpo()
		while self.tokens[self.absolute_position] != 'l_corchete' and self.tokens[self.absolute_position] != 'dos_puntos' : 
			if self.tokens[self.absolute_position] == 'coma':
				self.next_token(1)
			self.value()
			if self.tokens[self.absolute_position] == 'r_corchete': break
		if not self.tokens[self.absolute_position] == 'r_corchete': raise SyntaxError
		self.next_token(1)
		return True
	
	def value(self):
		if self.corchetes(): return True
		if self.llaves(): return True
		if self.tokens[self.absolute_position] == 'number': 
			self.next_token(1)
			return True
		if self.tokens[self.absolute_position] == 'string': 
			self.next_token(1)
			return True
		if self.tokens[self.absolute_position] == 'pr_false': 
			self.next_token(1)
			return True
		if self.tokens[self.absolute_position] == 'pr_true': 
			self.next_token(1)
			return True
		if self.tokens[self.absolute_position] == 'pr_null': 
			self.next_token(1)
			return True
		if self.tokens[self.absolute_position] == 'coma': 
			return True
		return False

	def cuerpo (self):
		if not self.tokens[self.absolute_position] == 'string': return False
		if not (self.tokens[self.absolute_position + 1] == 'dos_puntos' or  self.tokens[self.absolute_position + 1] == 'coma'): raise SyntaxError
		self.next_token(2)
		if not self.value(): raise SyntaxError
		if self.tokens[self.absolute_position] == 'coma':
			self.next_token(1)
			if not self.cuerpo() and not self.value(): raise SyntaxError
		return True
		
	def get_sintax_cheked(self):
		self.crear_sin_espacios()
		self.tokens_array()
		if not self.llaves(): 
			print("//////////////////////   Analizador Sintactico   //////////////////////////////////////")
			print(".\nExiste algun caracter que no pertenece al diccionario.\n.")
			print("//////////////////////////////////////////////////////////////////////////////////////")
		else:
			print("//////////////////////   Analizador Sintactico   //////////////////////////////////////")
			print(".\nSe ha realizado el analisis sintactico y no se han encontrado errores de sintaxis.\n.")
			print("//////////////////////////////////////////////////////////////////////////////////////")




if __name__ == '__main__':

	lexer = Lexer()
	lexer.get_tokens()
	#os.remove('lexer/input.txt')
	output = open('lexer/output.txt', 'r')
	syntax = SyntaxCheck(output)
	syntax.get_sintax_cheked()
	#os.remove('input.txt')