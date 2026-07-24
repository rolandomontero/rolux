Funcion f <- factorial ( n )
	f<-1
	si n=0 Entonces
		n<-1
	FinSi
	
	para i<-n hasta 1 Con Paso -1
		f<-f*i
	FinPara
Fin Funcion



Algoritmo Calculo_de_Combinatoria
	//Iniciar variable
	numerador<-1
	denominador<-1
	combinatoria<-1
	
	
	//Solicitar valores de n y k 
	Escribir "Ingresa una valor para n="
	leer n
	
	Escribir "Ingresa una valor para k="
	leer k
	
	//Cálculo del numerador
	numerador<-factorial(n)
	
	//Cálculo del denominador
	denominador<- factorial(k)*factorial(n-k)
	
	//Calculo de Combinatoria
	combinatoria<-numerador/denominador
	
	//Publicar resultados
	Escribir "La combinatoria de ", k," en ", n, " es ", combinatoria
	
	
FinAlgoritmo
