#-------------------------------------------------------------------------------
# Name:        módulo2
# Purpose:
#
# Author:      rolan
#
# Created:     14-09-2020
# Copyright:   (c) rolan 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------


from __future__ import division
import matplotlib.pyplot as plt
import numpy as np

def func(a,b,c):
    @np.vectorize
    def f(x):
        return a*x**2 + b*x + c
    return f

def quadratic(a,b=0,c=0):
    f = func(a,b,c)
    x0 = -b/(2*a)
    X = np.arange(x0-4,x0+4,0.01)
    return x0,f(x0),X,f(X)

blues = ['cyan', 'blue', 'purple']
reds = ['magenta', 'salmon', 'red']

for i,(a,b) in enumerate(zip((1,2,3),(2,4,6))):
    x0,y0,X,Y = quadratic(a,b,c=3)
    c = reds[i]
    plt.scatter(X,Y,s=2,color=c)
    plt.scatter(x0,y0,s=100,color=c)
    print ('x0',x0,'y0',y0)

    x0,y0,X,Y = quadratic(a)
    c = blues[i]
    plt.scatter(X,Y,s=2,color=c)
    plt.scatter(x0,y0,s=100,color='k')

ax = plt.axes()
ax.set_xlim(-3,3)
ax.set_ylim(-1,5)
plt.grid(True)
plt.savefig('example.png')