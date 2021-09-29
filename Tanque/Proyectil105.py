from Tanque.Proyectil import *

class Proyectil105(Proyectil):
    def __init__(self, daño,numeroBalas):
        Proyectil.__init__(self, daño, numeroBalas)

    # futura construcción
    def efectoDestructivo(self):
        pass