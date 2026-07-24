#-------------------------------------------------------------------------------
# Name:         Operaciones vectoriales
# Purpose:      Resalizar operaciones de suma de dos vectores y
#               el producto escalar con vector
#
# Author:      Rolando Montero
#
# Created:     03-09-2020
# Copyright:   (c) MC Lautaro's 2020
# Licence:     GNU
#-------------------------------------------------------------------------------

n=int(input("Ingresa orden del vector n="))

#Inicializar variable

#método append para variable v
v=[]

for i in range(n):
    v.append(0)

#metaformico para variables u y R
u=[int() for i in range(n)]
R=[int() for i in range(n)]




#Ingresar valores de las componentes del vector v
print("==========================================")
print("=== INGRESAR COMPONENTES DEL VECTOR V  ===")
print("==========================================")

for i in range(n):
    print(" v",i,"=")
    v[i]=int(input())


#Ingresar valores de las componentes del vector u
print("==========================================")
print("=== INGRESAR COMPONENTES DEL VECTOR U  ===")
print("==========================================")

for j in range(n):
    print(" u",j," =")
    u[j]=int(input())

#Operación de Suma R= v + u
for z in range(n):
    R[z]=v[z]+u[z]

print("La suma de los vectores v con u, es R=",R)




