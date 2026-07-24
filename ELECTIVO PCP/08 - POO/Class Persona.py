#-------------------------------------------------------------------------------
# Name:        módulo1
# Purpose:
#
# Author:      rolan
#
# Created:     09-10-2020
# Copyright:   (c) rolan 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import os
import sys


class Persona:
    Nombre =""
    RUT=int()
    peso=float()

    def __init__(self, nombre, RUT, peso):
        self.Nombre = nombre
        self.RUT = RUT
        self.peso = peso

    def respirar(self):
        print("Yo, ", self.Nombre, "estoy respirando")

    def muere(self, vive):
        if vive==True :
            sys.exit(0)



def main():

    persona=Persona("Rolo",8583504,80)

    while True:
        persona.muere(False)
        s=input("Quieres vivir?")
        if s=="s":
            persona.respirar()
        else: persona.muere(True)




    pass

if __name__ == '__main__':
    main()
