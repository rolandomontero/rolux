// Ejemplo de Dimensión
// Ingresar coeficiente de un polinomio
// Autor :Rolando E. Montero A.
// Fecha :30-agosto-2019
// email : rolandomontero@mclautaro.cl
//////////////////////////////////////
Algoritmo escalar_por_polinomio
	Dimension P[10]
	Escribir 'Grado del Polinomio?'
	Leer n
	Escribir 'un numero a='
	Leer a
	i <- 1
	Mientras i<=n+1 Hacer
		Escribir 'Ingresa coeficiente x^',i-1,'='
		Leer P[i]
		P[i] <- P[i]*a
		i <- i+1
	FinMientras
	i <- 1
	Escribir 'El polinomio queda '
	Mientras i<=n Hacer
		Escribir P[i],'x^',i-1,' + ' Sin Saltar
		i <- i+1
	FinMientras
	Escribir P[i],'x^',i-1
FinAlgoritmo

