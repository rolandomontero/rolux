# Este codigo ha sido generado por el modulo psexport 20180802-w32 de PSeInt.
# Es posible que el codigo generado no sea completamente correcto. Si encuentra
# errores por favor reportelos en el foro (http://pseint.sourceforge.net).

from math import sqrt

if __name__ == '__main__':
	# Iniciar variables
	a = 0
	b = 0
	c = 0
	d = 0
	x1 = 0
	x2 = 0
	re = 0
	im = 0
	# El usuario debe ingresar los coeficientes de la ecuaci�n cuadratica.
	while a==0:
		a = float(input(" Ingresar coeficiente cuadratico a="))

	b = float(input(" Ingresar coeficiente lineal b="))

	c = float(input(" Ingresar coeficiente independiente c="))
	# Calcular el discriminante
	d = b**2-4*a*c
	# Evaluar el discriminante
	# Dos raices reales x1 y x2
	if d>0:
		x1 = (-b-sqrt(d))/(2*a)
		x2 = (-b+sqrt(d))/(2*a)
		print(" La soluci�n corresponde a dos raices reales, x1=",x1," x2=",x2)
	# �nica r�iz reales x1
	if d==0:
		x1 = (-b)/(2*a)
		print(" La soluci�n corresponde a una �nica r�iz real, x=",x1)
	# Dos raices Complejas x1 y x2
	if d<0:
		re = (-b)/(2*a)
		im = (sqrt(-d))/(2*a)
		print(" La soluci�n corresponde a dos raices complejas,")
		print("x1=",re," - ",im," i")
		print("x2=",re," + ",im," i")

