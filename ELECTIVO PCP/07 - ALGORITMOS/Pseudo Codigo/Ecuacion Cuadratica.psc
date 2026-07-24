Algoritmo Ecuacion_Cuadratica
	// Iniciar variables
	a<-0
	b<-0
	c<-0
	d<-0
	x1<-0
	x2<-0
	re<-0
	im<-0
	
	// El usuario debe ingresar los coeficientes de la ecuación cuadratica.
	mientras a=0
		Escribir " Ingresar coeficiente cuadratico a="
		Leer a
	FinMientras
	
	Escribir " Ingresar coeficiente lineal b="
	Leer b
	
	Escribir " Ingresar coeficiente independiente c="
	Leer c
	
	// Calcular el discriminante
	d<- b^2 - 4*a*c
	
	// Evaluar el discriminante

	si d>0 Entonces // Dos raices reales x1 y x2
		x1<-(-b-raiz(d))/(2*a)
		x2<-(-b+raiz(d))/(2*a)
		
		Escribir " La solución corresponde a dos raices reales, x1=",x1, " x2=", x2
	FinSi
	
	si d=0 Entonces // Única ráiz reales x1
		x1<-(-b)/(2*a)		
		Escribir " La solución corresponde a una única ráiz real, x=",x1
	FinSi
	
	si d<0 Entonces // Dos raices Complejas x1 y x2
		re<-(-b)/(2*a)
		im<-(raiz(-d))/(2*a)
		
		Escribir " La solución corresponde a dos raices complejas," 
		Escribir "x1=",re, " - ", im," i"
		Escribir "x2=",re, " + ", im," i"
	FinSi
	
FinAlgoritmo
