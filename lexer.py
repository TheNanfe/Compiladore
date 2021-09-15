import re #libreria utilizada para crear un arhivos sin espacios, tabs ni saltos de linea

class Lexer():
	def __init__(self):
		pass
	
	#todos los metodos de la clase

	@classmethod
	def cadena(self, partial_string):
		count = 0
		total_count = 0
		for caracter in partial_string:
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
				int(caracter)
				total_count = total_count + 1
			except Exception as e:
				if total_count!=0:
					return [total_count-1, "number "]
				else:
					return False

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

	#encuentra el simbolo
	@classmethod
	def symbol_finder(self, caracter):
		symbol_array = [self.l_llave, self.r_llave, self.l_corchete, self.r_corchete, 
		self.dos_puntos, self.coma]
		for symbol in symbol_array:
			symbol_return = symbol(caracter)
			if symbol_return:
				return symbol_return


		return False

	#se define que tipo de token es
	@classmethod
	def token_finder(self, caracter, whole_string, index):
		symbol = self.symbol_finder(caracter)
		if symbol:
			return [0, symbol]


		if caracter == "'" or caracter == '"':
			cadena = self.cadena(whole_string[index:])
			if cadena:
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


#se crea el objeto 	
lexer = Lexer

#se crea un archivo intermedio de texto, el cual no contien espacios, tabs ni saltos de linea
fuente = open('fuente.txt', 'r')
input_file = open("sin_espacios.txt", 'w')
for x in fuente.readlines():
	input_file.write(re.sub(r"[\t\n\s]*", "", x))
input_file.close()


#se procede a leer el archivo sin espacios y a escribir en el output.txt
input_file = open("sin_espacios.txt", 'r')
output_file = open('output.txt', 'w')
for whole_line in input_file.readlines():
	skip_characters = 0
	#en caso de que exista algun caracter que no exista en el diccionario, se cancela la escritura del archivo.
	try:
		for index, caracter in enumerate(whole_line):
		#cuando son cadenas o caracteres, false, null o true, tienen una lectura especial 
		#necesitan ser saltados una x cantidad de caracteres.
		
			if skip_characters == 0:
				values = lexer.token_finder(caracter, whole_line, index)
				output_file.write(values[1])

				if caracter != ":" and lexer.symbol_finder(caracter):
					output_file.write('\n')
				skip_characters = values[0]

			else:
				skip_characters = skip_characters - 1
	except Exception as e:
			print("---------------------------------------------------------------------")
			print(".\n.\nSe ha detectado algo que no pertenece al diccionario.\n.\n.")
			print("La del escritura del output ha parado")
			print("---------------------------------------------------------------------")
			input_file.close()
			output_file.close()
			break
input_file.close()
output_file.close()
print("Se ha generado el OUTPUT.TXT en la misma carpeta contenedora de este script.\nPor favor verificar dicho archivo")

