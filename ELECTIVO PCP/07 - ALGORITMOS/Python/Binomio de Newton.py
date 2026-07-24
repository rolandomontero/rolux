# Este codigo ha sido generado por el modulo psexport 20160506-w32 de PSeInt.
# Es posible que el codigo generado no sea completamente correcto. Si encuentra
# errores por favor reportelos en el foro (http://pseint.sourceforge.net).


# En python no hay forma de elegir como pasar una variable a una
# funcion (por referencia o por valor). Las variables "inmutables"
# (str, int, float, bool) se pasan siempre por copia mientras que
# las demas (listas, objetos, etc.) se pasan siempre por referencia.
# Esto coincide con el comportamiento por defecto en pseint, pero
# cuando utiliza las palabras clave "Por Referencia" para
# alterarlo la traducción no es correcta.

# Función Factorial
def factorial(n):
	f = 1
	for i in range(1,n+1):
		f = f*i
	if n==0:
		f = 1
	return f

# Función Combinatoria
def combinar(n, k):
	numerador = factorial(n)
	denominador = factorial(k)*factorial(n-k)
	c = numerador/denominador
	return c

# Algorito para Binomio de Newton
if __name__ == '__main__':
	binomio = str()
	print("Ingresa un valor para n =")
	n = int(input())
	for i in range(n+1):
		nck = combinar(n,i)
		a = n-i
		b = i
		if i==0:
			binomio = "a^"+str(n)+" "
		elif i==1:
			binomio = binomio+"+ "+str(nck)+"a^"+str(a)+"*b "
		elif i==(n-1):
			binomio = binomio+"+ "+str(nck)+"a*b^"+str(b)+" "
		elif i==n:
			binomio = binomio+"+ b^"+str(n)+" "
		else:
			binomio = binomio+"+ "+str(nck)+"a^"+str(a)+"*b^"+str(b)+" "
	print(binomio)
	pausa=input();
	

