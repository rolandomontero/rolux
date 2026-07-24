#-------------------------------------------------------------------------------
# Name:         Objeto Persona
# Purpose:      Comprender programar entorno a objeto (POO)
#
# Author:      rolan
#
# Created:     10-09-2020
# Copyright:   (c) rolan 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------

class Persona(object):
    def __init__(self, nombre, rut):
        self.nombre =nombre
        self.rut = rut

    def dime_tu_nombre(self):
        print("Mi nombre es, ",self.nombre)

    def cambiar_nombre(self, nombre_nuevo):
        self.nombre = nombre_nuevo

habitante = Persona("Juan","12123123")

print(" Nombre del habitante ", habitante.nombre)

habitante.dime_tu_nombre()

#Cambiar el nombre del habitante
nombre =input("Su mombre ")
habitante.cambiar_nombre(nombre)

print("dime tu nombre ")
habitante.dime_tu_nombre()
