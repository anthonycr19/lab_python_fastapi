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


"""Aplicando herencia"""
"""Creamos una clase hija"""


class carroVolador(Carro):

    ruedas = 6
    def __init__(self, estadoVolando=False):
        super().__init__()
        self.estadoVolando = estadoVolando


    def vuela(self):
        self.estadoVolando = True

    def aterriza(self):
        self.estadoVolando = False


carro1 = Carro()
carro1.color = "Rojo"
carro1.aceleracion = 45

carroVol = carroVolador()
carroVolador.color = "Blanco"
carroVolador.aceleracion = 55

print(carroVol.color)

carroVol.vuela()
print("El estado actual del carro volador es: {}".format(carroVol.estadoVolando))

carroVol.aterriza()
print("El estado actual del carro volador es: {}".format(carroVol.estadoVolando))
