import pygame

from Tanque.Proyectil import *
from GUI.colores import *


class ProyectilPerforante(Proyectil):

    def __init__(self, daño, stock):
        Proyectil.__init__(self,daño, stock)
        self.imagen=pygame.image.load("GUI/imagenes/armas/proyectilPerforante.png")
        self.color=NARANJA
        self.redimensionarImagen()
        self.nombre= 'proyectil perforante'


    # implementar en un futuro
    def efectoDestructivo(self):
        pass
