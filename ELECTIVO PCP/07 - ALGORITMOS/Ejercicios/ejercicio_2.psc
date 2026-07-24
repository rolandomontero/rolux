Algoritmo ejercicio_2
	r <- 0
	i <- 0
	Escribir 'ingresa un valor'
	Leer n
	Mientras n<>1500 Hacer
		Si n>0 Entonces
			i <- i+1
			r <- r+i
			Escribir n
		Sino
			Escribir n
		FinSi
		Escribir 'ingrese un valor'
		Leer n
	FinMientras
	x <- r/i
	Escribir 'La salida es: ',x
FinAlgoritmo

