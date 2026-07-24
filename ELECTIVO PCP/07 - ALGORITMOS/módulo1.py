#-------------------------------------------------------------------------------
# Name:        módulo1
# Purpose:
#
# Author:      rolan
#
# Created:     07-09-2020
# Copyright:   (c) rolan 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------


def Polinomio(nombre):
    print("================================================")
    print ("Ingresa los coeficientes del Polinomio ", nombre)
    n=int(input("Ingresa el grado del Polinomio "))+1
    P=[int () for i in range(n)]
   
    for i in range(n):
        print("Ingresa el coeficiente del termino ",i)
        P[i]=int(input())
    return P

def Sumar(P, Q):
    print("================================================")
    n=len(P)
    m=len(Q)
    l =n+m-1
    R = [int() for i in range(l)]

    for j in range(m):
        for i in range(n):
            R[i+j]=R[i+j] + P[i]*Q[j]
            
            

    print("El resultado es ")
    print(R)


def main():
    Sumar(Polinomio("P(x)"),Polinomio("Q(x)"))
    pass

if __name__ == '__main__':
    main()
    input()
