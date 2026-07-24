Algoritmo ejercicio_5
	Definir num Como Entero
	Definir producto Como Entero
	producto <- 1
	num <- 1
	Escribir 'ingrese un numero'
	Leer num
	Si num=0 Entonces
		producto <- 0
	FinSi
	Mientras num<>0 Hacer
		producto <- producto*num
		Escribir 'ingrese otro numero'
		Leer num
	FinMientras
	Si producto<>0 Entonces
		Escribir 'El resultado es = ',producto
	SiNo
		Escribir 'No se ingresaron numeros validos'
	FinSi
FinAlgoritmo

