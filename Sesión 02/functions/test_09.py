"""Programación funcional con Python"""

var_1 = 50
var_2 = 120

"""Input: dos variables que pasarán por parámetro de la función"""
"""a, b: parámetros de la función 'sumar'"""


def sumar(a, b):
    return a + b


#def sumar(a, b):
#    suma = a + b
#    return suma

resultado = sumar(var_1, var_2)
"""Output: Lo que retorna la función"""
print(resultado)

resultado_2 = sumar(90.7, 150.89)
print(resultado_2)
