from GUI.bloque import Bloque
import pygame

pygame.init()


class Mapa:

    def __init__(self):
        # medidas
        self.ancho = 1280
        self.alto = 730
        self.pixel_y = 20
        self.pixel_x = 20
        self.listaBloques = []

        # colores
        self.blanco = (255, 255, 255)
        self.negro = (0, 0, 0)
        self.rojo = (255, 0, 0)
        self.verde = (0, 255, 0)
        self.azul = (0, 0, 255)
        self.marron = (150, 70, 10)
        self.azulClaro = (101, 113, 135)
        self.azulOscuro = (18, 32, 36)
        # mapa
        self.mapa = [
            "                                                                ",
            "                                                                ",
            "                                                                ",
            "                                                                ",
            "                                                                ",
            "                                                                ",
            "                                                                ",
            "                                                                ",
            "                                                                ",
            "                                                                ",
            "                                                                ",
            "                                                                ",
            "                                                                ",
            "                                                                ",
            "                                                                ",
            "                                                                ",
            "                                                                ",
            "                                                                ",
            "                                                                ",
            "                                                                ",
            "                                                                ",
            "                                                                ",
            "                                                       XXXXXXXXX",
            "         XXXXX                   X                 XXXXXXXXXXXXX",
            "        XXXXXXX                 XXX              XXXXXXXXXXXXXXX",
            "       XXXXXXXXX              XXXXXX            XXXXXXXXXXXXXXXX",
            "     XXXXXXXXXXX             XXXXXXXX        XXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXX    XXXXXXXXXXXXXX   XXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXX XXXXXXXXXXXXXXXX  XXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX", ]

    def dibujar(self, pantalla):  # define la matriz de cuadrados
        x = 0
        y = 0
        for fila in self.mapa:
            for muro in fila:
                if muro == "X":
                    bloque = Bloque(pantalla, self.pixel_x, self.pixel_y, (18, 25, 53), x, y)
                    self.listaBloques.append(bloque)
                    bloque.dibujar()
                x += self.pixel_x
            x = 0
            y += self.pixel_y
