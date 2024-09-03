"""Ingreso de datos mediante consola"""

"""Asignación múltiple"""
"""Referencia a dos o más variables"""

var1 = input("Ingrese su nombre de usuario: ")
var2 = input("Ingrese su nombre: ")
var3 = input("Ingrese su edad: ")

usuario, nombre, edad = var1, var2, var3

print("Su nombre de usuario es: {} y tiene {} años".format(usuario, edad))
