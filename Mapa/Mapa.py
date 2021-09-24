from GUI.bloque import Bloque
import pygame
from GUI.colores import *
pygame.init()


class Mapa:
    def __init__(self, mapa):
        # medidas
        self.ancho = 1280
        self.alto = 730
        self.pixel_y = 20
        self.pixel_x = 20
        self.listaBloques = []
        self.mapa = mapa

    def dibujarMapa(self, pantalla):
        for bloque in self.listaBloques:
            bloque.dibujar()

    def generarMatriz(self, pantalla):  # define la matriz de bloques, mirar listaMapas.py
        x = 0
        y = 0
        for fila in self.mapa:
            for caracter in fila:
                if caracter == "X":
                    bloque = Bloque(pantalla, self.pixel_x, self.pixel_y, COLOR_TIERRA, x, y)
                    self.listaBloques.append(bloque)
                x += self.pixel_x
            x = 0
            y += self.pixel_y
