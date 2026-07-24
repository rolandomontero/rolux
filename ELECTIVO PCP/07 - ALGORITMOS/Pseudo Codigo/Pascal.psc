// Función Factorial
Funcion f <- factorial ( n )
	f<-1
	si n=0 Entonces
		n<-1
	FinSi
	
	para i<-n hasta 1 Con Paso -1
		f<-f*i
	FinPara
Fin Funcion

// Función Combinatoria
Funcion c <- Combinar(n,k)
	numerador <- factorial(n)
	denominador <- factorial(k)*factorial(n-k)
	c <- numerador/denominador
FinFuncion

// Algorito para triangulo de Pascal
Algoritmo TrianguloPascal
	Escribir 'Ingresa n ='
	Leer n
	k <- 0
	Para k<-0 Hasta n Hacer
		Escribir ' ',Combinar(n,k), ' ' Sin Saltar
		
	FinPara
	Escribir " "
FinAlgoritmo

