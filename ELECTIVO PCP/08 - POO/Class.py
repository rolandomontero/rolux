#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      rolan
#
# Created:     10-09-2020
# Copyright:   (c) rolan 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from datetime import date
from datetime import datetime

class Persona(object):
    def __init__(self, nombre, fnac, rut):
        self.nombre=nombre
        self.fnac=fnac
        self.rut=rut

    def muestra_nombre(self):
        print(self.nombre)

    def muestra_fnac(self):
        print(self.fnac)

    def muestra_rut(self):
        print ("Su RUT es ", self.rut)


class Alumno(Persona):
    def __init__(self,  nombre, fnac, rut, colegio, curso):
        Persona.__init__(self, nombre, fnac, rut)
        self.colegio=colegio
        self.curso=curso



def main():
    print("Hola, por favor ingresa tus datos")

    #Persona = persona(nombre:=input("Nombre :"), input('Introducir fecha inicial (dd/mm/aaaa): ') , int(input("RUT :")))

    #print(Persona.nombre)
    #Persona.muestra_rut()
    ALM1 = Alumno("RAUL",'#21-01-2020#',int(8583504),"CGV","3ºA")
    ALM2= Alumno("JORGE","123",1234,"ICPV","IV-A")

    print(ALM1.colegio)
    ALM1.muestra_rut()
    ALM1.muestra_nombre()



    input()

    pass

if __name__ == '__main__':
    main()
