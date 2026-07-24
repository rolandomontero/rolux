# Este codigo ha sido generado por el modulo psexport 20180802-w32 de PSeInt.
# Es posible que el codigo generado no sea completamente correcto. Si encuentra
# errores por favor reportelos en el foro (http://pseint.sourceforge.net).


if __name__ == '__main__':
	print("Ingrese Primer entero")
	n1 = input()
	print("Ingrese Segundo entero")
	n2 = input()
	if n1<n2:
		a = n1
		b = n2
	else:
		a = n2
		b = n1
	c = a
	while c<=b:
		if c%2==1:
			print(c)
		c = c+1

