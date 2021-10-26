# Compiladores
Integrante: Hernan Lopez 

Para que el analaizador sintactico funcione, primero hay que crear un archivo fuente.txt en la carpeta con el lexer. El lexer traducira todos los caracteres pasados y generara
un archivo output.txt. El analizador sintactico luego leera ese archivo output.txt creado por el lexer.py

Para correr el codigo se necesita: 
-Python 3.x
-libreria re y os de Python (que deberian de venir con el paquete default descargado)
-un archivo plano .txt con codigo JSON
-Se generara un archivo de texto extra (sin_espacios.txt) cuyo unico proposito es eliminar todo espacio existente en el archivo fuente orignal. !NO ES EL OUTPUT FINAL!
