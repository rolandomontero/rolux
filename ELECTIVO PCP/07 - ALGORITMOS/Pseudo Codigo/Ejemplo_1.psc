Algoritmo Ejemplo_1
	
	// Se usa "//" para escribir un comentario.
	
	// Autor: Nombre del Programador
	// Fecha: 21 - julio - 2022
	// Descripción:
	// Escribe una descripción del algoritmo.
	// ///////////////////////////////////////////
	
	// Definir variables, existe dos formas de definir variables.
	numero_entero Es Entero
	Definir numero_real Como Real
	Definir resultado Como Real
	
	Definir frase Como Caracter
	parrafos Es Caracter
	
	// Asignar valor a una variable
	
	numero_entero <- 12 
	// o también se puede definir 
	numero_real = 2.315
	
	frase = "Hola! esta es una frase"
	parrafos = "Esto es un ejemplo de párrafo"
	
	// Para escribir un mensaje en pantalla y también una variable
	Escribir "Esta frase se debe colocar entre comillas"
	Escribir "Esta es el valor de la variable numero_entero =", numero_entero
	
	
	// Para pedir al usuario un valor
	Escribir "Ingresa un número entero"
	Leer numero_entero
	
	Escribir "Ingresa un número real"
	Leer numero_real
	
	Escribir "Ingresa una frase"
	Leer frase
	
	//  Realizar una operación
	resultado = numero_entero * numero_real
	
	Escribir  "El producto entre el numero_entero x numero_real =", resultado, " y tu frase es =", frase
	
	
	
FinAlgoritmo
