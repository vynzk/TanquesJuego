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
        self.posPosiblesJug= []
        self.mapa = mapa

    def dibujarMapa(self, pantalla):
        for bloque in self.listaBloques:
            bloque.dibujar()
        # debug
        for bloque in self.posPosiblesJug:
            bloque.dibujar()

    def generarMatriz(self, pantalla):  # define la matriz de bloques, mirar listaMapas.py
        x = 0
        y = 0
        for fila in self.mapa:
            for numero in fila:
                if numero == 1:
                    bloque = Bloque(pantalla, self.pixel_x, self.pixel_y, BLANCO, x, y)
                    self.listaBloques.append(bloque)
                # debug
                elif numero==2:
                    posibleJugador=Bloque(pantalla, self.pixel_x, self.pixel_y, AZUL, x, y)
                    self.posPosiblesJug.append(posibleJugador)
                x += self.pixel_x
            x = 0
            y += self.pixel_y
