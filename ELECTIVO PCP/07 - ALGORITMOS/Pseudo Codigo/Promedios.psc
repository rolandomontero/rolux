Algoritmo Calcula_Promedio
	// INICIANDO VARIABLES
	n <- 0
	NOTA <- 0
	SUMA <- 0
	PROMEDIO <- 0
	// Interaccion con el usuario del número de notas
	Escribir 'Ingresa el número de notas '
	Leer n
	// Ingresa notas desde el usuario
	// Utiliza i, como indice para indicar el número de ubicación de la nota
	Para i<-1 Hasta n Hacer
		Escribir 'Ingresa nota',i,' ='
		Leer NOTA
		SUMA <- SUMA+NOTA
	FinPara
	// Calcular promedio 
	PROMEDIO <- SUMA/n
	Escribir 'El promedio de las notas es, ',PROMEDIO
FinAlgoritmo
