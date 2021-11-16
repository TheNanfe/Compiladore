from analizador_sintactico import SyntaxCheck
from lexer.lexer import Lexer

class Traductor():
	def __init__ (self, input_file, traductor_output):
		self.input_file = input_file
		self.tokens = None
		self.absolute_position = 0
		self.token = None
		self.tabs_numbers = 0
		self.item = []
		self.traductor_output = traductor_output
		#self.first_time = 1

	def tokens_array(self):
		self.input_file = open('lexer/input.txt', 'r')
		self.tokens = self.input_file.read()
		#self.tokens = self.tokens[1:-1]
		self.input_file.close()

	def next_token(self, increment):
		self.absolute_position = self.absolute_position + increment
		self.token = self.tokens[self.absolute_position]

	def increase_tabs(self, increment):
		self.tabs_numbers = self.tabs_numbers + increment

	def split_string(self):
		strings = "".join(self.item)
		strings = (strings.split(sep=":"))
		return strings



	def get_string(self,tags):
		if tags[0] == []:
			tags[0] = tags[1]
			tags[1] = tags[2]
		try:

			if tags[0][0] == ',':
				tags[0] = tags[0][1:]
			if tags[0][0] == '"':
				tags[0] = tags[0][1:-1]
			if tags[0][0] == '"':
				tags[0] = tags[0][1:-1]
			if len(tags) > 2:	
				tags.pop(0)
		except:
			return

		string = ['\t'*self.tabs_numbers,'<',tags[0],'>',tags[1],'</',tags[0],'>']
		self.traductor_output.write(''.join(string))
		self.traductor_output.write('\n')
		print('\t'*self.tabs_numbers,'<',tags[0],'>',tags[1],'</',tags[0],'>')



	def llave(self):
		self.token = self.tokens[self.absolute_position]
		if not Lexer.l_llave(self.token): return False
		corchete_position = 0;
		llave_position = 0
		tag_value = None

		while True:
			if self.token == '{':
				self.next_token(1)
				print("\t"*self.tabs_numbers, "<llave>")
				string = ["\t"*self.tabs_numbers, "<item>"]
				self.traductor_output.write(''.join(string))
				self.traductor_output.write('\n')

				self.increase_tabs(1)

			if self.token == "[":
				self.corchete()

			if self.token == '}':
				#print(self.token, llave_position)
				if corchete_position != 0:
					self.increase_tabs(-1)
					string = ["\t"*self.tabs_numbers, "</",tag_value,">"]
					self.traductor_output.write(''.join(string))
					self.traductor_output.write('\n')
					print("\t"*self.tabs_numbers, "</",tag_value,">")
					break
				else:
					self.increase_tabs(-1)
					#print(self.tokens[self.absolute_position-1], 'tokens array')
					string = ["\t"*self.tabs_numbers, "</item>"]
					self.traductor_output.write(''.join(string))
					self.traductor_output.write('\n')
					print("\t"*self.tabs_numbers, "</llave>")
					break
				
			if self.token == ":":
				if self.tokens[self.absolute_position+1] == '{' or self.tokens[self.absolute_position+1] == '[':
					tag_value = self.split_string()[0]
					if tag_value[0] == ',':
						tag_value = tag_value[1:]
					if tag_value[0] == '"':
						tag_value = tag_value[1:-1]
					string = ["\t"*self.tabs_numbers, "<",tag_value,">"]
					self.traductor_output.write(''.join(string))
					self.traductor_output.write('\n')
					print("\t"*self.tabs_numbers, "<",tag_value,">")
					self.item.clear()

					if self.tokens[self.absolute_position+1] == '{':
						llave_position = self.tabs_numbers
					elif self.tokens[self.absolute_position+1] == '[':
						corchete_position = self.tabs_numbers
					self.increase_tabs(1)


			if self.token == ",":
				self.get_string(self.split_string())
				self.item.clear()


			self.item.append(self.token)
			self.next_token(1)
			
	def corchete(self):
		self.token = self.tokens[self.absolute_position]
		if not Lexer.l_corchete(self.token): return False
		corchete_position = 0;
		llave_position = 0
		tag_value = None

		while True:

			if self.token == '[': 	
				self.next_token(1)
				string = ["\t"*self.tabs_numbers, "<item>"]
				self.traductor_output.write(''.join(string))
				self.traductor_output.write('\n')
				print("\t"*self.tabs_numbers, "<corchete>")	
				self.corchete()
				self.increase_tabs(1)

			if self.token == "{":
				self.llave()

			if self.token == ']':
				if corchete_position != 0:
					self.increase_tabs(-1)
					string = ["\t"*self.tabs_numbers, "</",tag_value,">"]
					self.traductor_output.write(''.join(string))
					self.traductor_output.write('\n')
					print("\t"*self.tabs_numbers, "</",tag_value,">")
					break
				else:
					self.increase_tabs(-1)
					string = ["\t"*self.tabs_numbers, "</item>"]
					self.traductor_output.write(''.join(string))
					self.traductor_output.write('\n')
					print("\t"*self.tabs_numbers, "</corchete>")
					break

			if self.token == ":":
				if self.tokens[self.absolute_position+1] == '{' or self.tokens[self.absolute_position+1] == '[':
					tag_value = self.split_string()[0]
					if tag_value[0] == ',':
						tag_value = tag_value[1:]
					if tag_value[0] == '"':
						tag_value = tag_value[1:-1]
					string = ["\t"*self.tabs_numbers, "<",tag_value,">"]
					self.traductor_output.write(''.join(string))
					self.traductor_output.write('\n')
					print("\t"*self.tabs_numbers, "<",tag_value,">")

					if self.tokens[self.absolute_position+1] == '{':
						llave_position = self.tabs_numbers
					elif self.tokens[self.absolute_position+1] == '[':
						corchete_position = self.tabs_numbers
					self.increase_tabs(1)

			if self.token == ",":
				self.item.clear()


			self.item.append(self.token)
			self.next_token(1)
			

	def translating(self):
		self.tokens_array()
		self.llave()
	

if __name__ == '__main__':
	try:
		lexer = Lexer().get_tokens()
	except:
		print("Ha ocurrido un error lexico")

	lexer_output = open('lexer/output.txt', 'r')
	try:
		var = SyntaxCheck(lexer_output)
		var.get_sintax_cheked()
	except Exception as e:
		print("//////////////////////   Analizador Sintactico   //////////////////////////////////////")
		print(".\nSe ha encontrado un error sintatico.\n.")
		print("//////////////////////////////////////////////////////////////////////////////////////")
		raise

	traductor_output = open('traductor_output.xml', 'w')
	translate_to_xml = Traductor(open('lexer/input.txt', 'r'), traductor_output)
	translate_to_xml.tokens_array()
	translate_to_xml.translating()
	traductor_output.close()
	with open('traductor_output.xml', 'r+') as fp:
		lines = fp.readlines()
		fp.seek(0)
		fp.truncate()
		fp.writelines(lines[1:])


	print("::::::::::::::::::::::::::::::::::::  Analizador Sintactico  ::::::::::::::::::::::::::::::::")
	print(".\nSe ha generado el archivo .xml.\n.")
	print("::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
