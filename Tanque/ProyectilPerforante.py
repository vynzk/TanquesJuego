from Tanque.Proyectil import *


class ProyectilPerforante(Proyectil):

    def __init__(self, daño, stock):
        Proyectil.__init__(self,daño, stock)

    # implementar en un futuro
    def efectoDestructivo(self):
        pass
