


def venta():
    l_venta=[]
    vendedor =int(input("Ingrese vendedor ="))
    combo=int(input("Ingrese combo ="))
    l_venta.append(vendedor)
    l_venta.append(combo)
    return l_venta

def anlisis_vendedor(Ventas):
    vendedores = [0 for i in range(6)]
    for vendedor in range(6):
        for venta in Ventas:
            if venta[0]==vendedor:
                vendedores[venta[0]]+=1

    Max=0
    Min=1000
    VMax=0
    VMin=0

    for v in range(1,6):

        print("Vendedor ",v," numero de combo ", vendedores[v],"\n")
        if vendedores[v]>Max :
            Max = vendedores[v]
            VMax = v
        if vendedores[v]<Min :
            Min = vendedores[v]
            VMin = v

    print("El Vendedor con menos venta es ", VMin, " con ", Min," ventas")
    print("El Vendedor con mayor venta es ", VMax, " con ", Max," ventas")



ventas=[]
abierto = True

while abierto :
    pregunta=input("Ingresar una venta (s/n)?")

    if pregunta=="n":
        abierto=False
    else:
        ventas.append(venta())

print(ventas)
anlisis_vendedor(ventas)



