#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Digito RUT.py
#  

rut = input("Ingrese su run :");
ln = len(rut)-1;
c=2;
b=0;

for i in range(len(rut)):
        a = int(rut[ln-i])
        b = b + a*c
        c = c + 1*(c<7) -5 *(c==7)

d = 11 - b%11;
if d==10:
	dv="K"
elif d==11:
    dv="0"
else:
    dv=d

print("sur run :",rut,"-",dv,'\n \n');

