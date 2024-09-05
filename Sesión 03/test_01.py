"""
    Programación orientada a objetos
"""


class Carro:
    """Atributos"""
    ruedas = 4

    """Constructor: Valores que van a tener por defecto mi clase que se le instanciará a una varaible"""
    def __int__(self, color, aceleracion):
        self.color = color
        self.aceleracion = aceleracion
        self.velocidad = 0


    """Métodos: son las funciones de la clase"""
    def acelerar(self):
        self.velocidad = self.velocidad + self.aceleracion

    def frena(self):
        velocidad = self.velocidad - self.aceleracion
        if velocidad<0:
            velocidad=0
        self.velocidad = velocidad


"""Instaciones nuestra clase"""
carro1 = Carro()
carro1.color = "Negro"
carro1.aceleracion = 50
carro1.velocidad = 0
print(carro1.color)
print(carro1.aceleracion)
print("La velocidad inicial de mi carro 1 es: {}".format(carro1.velocidad))
print("La cantidad de ruedas que tiene mi primer carro es: {}".format(carro1.ruedas))

carro2 = Carro()
carro2.color = "Rojo"
carro2.aceleracion = 70
carro2.velocidad = 0
print(carro2.color)
print(carro2.aceleracion)
print("La velocidad inicial de mi carro 2 es: {}".format(carro2.velocidad))
print("La cantidad de ruedas que tiene mi segundo carro es: {}".format(carro2.ruedas))

carro2.marchas = 2000
print("El número de marchas de mi 2do carro es: {}".format(carro2.marchas))


"""
Importante
No es posible llamar un atributo de dato que se le ha asignado a otra instancia de la clase
"""
#print(carro1.marchas)

