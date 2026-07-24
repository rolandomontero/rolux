Algoritmo Lista_de_numeros
	Escribir "Ingrese Primer entero"
	Leer N1
	Escribir "Ingrese Segundo entero"
	Leer N2
	Si N1<N2 Entonces
		A <- N1
		B <- N2
	Sino
		A <- N2
		B <- N1
	FinSi
	C <- A
	Mientras C<=B Hacer
		Si C MOD 2=1 Entonces
			Escribir C
		FinSi
		C <- C+1
	FinMientras
FinAlgoritmo

