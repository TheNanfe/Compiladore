from analizador_sintactico import SyntaxCheck
from lexer.lexer import Lexer

class Translate():
	def __init__ (self, input_file, lexer_output_path, traductor_output=None):
		self.input_file = input_file
		self.lexer_output_path = lexer_output_path
		self.lexer_output = None
		self.tokens = None
		self.lexer_token = None
		self.absolute_position = 0
		self.token = None
		self.tabs_numbers = 0
		self.item = []
		self.traductor_output = traductor_output
		self.separated_simbols = []
		self.lexer_simbols = []
	
	def lexer_tokens_array(self):
		self.lexer_output = open(lexer_output_path, 'r')
		self.lexer_simbols = self.lexer_output.read().split()
		self.lexer_output.close()

	def tokens_array(self):
		self.input_file = open('lexer/input.txt', 'r')
		self.tokens = self.input_file.read()
		self.input_file.close()

	def next_token(self, increment):
		self.absolute_position = self.absolute_position + increment
		self.token = self.tokens[self.absolute_position]
		
	def tranlsate_next_token(self, increment):
		self.absolute_position = self.absolute_position + increment
		self.token = self.separated_simbols[self.absolute_position]
		self.lexer_token = self.lexer_simbols[self.absolute_position]
	
	def increase_tabs(self, increment):
		self.tabs_numbers = self.tabs_numbers + increment


	def write_file(self, item):
		if isinstance(item, list):
			item = ''.join(item)
		string = ["\t"*self.tabs_numbers, item]
		self.traductor_output.write(''.join(string))
		self.traductor_output.write('\n')


	def separating_simbols(self):
		self.lexer_tokens_array()
		flag = 0
		self.tokens_array()
		self.token = self.tokens[self.absolute_position]
		while self.absolute_position < len(self.tokens)-1:
			if self.token == '{':
				self.separated_simbols.append('{')
			if self.token == '}':
				self.separated_simbols.append('}')
			if self.token == '[':
				self.separated_simbols.append('[')
			if self.token == ']':
				self.separated_simbols.append(']')
			if self.token == ',':
				self.separated_simbols.append(',')
			if self.token == ':':
				self.separated_simbols.append(':')
			if self.token == '"':
				inner_simbols = []
				while True:
					self.next_token(1)
					#self.separated_simbols.append(self.token)
					if self.token == '"':
						string = ''.join(inner_simbols)
						inner_simbols = []
						self.separated_simbols.append(string)
						break
					else:
						inner_simbols.append(self.token)
			if self.token.isdigit():
				flag = 1
				inner_simbols = []
				while True:
					if self.token.isdigit():
						inner_simbols.append(self.token)
						self.next_token(1)
					else:
						numbers = ''.join(inner_simbols)
						self.separated_simbols.append(numbers)
						break
			if self.token == 't':
				self.separated_simbols.append('true')
			elif self.token == 'f':
				self.separated_simbols.append('false')
			elif self.token == 'n':
				self.separated_simbols.append('null')

			if flag == 0:
				self.next_token(1)
			else:
				flag = 0
		self.separated_simbols.append('}')

	def translating(self):
		bandera_primer_caracter = 0
		bandera_cierre_llave =  0
		bandera_cierre_corchete = 0
		self.separating_simbols()
		self.absolute_position = 0
		while self.absolute_position != len(self.separated_simbols)-1:
			
			if self.lexer_token == 'l_llave':
				string = "<item>"
				self.write_file(string)
				self.increase_tabs(1)

			if self.lexer_token == 'l_corchete':
				string = "<item>"
				self.write_file(string)
				self.increase_tabs(1)

			if self.lexer_token == 'r_llave':
				if bandera_cierre_llave == 1:
					self.increase_tabs(-1)
					self.write_file(token_cierre)
					bandera_cierre_llave = 0
				else:
					self.increase_tabs(-1)
					string = "</item>"
					self.write_file(string)

			if self.lexer_token == 'r_corchete':
				if bandera_cierre_corchete == 1:
					self.increase_tabs(-1)
					self.write_file(token_cierre)
					bandera_cierre_corchete = 0
				else:	
					self.increase_tabs(-1)
					string = "</item>"
					self.write_file(string)

			if self.lexer_token == 'string':
				self.tranlsate_next_token(1)
				if self.lexer_token == 'dos_puntos':
					self.tranlsate_next_token(1)
					if self.lexer_token == 'string':
						tag = self.separated_simbols[self.absolute_position-2]
						string = ['<',tag,'>','"',self.token,'"','</',tag,'>']
						self.write_file(string)
					
					if self.lexer_token == 'number':
						tag = self.separated_simbols[self.absolute_position-2]
						string = ['<',tag,'>',self.token,'</',tag,'>']
						self.write_file(string)

					if self.lexer_token == 'pr_true' or self.lexer_token == 'pr_false' or self.lexer_token == 'null':
						tag = self.separated_simbols[self.absolute_position-2]
						string = ['<',tag,'>',self.token,'</',tag,'>']
						self.write_file(string)

					if self.lexer_token == 'l_llave':
						tag = self.separated_simbols[self.absolute_position-2]
						string = ["<",tag,">"]
						self.write_file(string)
						self.increase_tabs(1)
						bandera_cierre_llave = 1
						string.insert(1, '/')
						token_cierre = string
						if bandera_primer_caracter == 0:
							primer_caracter = token_cierre
							bandera_primer_caracter = 1
					
					if self.lexer_token == 'l_corchete':
						tag = self.separated_simbols[self.absolute_position-2]
						string = ["<",tag,">"]
						self.write_file(string)
						self.increase_tabs(1)
						bandera_cierre_corchete = 1
						string.insert(1, '/')
						token_cierre = string
						if bandera_primer_caracter == 0:
							primer_caracter = token_cierre
							bandera_primer_caracter = 1
			self.tranlsate_next_token(1)
			if self.absolute_position == len(self.separated_simbols)-1:
				self.increase_tabs(-1)
				self.write_file(primer_caracter)

		
	


if __name__ == '__main__':
	try:
		lexer = Lexer().get_tokens()
	except:
		print("#####################################   Analizado Lexico  ####################################")
		print(".\nSe ha producido un error lexico.\n.")
		print("##########################################################################################\n")
		raise

	lexer_output = open('lexer/output.txt', 'r')
	try:
		var = SyntaxCheck(lexer_output)
		var.get_sintax_cheked()
	except Exception as e:
		print("//////////////////////   Analizador Sintactico   //////////////////////////////////////")
		print(".\nSe ha encontrado un error sintatico.\n.")
		print("//////////////////////////////////////////////////////////////////////////////////////\n")
		raise



	traductor_output = open('traductor_output.xml', 'w')
	input = open('lexer/input.txt', 'r')
	lexer_output_path = 'input.txt'
	translate = Translate(input, lexer_output_path, traductor_output)
	translate.translating()
	input.close()


	print(":::::::::::::::::::::::::::::::::::::::::  Traductor  ::::::::::::::::::::::::::::::::::::::")
	print(".\nSe ha generado un archivo .xml en esta misma carpeta.\n.")
	print(":::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::\n")


