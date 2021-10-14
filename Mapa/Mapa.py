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
        self.imagenCemento = "GUI/imagenes/bloque/bloqueTierra2.png"

    def dibujarMapa(self, pantalla):
        for bloque in self.listaBloques:
            bloque.dibujar()

    def generarMatriz(self, pantalla):  # define la matriz de bloques, mirar listaMapas.py
        i = 0
        largFila = len(self.mapa[0])  # se escoque self.mapa[0] ya que todas las filas tienen la misma cant filas
        # se recorre la matriz tantas veces como columnas existan
        while i < largFila:
            j = 0
            while j < len(self.mapa):  # se recoorren todas las filas
                if self.mapa[j][i] == 1:
                    bloque = Bloque(pantalla, self.pixel_x, self.pixel_y, self.imagenCemento, i * self.pixel_x,
                                    j * self.pixel_y)
                    self.listaBloques.append(bloque)
                elif self.mapa[j][i] == 2:
                    self.posPosiblesJug.append([i * self.pixel_x, j * self.pixel_y])
                j += 1
            i += 1

    def buscarBloque(self, x, y):
        for bloque in self.listaBloques:
            if bloque.x == x and bloque.y == y:
                return bloque
        return None

    def destruir(self, bloque):
        if bloque is not None:
            self.listaBloques.remove(bloque)

    def destruirZonaImpacto(self, bloqueImpactado, dañoArma):

        self.destruir(bloqueImpactado)  # todos rompen el bloque de impacto
        # Proyectil 105
        if dañoArma == 50:
            pass
        # Proyectil 105 o Perforante, comparten romper los bloques de los lados iz y derecho
        if dañoArma == 40 or dañoArma == 50:
            bloqueIzquierda = self.buscarBloque(bloqueImpactado.x - 40, bloqueImpactado.y)
            bloqueDerecha = self.buscarBloque(bloqueImpactado.x + 40, bloqueImpactado.y)
            # destrucción de los bloques
            self.destruir(bloqueIzquierda)
            self.destruir(bloqueDerecha)
