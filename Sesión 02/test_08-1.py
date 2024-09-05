"""Ingreso de datos mediante consola"""

nombre = input("Ingrese su nombre: ")
edad = input("Ingrese su edad: ")

print(type(int(edad)))
print("Bienvenido/a {nombre_usuario} usted tiene {edad_usuario} años".format(nombre_usuario=nombre, edad_usuario=int(edad)))
