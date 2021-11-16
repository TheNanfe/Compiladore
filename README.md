# Compiladores
Integrante: Hernan Lopez 

Para que el traductor json-->xml funcione, primero hay que crear un archivo fuente.txt en la carpeta con el lexer. El lexer traducira todos los caracteres pasados y generara
un archivo output.txt. El analizador sintactico luego leera ese archivo output.txt creado por el lexer.py.
En caso de algun error lexico o sintactico, la consola imprimira dicho error y la escritura del archivo parara.
El archivo xml se generara en la carpeta donde se encuentra el traductor.py

Para correr el codigo se necesita: 
-Python 3.x
-libreria re y os de Python (que deberian de venir con el paquete default descargado)
-un archivo plano .txt con codigo JSON

