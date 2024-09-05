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
        if velocidad < 0:
            velocidad = 0
        self.velocidad = velocidad


carro1 = Carro()
carro1.color = "Negro"
carro1.aceleracion = 50
carro1.velocidad = 0

carro1.acelerar()
carro1.acelerar()
carro1.acelerar()
carro1.acelerar()

print("La velocidad actual de mi carro 1 es: {}".format(carro1.velocidad))

carro1.frena()
carro1.frena()

print("La velocidad actual de mi carro 1 es: {}".format(carro1.velocidad))
