import pygame

class Proyectil:
    def __init__(self, daño, stock):
        self.daño = daño
        self.stock = stock
        self.imagen = pygame.image.load("GUI/imagenes/armas/bomb.png")
        self.nombre = 'default'

    def efectoDestructivo(self):
        pass
    def redimensionarImagen(self):
        self.imagen= pygame.transform.scale(self.imagen, (50,50) )