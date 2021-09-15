import re

class Lexer():
	def __init__(self):
		pass

	@classmethod
	def cadena(self, partial_string):
		count = 0
		total_count = 0
		for caracter in partial_string:
			print(caracter)
			total_count = total_count + 1
			if caracter == "'" or caracter == '"':
				count = count + 1
				if count == 2:
					return [total_count-1, "string "]
			elif self.symbol_finder(caracter) and count == 1:
				raise ValueError('A very specific bad thing happened.')
		return False

	@classmethod
	def numero(self, partial_string):
		total_count = 0
		for caracter in partial_string:
			try:
				#print(caracter)
				int(caracter)
				total_count = total_count + 1
			except Exception as e:
				if total_count!=0:
					return [total_count-1, "number "]

		if total_count!=0:
					return [total_count-1, "number "]


		return False

	def l_llave(caracter):
		if caracter == '{':
			return "l_llave "
		return False

	def r_llave(caracter):
		if caracter == '}':
			return "r_llave "
		return False

	def l_corchete(caracter):
		if caracter == '[':
			return "l_corchete "
		return False

	def r_corchete(caracter):
		if caracter == ']':
			return "r_corchete "
		return False

	def dos_puntos(caracter):
		if caracter == ':':
			return "dos_puntos "
		return False

	def coma(caracter):
		if caracter == ',':
			return "coma "
		return False

	@classmethod
	def symbol_finder(self, caracter):
		symbol_array = [self.l_llave, self.r_llave, self.l_corchete, self.r_corchete, 
		self.dos_puntos, self.coma]
		for symbol in symbol_array:
			symbol_return = symbol(caracter)
			if symbol_return:
				return symbol_return


		return False

	@classmethod
	def token_finder(self, caracter, whole_string, index):
		symbol = self.symbol_finder(caracter)
		if symbol:
			return [0, symbol]


		if caracter == "'" or caracter == '"':
			cadena = self.cadena(whole_string[index:])
			if cadena:
				print(cadena)
				return cadena


		if caracter.lower() == "f":
			if (whole_string[index:index+5]).lower() == "false":
				return [4,"pr_false "]
		elif caracter.lower() == "t":
			if (whole_string[index:index+4]).lower() == "true":
				return [3,"pr_true "]
		elif caracter.lower() == "n":
			if (whole_string[index:index+4]).lower() == "null":
				return [3,"pr_null "]

		else:
			numero = self.numero(whole_string[index:])
			if numero:
				return numero

		return False


	
a = Lexer
fuente = open('fuente.txt', 'r')
input_file = open("sin_espacios.txt", 'w')

for x in fuente.readlines():
	input_file.write(re.sub(r"[\t\n\s]*", "", x))
input_file.close()



input_file = open("sin_espacios.txt", 'r')
output_file = open('output.txt', 'w')
for whole_line in input_file.readlines():
	#print(whole_line)
	skip_characters = 0
	for index, caracter in enumerate(whole_line):

		if skip_characters == 0:
			print(caracter, index)
			values = a.token_finder(caracter, whole_line, index)
			output_file.write(values[1])
			if caracter == '{' or caracter == ',' or caracter == '[' or caracter == '}'	or caracter == ']':
				output_file.write('\n')
			skip_characters = values[0]
		else:
			skip_characters = skip_characters - 1



#def cadena(literal):

