#-------------------------------------------------------------------------------
# Name:         Producto de Polinomios
# Purpose:      Multiplica dos polinomios
#
# Author:      Rolando MOntero
#
# Created:     07-09-2020
# Copyright:   (c) MC Lautaro's 2020
# Licence:     GNU
#-------------------------------------------------------------------------------

def Polinomio(nombre):
    print("========================================")
    print("Ingresa los coeficientes del polinomio ", nombre)

    n=int(input("Ingresa el grado del polinomio "))+1
    P=[int() for i in range(n)]
    print(P)
    for i in range(n):
        print("Ingresa el coeficientes del término ",i)
        P[i]=int(input())
    print(P)
    return P

def Producto(p, q):
    n=len(p)
    m=len(q)
    print("========================================")
    print("grado de P=",n-1, "grado de Q=",m-1)

    l = n+m-1
    R=[int() for i in range(l)]
    print(" Polinomio R=",R)
    for j in range(m): # Bucle exterior es el recorrido de Q(x)
        for i in range(n): # Bucle interior el recorrido de P(x)
            cR = p[i]*q[j]
            #print("P[",i,"] = ",p[i], " x Q[",j,"] = ",q[j], " = ",cR)
            R[i+j]=R[i+j]+cR
            #print("R[",i+j,"]=",R[i+j])
            #input()

    print("El resultado del producto de P(x)xQ(x)=R(x) =", R)


def Suma(p,q):
    pass





def main():

    Producto(Polinomio("P(X)"), Polinomio("Q(X)"))

    pass

if __name__ == '__main__':
    main()
