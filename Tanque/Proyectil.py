import pygame

class Proyectil:
    def __init__(self, nombre, municion, daño, pathImagen, color):
        self.nombre= nombre
        self.municion = municion
        self.daño = daño
        self.imagen = pathImagen
        self.color=color
        self.redimensionarImagen()

    def redimensionarImagen(self):
        self.imagen= pygame.transform.scale(pygame.image.load(self.imagen), (50,50))