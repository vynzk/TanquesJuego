from Tanque.Proyectil import *

class Proyectil60(Proyectil):
    def __init__(self, daño, stock):
        Proyectil.__init__(self,daño, stock)

    # implementar en un futuro
    def efectoDestructivo(self):
        pass