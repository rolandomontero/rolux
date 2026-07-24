// Función Factorial
Funcion f <- factorial(n)
	f <- 1
	Para i<-1 Hasta n Hacer
		f <- f*i
	FinPara
	Si n=0 Entonces
		f <- 1
	FinSi
FinFuncion

// Función Combinatoria
Funcion c <- Combinar(n,k)
	numerador <- factorial(n)
	denominador <- factorial(k)*factorial(n-k)
	c <- numerador/denominador
FinFuncion

// Algorito para Binomio de Newton
Algoritmo Binomio_Newton
Binomio es Cadena
	Escribir 'Ingresa un valor para n ='
	Leer n
	
	Para i desde 0 hasta n
		nCk = Combinar(n,i)
		a=n-i
		b=i
		
		Segun i Hacer
			0:
				Binomio <- "a^" + ConvertirATexto(n)+ " "
			1:
				si a=1 Entonces
					Binomio <- Binomio + "+ " + ConvertirATexto(nCk) + "a*b "	
				Sino
					Binomio <- Binomio + "+ " + ConvertirATexto(nCk) + "a^" + ConvertirATexto(a)+ "*b "	
				FinSi
				
			(n-1):
				Binomio <- Binomio + "+ " + ConvertirATexto(nCk) + "a*b^" + ConvertirATexto(b) + " "
			n:
				Binomio <- Binomio + "+ b^" + ConvertirATexto(n)+ " "
			De Otro Modo:
				Binomio <- Binomio + "+ " + ConvertirATexto(nCk) + "a^" + ConvertirATexto(a)+ "*b^" + ConvertirATexto(b) + " "
		Fin Segun
	FinPara
	Escribir Binomio
FinAlgoritmo

