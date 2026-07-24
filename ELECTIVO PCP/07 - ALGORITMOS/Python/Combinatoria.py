#Función Factorial
def factorial(n):
	f = 1
	for i in range(1,n+1):
		f = f*i
	if n==0:
		f = 1
	return f

# Función Combinatoria
def combinatoria(n, k):
	numerador = factorial(n)
	denominador = factorial(k)*factorial(n-k)
	c = numerador/denominador
	return c

# Cuerpo del programa
n=int(input("Ingresa n="));
for k in range(0, n+1):
        print(" ",n, "C",k," =", combinatoria(n, k));
      
