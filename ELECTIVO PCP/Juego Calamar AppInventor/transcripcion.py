def ADN_ARNm(cadena):
	adn="TAGC"
	arn_m="aucg"
	for i in range(0,4):
		cadena = cadena.replace(adn[i],arn_m[i])
	return cadena