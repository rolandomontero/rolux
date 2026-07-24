' Este codigo ha sido generado por el modulo psexport 20160506-w32 de PSeInt.
' Es posible que el codigo generado no sea completamente correcto. Si encuentra
' errores por favor reportelos en el foro (http://pseint.sourceforge.net).

Module BINOMIO_NEWTON

	' Función Factorial
	Public Function factorial(ByVal n As Double)
		Dim f As Double
		Dim i As Double
		f = 1
		For i=1 To n
			f = f*i
		Next i
		If n=0 Then
			f = 1
		End If
		Return f
	End Function

	' Función Combinatoria
	Public Function combinar(ByVal n As Double, ByVal k As Double)
		Dim c As Double
		Dim denominador As Double
		Dim numerador As Double
		numerador = factorial(n)
		denominador = factorial(k)*factorial(n-k)
		c = numerador/denominador
		Return c
	End Function

	' Algorito para Binomio de Newton
	Sub Main()
		Dim a As Double
		Dim b As Double
		Dim binomio As String
		Dim i As Double
		Dim n As Double
		Dim nck As Double
		Console.WriteLine("Ingresa un valor para n =")
		n = Double.Parse(Console.ReadLine())
		For i=0 To n
			nck = combinar(n,i)
			a = n-i
			b = i
			Select Case i
			Case 0
				binomio = "a^"&CStr(n)&" "
			Case 1
				binomio = binomio&"+ "&CStr(nck)&"a^"&CStr(a)&"*b "
			Case (n-1)
				binomio = binomio&"+ "&CStr(nck)&"a*b^"&CStr(b)&" "
			Case n
				binomio = binomio&"+ b^"&CStr(n)&" "
			Case Else
				binomio = binomio&"+ "&CStr(nck)&"a^"&CStr(a)&"*b^"&CStr(b)&" "
			End Select
		Next i
		Console.WriteLine(binomio)
	End Sub

End Module
