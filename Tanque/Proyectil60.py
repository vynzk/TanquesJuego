import pygame

from Tanque.Proyectil import *
from GUI.colores import *

class Proyectil60(Proyectil):
    def __init__(self, daño, stock):
        Proyectil.__init__(self,daño, stock)
        self.imagen=pygame.image.load("GUI/imagenes/armas/proyectil60.png")
        self.color=AMARILLO

    # implementar en un futuro
    def efectoDestructivo(self):
        pass