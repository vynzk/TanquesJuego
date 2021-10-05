from GUI.bloque import Bloque
import pygame
from GUI.colores import *

pygame.init()


class Mapa:
    def __init__(self, mapa):
        # medidas
        self.ancho = 1280
        self.alto = 730
        self.pixel_y = 40
        self.pixel_x = 40
        self.listaBloques = []
        self.posPosiblesJug = []
        self.bloquePos = []
        self.mapa = mapa

    def dibujarMapa(self, pantalla):
        for bloque in self.listaBloques:
            bloque.dibujar()
    def generarMatriz(self, pantalla):  # define la matriz de bloques, mirar listaMapas.py
        i = 0
        largFila = len(self.mapa[0]) # se escoque self.mapa[0] ya que todas las filas tienen la misma cant filas
        # se recorre la matriz tantas veces como columnas existan
        while i < largFila:
            j = 0
            while j < len(self.mapa):  # se recoorren todas las filas
                if self.mapa[j][i] == 1:
                    bloque = Bloque(pantalla, self.pixel_x, self.pixel_y, BLANCO, i * self.pixel_x, j * self.pixel_y)
                    self.listaBloques.append(bloque)
                elif self.mapa[j][i] == 2:
                    self.posPosiblesJug.append([i * self.pixel_x, j * self.pixel_y])
                j += 1
            i += 1

