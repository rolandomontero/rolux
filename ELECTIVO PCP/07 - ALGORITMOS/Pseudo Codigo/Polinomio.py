# Este codigo ha sido generado por el modulo psexport 20180802-w32 de PSeInt.
# Es posible que el codigo generado no sea completamente correcto. Si encuentra
# errores por favor reportelos en el foro (http://pseint.sourceforge.net).


# Ejemplo de Dimensión
# Ingresar coeficiente de un polinomio
# Autor :Rolando E. Montero A.
# Fecha :30-agosto-2019
# email : rolandomontero@mclautaro.cl
# ////////////////////////////////////
if __name__ == '__main__':
	p = [float() for ind0 in range(10)]
	print("Grado del Polinomio?")
	n = input()
	print("un numero a=")
	a = float(input())
	i = 1
	while i<=n+1:
		print("Ingresa coeficiente x^",i-1,"=")
		p[i-1] = float(input())
		p[i-1] = p[i-1]*a
		i = i+1
	i = 1
	print("El polinomio queda ")
	while i<=n:
		print(p[i-1],"x^",i-1," + ", end="")
		i = i+1
	print(p[i-1],"x^",i-1)

