import pygame
from GUI.colores import *

from Tanque.Proyectil import *

class Proyectil105(Proyectil):
    def __init__(self, daño, stock):
        Proyectil.__init__(self, daño, stock)
        self.imagen=pygame.image.load("GUI/imagenes/armas/proyectil105.png")
        self.color=ROJO

    # futura construcción
    def efectoDestructivo(self):
        pass