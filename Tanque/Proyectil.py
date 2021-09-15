import pygame
from GUI.bloque import Bloque


class Proyectil(Bloque):
    def __init__(self, pantalla, ancho, alto, color, x, y):
        Bloque.__init__(self, pantalla, ancho, alto, color, x, y)
        self.vivo = False
        self.balaImagen = pygame.image.load("GUI/imagenes/bomb.png").convert_alpha()
        self.redimensionaBala()

    def activaProyectil(self, coordenadasXY):
        self.vivo = True

    def sigueTrayectoria(self, coordenadasXY):  # para que siga la trayectoria de disparo
        """
        objetivo??: que siga la trayectoria de disparo... al ser un
		objeto... se puede crear una función que determine cuando colisona
		con la coordenada de otro (como el cuadrado rosa con la interfaz)
		"""
        if (self.vivo==True):
            self.pantalla.blit(self.balaImagen, coordenadasXY)

    def redimensionaBala(self):
        self.balaImagen = pygame.transform.scale(self.balaImagen, (30, 30))
