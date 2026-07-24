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

// Algorito para Experimento de Bernulli
Algoritmo Bernulli
	Probabilidad Es Real
	p Es Real
	
	Escribir 'Ingresa n ='
	Leer n
	
	Escribir 'Ingresa x ='
	Leer x
	
	Escribir 'Ingresa p ='
	Leer p
	
	Probabilidad<- Combinar(n,x)*(p^x)*((1-p)^(n-x))
	
	Escribir "La probabilidada de X =", x, " en ", n, " con p=",p, " es ", Probabilidad
	
FinAlgoritmo

