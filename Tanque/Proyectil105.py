from Tanque.Proyectil import *

class Proyectil105(Proyectil):
    def __init__(self, daño, stock):
        Proyectil.__init__(self, daño, stock)

    # futura construcción
    def efectoDestructivo(self):
        pass